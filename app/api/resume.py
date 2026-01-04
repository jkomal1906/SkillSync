from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.db.database import SessionLocal
from app.services.resume_parser import parse_resume
from app.services.job_matcher import match_jobs
from app.models.job_posting import JobPosting
import os
from app.core.config import UPLOAD_DIR
import shutil

router = APIRouter(prefix="", tags=["Resume Analysis"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...), db=Depends(get_db)):
    # Validate file type
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files allowed")

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse the resume (parse_resume handles both file path or UploadFile)
    parsed_data = parse_resume(file_path)

    # Fetch all jobs from DB
    jobs = db.query(JobPosting).all()
    matches = match_jobs(parsed_data["skills"], jobs)

    return {
        "skills": parsed_data["skills"],
        "experience": parsed_data["experience"],
        "education": parsed_data["education"],
        "job_matches": matches
    }
