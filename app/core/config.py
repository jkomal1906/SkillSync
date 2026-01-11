from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SkillSync"
    SECRET_KEY: str = "super-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()

DATABASE_URL = (
    "mssql+pyodbc://LAPTOP-NE96B3JP\\SQLEXPRESS/SkillSyncDB"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

UPLOAD_DIR = "uploads"
