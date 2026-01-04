import docx2txt
from pdfminer.high_level import extract_text
import spacy
import re
import tempfile
from fastapi import UploadFile

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python", "fastapi", "sql", "sql server", "c#", ".net",
    "api", "rest", "microservices", "dto", "dal", "bal",
    "html", "css", "javascript", "react", "angular",
    "n-tier", "entity framework"
]

EDUCATION_KEYWORDS = [
    "bachelor", "master", "b.sc", "m.sc", "btech", "mtech",
    "mba", "phd", "high school", "diploma"
]

def extract_text_from_file(file) -> str:
    """
    Extract clean text from PDF or DOCX without destroying content.
    """

    # Save UploadFile to temp file
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

    # -----------------------------
    # ✅ SAFE NORMALIZATION
    # -----------------------------

    # Normalize whitespace (but keep content)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)

    # Remove only exact unwanted phrases (NOT whole sentences)
    UNWANTED_PHRASES = [
        "user interface",
        "currently pursuing",
        "focus on backend development",
        "api engineering"
    ]

    for phrase in UNWANTED_PHRASES:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)

    return text.strip()


def extract_skills(text: str):
    text_lower = text.lower()
    skills = set()

    for skill in SKILL_KEYWORDS:
        pattern = rf"\b{re.escape(skill.lower())}\b"
        if re.search(pattern, text_lower):
            skills.add(skill.lower())

    # Sorted, title-cased for UI
    return sorted({s.strip() for s in skills})


def extract_education(text: str):
    education_found = set()
    lines = text.splitlines()

    STOP_WORDS = ["experience", "professional"]

    for i, line in enumerate(lines):
        line_lower = line.lower()

        if any(edu in line_lower for edu in EDUCATION_KEYWORDS):

            # Ignore section headings
            if any(stop in line_lower for stop in STOP_WORDS):
                continue

            combined = line.strip()

            for j in range(1, 3):
                if i + j < len(lines):
                    next_line = lines[i + j].strip()
                    next_lower = next_line.lower()

                    # Stop at Experience section
                    if any(stop in next_lower for stop in STOP_WORDS):
                        break

                    if len(next_line.split()) > 15:
                        break

                    combined += " " + next_line

            # Remove years only
            combined = re.sub(r'\b(19\d{2}|20\d{2})\b', '', combined)
            combined = re.sub(r'\s+', ' ', combined).strip()

            # Must contain alphabet (institution)
            if re.search(r'[a-zA-Z]', combined):
                education_found.add(combined)

    return list(education_found)


def extract_experience(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    experience = []

    year_pattern = r'(19\d{2}|20\d{2})\s*[-–]\s*(19\d{2}|20\d{2})'

    EDUCATION_NOISE = [
        "school", "college", "university", "degree",
        "bachelor", "master", "msc", "bsc"
    ]

    in_experience_section = False
    current_company = None

    for line in lines:
        line_lower = line.lower()

        # Detect start of experience section
        if "experience" in line_lower:
            in_experience_section = True
            continue

        # Stop if education starts again
        if in_experience_section and "education" in line_lower:
            break

        if not in_experience_section:
            continue

        # Reject education/institution lines
        if any(word in line_lower for word in EDUCATION_NOISE):
            continue

        # Candidate company name
        if re.search(r'[a-zA-Z]', line) and len(line.split()) <= 7:
            current_company = line

        # Year detection
        match = re.search(year_pattern, line)
        if match and current_company:
            years = f"{match.group(1)}-{match.group(2)}"

            # Reject percentages & numeric junk
            if '%' in current_company or re.search(r'\d', current_company):
                continue

            experience.append(f"{current_company} ({years})")
            current_company = None

    return " | ".join(sorted(set(experience)))


def parse_resume(file) -> dict:
    text = extract_text_from_file(file)
    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
