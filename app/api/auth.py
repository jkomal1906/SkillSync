from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import signup_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    return signup_user(db, data.name, data.email, data.password)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, data.email, data.password)
    return {"access_token": token}
