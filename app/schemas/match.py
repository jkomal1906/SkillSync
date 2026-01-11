from pydantic import BaseModel
from typing import List
from datetime import datetime

class JobMatchRequest(BaseModel):
    resume_text: str
    top_n: int = 5

class JobMatchResponse(BaseModel):
    job_id: int
    job_title: str
    skills: List[str]
    description: str
    similarity_score: float


class ResumeMatchHistoryResponse(BaseModel):
    job_id: int
    job_title: str
    skills: List[str]
    description: str
    similarity_score: float
    matched_at: datetime