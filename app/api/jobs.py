from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.job_posting import JobPosting
from app.schemas.job import JobCreateRequest, JobResponse
from app.services.job_matcher import match_resume_with_jobs
from app.schemas.match import JobMatchRequest, JobMatchResponse
from app.core.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/jobs", tags=["Jobs"])

# CREATE JOB

@router.post("/create", response_model=JobResponse)
def create_job(
    job: JobCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job_entity = JobPosting(
        job_title=job.job_title,
        skills=",".join(job.skills),
        description=job.description
    )

    db.add(job_entity)
    db.commit()
    db.refresh(job_entity)

    return {
        "id": job_entity.id,
        "job_title": job_entity.job_title,
        "skills": job_entity.skills.split(","),
        "description": job_entity.description,
        "posted_date": job_entity.posted_date
    }

# LIST ALL JOBS

@router.get("/list", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobPosting).order_by(JobPosting.posted_date.desc()).all()

    return [
        {
            "id": j.id,
            "job_title": j.job_title,
            "skills": j.skills.split(","),
            "description": j.description,
            "posted_date": j.posted_date
        }
        for j in jobs
    ]


