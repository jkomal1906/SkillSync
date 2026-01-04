def match_jobs(resume_skills, jobs):
    resume_skills_set = set([s.lower().strip() for s in resume_skills])
    matches = []

    for job in jobs:
        job_skills_set = set([s.strip().lower() for s in job.Skills.split(",")])
        overlap = resume_skills_set & job_skills_set
        score = len(overlap)
        if score > 0:
            matches.append({
                "job_title": job.JobTitle,
                "match_score": score,
                "matched_skills": list(overlap)
            })
    return sorted(matches, key=lambda x: x["match_score"], reverse=True)
