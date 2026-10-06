import csv
import re

from src.resume_parser import extract_resume_text


def load_job_roles(file_path):
    job_roles = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            role = row["job_role"].strip()

            required_skills = [
                skill.strip().lower()
                for skill in row["required_skills"].split(",")
            ]

            job_roles.append({
                "job_role": role,
                "required_skills": required_skills
            })

    return job_roles


def load_skills(file_path):
    skills = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            skill = row["skill"].strip().lower()

            skills.append(skill)

    return skills


def find_skills(resume_text, skill_list):
    resume_text = resume_text.lower()

    found_skills = []

    for skill in skill_list:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text):
            found_skills.append(skill)

    return found_skills


def calculate_match_score(resume_skills, required_skills):
    resume_skills = set(skill.lower() for skill in resume_skills)
    required_skills = set(skill.lower() for skill in required_skills)

    matched_skills = resume_skills.intersection(required_skills)

    missing_skills = required_skills - resume_skills

    if len(required_skills) == 0:
        return 0, [], []

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2), sorted(matched_skills), sorted(missing_skills)


def rank_job_roles(resume_skills, job_roles):
    results = []

    for job in job_roles:
        score, matched_skills, missing_skills = calculate_match_score(
            resume_skills,
            job["required_skills"]
        )

        results.append({
            "job_role": job["job_role"],
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results


if __name__ == "__main__":
    resume_path = "sample_resumes/resume.pdf"
    skills_path = "data/skill_dictionary.csv"
    job_roles_path = "data/job_roles.csv"

    print("\nReading resume...")

    resume_text = extract_resume_text(resume_path)

    print("Resume text extracted successfully.")

    skill_list = load_skills(skills_path)

    resume_skills = find_skills(resume_text, skill_list)

    print(f"Detected {len(resume_skills)} skills.")

    print("\nDetected Skills:")

    for skill in resume_skills:
        print(f"- {skill}")

    job_roles = load_job_roles(job_roles_path)

    ranked_roles = rank_job_roles(resume_skills, job_roles)

    print("\nTop 3 Recommended Job Roles:\n")

    for position, role in enumerate(ranked_roles[:3], start=1):
        print(f"{position}. {role['job_role']}")
        print(f"   Match Score: {role['score']}%")
        print(f"   Matched Skills: {role['matched_skills']}")
        print(f"   Missing Skills: {role['missing_skills']}")
        print()