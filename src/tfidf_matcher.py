from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_parser import extract_resume_text
from job_matcher import load_job_roles


def calculate_similarity(resume_text, job_text):
    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def create_job_text(job):
    required_skills = ", ".join(job["required_skills"])

    return f"{job['job_role']} requires the following skills: {required_skills}."


if __name__ == "__main__":
    resume_path = "sample_resumes/resume.pdf"
    job_roles_path = "data/job_roles.csv"

    print("\nReading resume...")

    resume_text = extract_resume_text(resume_path)

    print("Resume text extracted successfully.")

    job_roles = load_job_roles(job_roles_path)

    print("\nTF-IDF Similarity Scores:\n")

    results = []

    for job in job_roles:
        job_text = create_job_text(job)

        score = calculate_similarity(
            resume_text,
            job_text
        )

        results.append({
            "job_role": job["job_role"],
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    for position, result in enumerate(results, start=1):
        print(
            f"{position}. "
            f"{result['job_role']}: "
            f"{result['score']}%"
        )