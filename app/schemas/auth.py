from pydantic import BaseModel, EmailStr   #DTOs for auth APIs

class SignupRequest(BaseModel):             #DTO for signup request
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):               #DTO for login request
    email: EmailStr
    password: str


class TokenResponse(BaseModel):               #DTO for token response
    access_token: str
    token_type: str = "bearer"
