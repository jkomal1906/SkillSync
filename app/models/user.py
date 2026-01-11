from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    signup_date = Column(DateTime, default=datetime.utcnow)
