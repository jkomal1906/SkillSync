from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import shutil

from app.db.database import get_db
from app.models.resume import Resume
from app.models.job_posting import JobPosting
from app.services.resume_parser import parse_resume, extract_text_from_file
from app.services.job_matcher import match_resume_with_jobs, get_match_history
from app.schemas.resume import ResumeResponse
from app.core.config import UPLOAD_DIR
from app.core.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/resume", tags=["Resume Analysis"])


# ---------- Upload and Analyze Resume ----------
@router.post("/upload-analyze", response_model=ResumeResponse)
async def upload_and_analyze_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF or DOCX files are allowed"
        )

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract resume text
    resume_text = extract_text_from_file(file_path)

    # Parse resume
    parsed_data = parse_resume(file_path)

    # Store resume in DB FIXED
    resume = Resume(
        user_id=current_user.id,   # JWT-based user
        file_path=file_path,
        analysis_result=parsed_data
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    # AI Job Matching
    jobs = db.query(JobPosting).all()

    job_matches = match_resume_with_jobs(
        resume_data={
            "skills": parsed_data.get("skills", []),
            "experience": parsed_data.get("experience", ""),
            "education": parsed_data.get("education", "")
        },
        jobs=jobs,
        top_n=5,
        threshold=0.6
    )

    return {
        "id": resume.id,
        "file_path": resume.file_path,
        "upload_date": resume.upload_date,
        "analysis_result": {
            **parsed_data,
            "job_matches": job_matches
        }
    }


# ---------- Get Resume Match History ----------
@router.get("/{resume_id}/matches")
def get_resume_match_history(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    matches = get_match_history(db, resume_id)

    return {
        "resume_id": resume_id,
        "matches": matches
    }
