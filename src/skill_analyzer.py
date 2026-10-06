import csv
import re


def load_skills(file_path):
    skills = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            skill = row["skill"].strip().lower()
            category = row["category"].strip()

            skills.append({
                "skill": skill,
                "category": category
            })

    return skills


def find_skills(resume_text, skill_list):
    resume_text = resume_text.lower()

    found_skills = []

    for skill_info in skill_list:
        skill = skill_info["skill"]

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, resume_text):
            found_skills.append(skill_info)

    return found_skills


def group_skills_by_category(found_skills):
    grouped_skills = {}

    for skill_info in found_skills:
        category = skill_info["category"]
        skill = skill_info["skill"]

        if category not in grouped_skills:
            grouped_skills[category] = []

        grouped_skills[category].append(skill)

    return grouped_skills


if __name__ == "__main__":
    from resume_parser import extract_resume_text

    resume_path = "sample_resumes/resume.pdf"
    skills_path = "data/skill_dictionary.csv"

    resume_text = extract_resume_text(resume_path)

    skill_list = load_skills(skills_path)

    found_skills = find_skills(resume_text, skill_list)

    grouped_skills = group_skills_by_category(found_skills)

    print("\nSkills found in your resume:")

    for category, skills in grouped_skills.items():
        print(f"\n{category}:")

        for skill in skills:
            print(f"- {skill}")