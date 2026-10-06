import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.resume_parser import extract_resume_text
from src.skill_analyzer import load_skills, find_skills
from src.job_matcher import load_job_roles


def normalize_skill_list(skills):
    """
    Converts different skill formats into a simple list of strings.
    Handles both strings and dictionaries.
    """

    normalized = []

    if not skills:
        return normalized

    for skill in skills:

        if isinstance(skill, dict):

            value = (
                skill.get("skill")
                or skill.get("name")
                or skill.get("Skill")
                or skill.get("skills")
            )

            if value:
                normalized.append(
                    str(value).lower().strip()
                )

        else:
            normalized.append(
                str(skill).lower().strip()
            )

    return normalized


def calculate_skill_match(resume_skills, required_skills):
    """
    Calculates skill match percentage between resume and job role.
    """

    resume_skills = set(
        normalize_skill_list(resume_skills)
    )

    required_skills = set(
        normalize_skill_list(required_skills)
    )

    if not required_skills:
        return 0.0, [], []

    matched_skills = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        required_skills - resume_skills
    )

    score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    return (
        round(score, 2),
        matched_skills,
        missing_skills
    )


def calculate_tfidf_similarity(
    resume_text,
    required_skills
):
    """
    Calculates TF-IDF cosine similarity between
    resume text and required skills.
    """

    if not required_skills:
        return 0.0

    if isinstance(required_skills, list):

        job_text = " ".join(
            str(skill)
            for skill in required_skills
        )

    else:
        job_text = str(required_skills)

    if not job_text.strip():
        return 0.0

    documents = [
        str(resume_text),
        job_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:

        tfidf_matrix = vectorizer.fit_transform(
            documents
        )

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(
            similarity * 100,
            2
        )

    except ValueError:

        return 0.0


def get_job_role_name(job):
    """
    Gets the job role name.
    """

    if isinstance(job, dict):

        return (
            job.get("role")
            or job.get("job_role")
            or job.get("Job Role")
            or job.get("job")
            or job.get("title")
            or job.get("Role")
            or "Unknown Role"
        )

    return str(job)


def get_required_skills(job):
    """
    Gets required skills from a job-role dictionary.
    """

    if isinstance(job, dict):

        skills = (
            job.get("skills")
            or job.get("required_skills")
            or job.get("Required Skills")
            or job.get("required")
            or job.get("Skills")
        )

        if isinstance(skills, str):

            return [
                skill.strip()
                for skill in skills.split(",")
                if skill.strip()
            ]

        return skills or []

    return []


def analyze_resume(resume_path):
    """
    Main resume analysis function.

    Returns:

        resume_skills
        results

    results contains ALL job roles
    sorted by final score.
    """

    print("Analyzing resume...")

    # --------------------------------------------------
    # 1. Extract resume text
    # --------------------------------------------------

    resume_text = extract_resume_text(
        resume_path
    )

    # --------------------------------------------------
    # 2. Load skill dictionary
    # --------------------------------------------------

    skill_data = load_skills(
        "data/skill_dictionary.csv"
    )

    detected_skills = find_skills(
        resume_text,
        skill_data
    )

    # Convert detected skills into strings
    resume_skills = normalize_skill_list(
        detected_skills
    )

    # --------------------------------------------------
    # 3. Load ALL job roles
    # --------------------------------------------------

    job_roles = load_job_roles(
        "data/job_roles.csv"
    )

    results = []

    # --------------------------------------------------
    # 4. Analyze EVERY job role
    # --------------------------------------------------

    for job in job_roles:

        role_name = get_job_role_name(
            job
        )

        required_skills = get_required_skills(
            job
        )

        # ----------------------------------------------
        # Skill Match
        # ----------------------------------------------

        skill_score, matched_skills, missing_skills = calculate_skill_match(
            resume_skills,
            required_skills
        )

        # ----------------------------------------------
        # TF-IDF Similarity
        # ----------------------------------------------

        tfidf_score = calculate_tfidf_similarity(
            resume_text,
            required_skills
        )

        # ----------------------------------------------
        # Final Match Score
        #
        # Skill Match = 70%
        # TF-IDF      = 30%
        # ----------------------------------------------

        final_score = (
            (skill_score * 0.70)
            +
            (tfidf_score * 0.30)
        )

        results.append({

            "role": role_name,

            "skill_score": round(
                skill_score,
                2
            ),

            "tfidf_score": round(
                tfidf_score,
                2
            ),

            "final_score": round(
                final_score,
                2
            ),

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills
        })

    # --------------------------------------------------
    # 5. Sort ALL job roles
    # --------------------------------------------------

    results = sorted(
        results,
        key=lambda x: x["final_score"],
        reverse=True
    )

    # --------------------------------------------------
    # 6. Add ranking
    # --------------------------------------------------

    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index

    # --------------------------------------------------
    # 7. Display ALL job roles
    # --------------------------------------------------

    print("\nAll Job Role Analysis:")
    print("-" * 60)

    for result in results:

        print(
            f"{result['rank']}. "
            f"{result['role']} "
            f"- {result['final_score']:.2f}%"
        )

    # --------------------------------------------------
    # 8. Display TOP 3
    # --------------------------------------------------

    print("\nTop 3 Recommended Job Roles:")
    print("-" * 60)

    for result in results[:3]:

        print(
            f"\n{result['rank']}. "
            f"{result['role']}"
        )

        print(
            f"   Skill Match: "
            f"{result['skill_score']:.2f}%"
        )

        print(
            f"   TF-IDF Similarity: "
            f"{result['tfidf_score']:.2f}%"
        )

        print(
            f"   Final Match Score: "
            f"{result['final_score']:.2f}%"
        )

        print(
            f"   Matched Skills: "
            f"{result['matched_skills']}"
        )

        print(
            f"   Missing Skills: "
            f"{result['missing_skills']}"
        )

    return resume_skills, results


if __name__ == "__main__":

    resume_path = os.path.join(
        "sample_resumes",
        "resume.pdf"
    )

    resume_skills, results = analyze_resume(
        resume_path
    )