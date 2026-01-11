from typing import List, Dict
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.job_match import JobMatch
from typing import List, Dict
from app.models.job_posting import JobPosting as Job  # import your Job model
from app.models.resume import Resume


# ----- Load embedding model once -----
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------- Embedding & Similarity Utilities ----------
def embed(text: str):
    """Generate vector embedding for a given text"""
    if not text:
        return None
    return model.encode([text])[0]


def similarity(vec1, vec2):
    """Compute cosine similarity between two embeddings"""
    if vec1 is None or vec2 is None:
        return 0.0
    return cosine_similarity([vec1], [vec2])[0][0]


# ---------- Job Matching Logic ----------
def match_resume_with_jobs(
    resume_data: Dict,
    jobs: List[Job],  # now Python knows Job
    top_n: int = 5,
    threshold: float = 0.6
) -> List[Dict]:
    """
    Match a resume against available jobs and return top N matches above threshold.

    resume_data format:
    {
        "skills": [...],
        "experience": "...",
        "education": "..."
    }
    """
    # Combine resume sections
    resume_skills_text = " ".join(resume_data.get("skills", []))
    resume_experience_text = resume_data.get("experience", "")
    resume_education_text = resume_data.get("education", "")

    # Create embeddings
    resume_skill_emb = embed(resume_skills_text)
    resume_exp_emb = embed(resume_experience_text)
    resume_edu_emb = embed(resume_education_text)

    matched_jobs = []

    for job in jobs:
        job_skill_emb = embed(job.skills)
        job_desc_emb = embed(job.description)

        # Weighted similarity calculation
        skill_score = similarity(resume_skill_emb, job_skill_emb)
        experience_score = similarity(resume_exp_emb, job_desc_emb)
        education_score = similarity(resume_edu_emb, job_desc_emb)

        final_score = skill_score * 0.5 + experience_score * 0.3 + education_score * 0.2

        if final_score >= threshold:
            matched_jobs.append({
                "job_id": job.id,
                "job_title": job.job_title,
                "skills": job.skills.split(","),
                "description": job.description,
                "similarity_score": round(float(final_score), 4)
            })

    # Sort matches by descending similarity
    matched_jobs.sort(key=lambda x: x["similarity_score"], reverse=True)

    return matched_jobs[:top_n]


# ---------- Save Matches to Database ----------
def save_job_matches(
    db: Session,
    resume_id: int,
    matched_jobs: List[Dict]
):
    """
    Save top N job matches to JobMatch table
    matched_jobs = [
        {"job_id": 1, "similarity_score": 0.82},
        ...
    ]
    """
    matches = []
    for job in matched_jobs:
        match = JobMatch(
            resume_id=resume_id,
            job_id=job["job_id"],
            similarity_score=job["similarity_score"]
        )
        matches.append(match)

    db.add_all(matches)
    db.commit()


# ---------- Full Pipeline Function ----------
def match_and_store(
    db: Session,
    resume_id: int,
    resume_data: Dict,
    top_n: int = 5,
    threshold: float = 0.6
) -> List[Dict]:
    """
    Match a resume to jobs and store top matches in DB
    Returns the list of matched jobs
    """
    # Fetch all jobs from DB
    jobs = db.query(Job).all()

    # Step 1: Compute top matches
    matched_jobs = match_resume_with_jobs(resume_data, jobs, top_n, threshold)

    # Step 2: Save matches to DB
    save_job_matches(db, resume_id, matched_jobs)

    return matched_jobs



#---------- Retrieve Match History ----------
def get_match_history(
    db: Session,
    resume_id: int
) -> List[Dict]:
    matches = (
        db.query(JobMatch)
        .filter(JobMatch.resume_id == resume_id)
        .order_by(JobMatch.created_at.desc())
        .all()
    )

    history = []
    for m in matches:
        history.append({
            "job_id": m.job.id,
            "job_title": m.job.job_title,
            "skills": m.job.skills.split(","),
            "description": m.job.description,
            "similarity_score": m.similarity_score,
            "matched_at": m.created_at
        })

    return history
