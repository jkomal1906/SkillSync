from pydantic import BaseModel
from datetime import datetime
from typing import List

class JobCreateRequest(BaseModel):    #DTO for creating a job posting
    job_title: str
    skills: List[str]
    description: str

  
class JobResponse(BaseModel):         #DTO for job posting response
    id: int
    job_title: str
    skills: List[str]
    description: str
    posted_date: datetime

    class Config:
        from_attributes = True
