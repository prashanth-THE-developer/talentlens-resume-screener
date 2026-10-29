
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def text_similarity(resume: str, jd: str) -> float:
    # Check whether resume or job description is empty
    if not resume.strip() or not jd.strip():
        return 0.0

    # Convert both texts into numerical TF-IDF vectors
    vec = TfidfVectorizer(stop_words="english")
    tfidf = vec.fit_transform([resume, jd])

    # Calculate similarity between the two text vectors
    return float(cosine_similarity(tfidf[0], tfidf[1])[0][0])


def final_score(resume, jd, resume_skills, jd_skills) -> float:
    # Calculate text similarity
    sim = text_similarity(resume, jd)

    # Calculate the percentage of job skills found in the resume
    overlap = len(resume_skills & jd_skills) / max(len(jd_skills), 1)

    # Give 40% weight to text similarity and 60% to skill matching
    return round((0.4 * sim + 0.6 * overlap) * 100, 1)
