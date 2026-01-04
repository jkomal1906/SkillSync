# Resume Analyzer Phase 1
A Resume Analyzer web application built using FastAPI and spaCy.
This project allows users to upload resumes (PDF / DOCX) and extract useful information.


## Features of Phase 1
- Upload resume (PDF / DOCX)
- Extract text from resume
- NLP-based analysis using spaCy
- FastAPI backend
- Ready for frontend integration


#Tech Stack
- Python 3.11+
- FastAPI
- spaCy
- pdfminer.six
- docx2txt
- SQLAlchemy
- Uvicorn

# Setup Instructions

# 1.Clone the Repository
bash
git clone <your-repo-url>
cd ResumeAnalyzer

# 2.To create virtual Environment for windows
venv\Scripts\activate

# 2.To create virtual Environment for Mac / Linux
source venv/bin/activate

# 3. To Install Dependencies
pip install -r requirements.txt

# 4. To Install spaCy Language Model
python -m spacy download en_core_web_sm

# 5.To Run the Application
uvicorn app.main:app --reload


# 6. To Access the App

API Base URL: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs

*********************************************************************************************

# Frontend (UI Layer)
The frontend of this project is built using HTML, CSS, and JavaScript and provides a simple, user-friendly interface for uploading resumes and viewing analysis results.


# Frontend Features
Resume upload form (PDF / DOCX)
Client-side validation
API integration using Fetch API
Displays extracted resume data dynamically
Clean and responsive UI using CSS


# Frontend Tech Stack

HTML5 – Structure of the UI
CSS3 – Styling and layout
JavaScript (Vanilla JS) – API calls & dynamic rendering