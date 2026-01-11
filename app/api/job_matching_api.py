from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.database import get_db
from app.models.resume import Resume
from app.models.job_posting import JobPosting  # Your job model
from app.models.job_match import JobMatch
from app.services.job_matcher import match_resume_with_jobs, save_job_matches
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/match",
    tags=["Job Matching"]
)


@router.post("/resume/{resume_id}")
def match_resume_to_jobs(
    resume_id: int,
    top_n: int = 5,
    threshold: float = 0.6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Match a resume to jobs and save top N matches to the DB.
    
    Parameters:
    - resume_id: ID of the resume to match
    - top_n: number of top matches to store
    - threshold: minimum similarity score to consider
    """
    # Fetch the resume
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Prepare resume data for matching
    resume_data: Dict = {
        "skills": resume.skills.split(",") if resume.skills else [],
        "experience": resume.experience or "",
        "education": resume.education or ""
    }

    # Fetch all jobs from DB
    jobs: List[JobPosting] = db.query(JobPosting).all()
    if not jobs:
        return {"matched_jobs": []}

    # Step 1: Compute weighted matches
    matched_jobs = match_resume_with_jobs(
        resume_data=resume_data,
        jobs=jobs,
        top_n=top_n,
        threshold=threshold
    )

    # Step 2: Save matches to DB
    save_job_matches(db=db, resume_id=resume_id, matched_jobs=matched_jobs)

    # Return the matches
    return {"matched_jobs": matched_jobs}
