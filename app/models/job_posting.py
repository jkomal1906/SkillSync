from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.base import Base


class JobPosting(Base):
    __tablename__ = "JobPostings"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(150), nullable=False)
    skills = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    posted_date = Column(DateTime, default=datetime.utcnow)
