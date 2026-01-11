from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Resume(Base):
    __tablename__ = "Resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)

    file_path = Column(String(255), nullable=False)

    upload_date = Column(DateTime, default=datetime.utcnow)

    analysis_result = Column(JSON, nullable=False)

    # Relationships
    user = relationship("User", backref="resumes")
    matches = relationship(
        "JobMatch",
        back_populates="resume",
        cascade="all, delete-orphan"
    )
