from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class JobMatch(Base):
    __tablename__ = "JobMatches"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(Integer, ForeignKey("Resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("JobPostings.id"), nullable=False)

    similarity_score = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="matches")
    job = relationship("JobPosting")
