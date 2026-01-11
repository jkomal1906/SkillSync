import docx2txt
from pdfminer.high_level import extract_text
import spacy
import re
import tempfile
from fastapi import UploadFile
from datetime import datetime

# Load English NLP model
nlp = spacy.load("en_core_web_sm")


# SKILL & EDUCATION KEYWORDS

SKILL_KEYWORDS = [
    "python", "fastapi", "sql", "sql server", "c#", ".net",
    "api", "rest", "microservices", "dto", "dal", "bal",
    "html", "css", "javascript", "react", "angular",
    "n-tier", "entity framework", "docker", "azure", "aws"
]

EDUCATION_KEYWORDS = [
    "bachelor", "master", "b.sc", "m.sc", "btech", "mtech",
    "mba", "phd", "high school", "diploma"
]

EXPERIENCE_SECTION_KEYWORDS = [
    "experience", "employment", "work history"
]



# TEXT EXTRACTION

def extract_text_from_file(file) -> str:
    """
    Extract clean text from PDF or DOCX without destroying structure.
    """

    if isinstance(file, UploadFile):
        suffix = "." + file.filename.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.file.read())
            file_path = tmp.name
    else:
        file_path = file

    ext = file_path.lower().split(".")[-1]

    if ext == "pdf":
        text = extract_text(file_path)
    elif ext == "docx":
        text = docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")

    # Normalize whitespace safely
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)

    # Remove known noise phrases only
    UNWANTED_PHRASES = [
        "user interface",
        "currently pursuing",
        "focus on backend development",
        "api engineering"
    ]

    for phrase in UNWANTED_PHRASES:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)

    return text.strip()


# SKILLS EXTRACTION

def extract_skills(text: str):
    text_lower = text.lower()
    skills = set()

    for skill in SKILL_KEYWORDS:
        pattern = rf"\b{re.escape(skill.lower())}\b"
        if re.search(pattern, text_lower):
            skills.add(skill.lower())

    return sorted(skills)


# EDUCATION EXTRACTION

def extract_education(text: str):
    education_found = set()
    lines = text.splitlines()

    STOP_WORDS = ["experience", "professional"]

    for i, line in enumerate(lines):
        line_lower = line.lower()

        if any(edu in line_lower for edu in EDUCATION_KEYWORDS):

            if any(stop in line_lower for stop in STOP_WORDS):
                continue

            combined = line.strip()

            for j in range(1, 3):
                if i + j < len(lines):
                    next_line = lines[i + j].strip()
                    next_lower = next_line.lower()

                    if any(stop in next_lower for stop in STOP_WORDS):
                        break

                    if len(next_line.split()) > 15:
                        break

                    combined += " " + next_line

            combined = re.sub(r'\b(19\d{2}|20\d{2})\b', '', combined)
            combined = re.sub(r'\s+', ' ', combined).strip()

            if re.search(r'[a-zA-Z]', combined):
                education_found.add(combined)

    return list(education_found)


# EXPERIENCE DETAILS EXTRACTION

def extract_experience(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    experience_entries = []

    year_pattern = r'(19\d{2}|20\d{2})\s*[-–]\s*(19\d{2}|20\d{2})'
    in_experience_section = False
    current_company = None

    for line in lines:
        line_lower = line.lower()

        if any(k in line_lower for k in EXPERIENCE_SECTION_KEYWORDS):
            in_experience_section = True
            continue

        if in_experience_section and "education" in line_lower:
            break

        if not in_experience_section:
            continue

        if re.search(r'[a-zA-Z]', line) and len(line.split()) <= 7:
            current_company = line

        match = re.search(year_pattern, line)
        if match and current_company:
            start, end = match.group(1), match.group(2)
            experience_entries.append({
                "company": current_company,
                "duration": f"{start}-{end}"
            })
            current_company = None

    return experience_entries


# JOB TITLES (NLP)

def extract_job_titles(text: str):
    doc = nlp(text)
    titles = set()

    for ent in doc.ents:
        if ent.label_ == "ORG":
            if len(ent.text.split()) <= 4:
                titles.add(ent.text)

    return list(titles)


# EXPERIENCE YEARS CALCULATION

def calculate_total_experience(experience_entries):
    total_years = 0

    for exp in experience_entries:
        try:
            start, end = exp["duration"].split("-")
            total_years += int(end) - int(start)
        except:
            continue

    return total_years


# MAIN PARSER (PHASE-2 READY)

def parse_resume(file) -> dict:
    text = extract_text_from_file(file)

    skills = extract_skills(text)
    education = extract_education(text)
    experience_entries = extract_experience(text)
    job_titles = extract_job_titles(text)
    total_experience_years = calculate_total_experience(experience_entries)

    return {
        "skills": skills,
        "education": education,
        "experience": experience_entries,
        "job_titles": job_titles,
        "total_experience_years": total_experience_years,
        "parsed_at": datetime.utcnow().isoformat()
    }
