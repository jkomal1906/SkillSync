import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads/resumes"                       #Directory to store uploaded resumes

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_resume_file(file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
