from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.base import Base
from app.models import user, resume, job_posting, job_match

# Import routers correctly
from app.api.auth import router as auth_router
from app.api.jobs import router as jobs_router
from app.api.resume import router as resume_router
from app.api.job_matching_api import router as job_matching_router


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSync API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Phase 1 only (restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(job_matching_router)
