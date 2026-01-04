from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobPosting(Base):
    __tablename__ = "JobPostings"

    Id = Column(Integer, primary_key=True, index=True)
    JobTitle = Column(String)
    Skills = Column(String)
    JobDescription = Column(String)
