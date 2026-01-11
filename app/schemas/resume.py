from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class ResumeResponse(BaseModel):           #DTO for resume data
    id: int
    file_path: str
    upload_date: datetime
    analysis_result: Dict[str, Any]

    class Config:
        from_attributes = True


class ResumeMatchRequest(BaseModel):  #DTO for resume-job matching request
    resume_text: str
    top_n: int = 5