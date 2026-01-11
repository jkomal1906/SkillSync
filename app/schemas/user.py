from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):   #DTO for user data
    id: int
    name: str
    email: EmailStr
    signup_date: datetime

    class Config:
        from_attributes = True
