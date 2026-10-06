from final_matcher import analyze_resume


def analyze_skill_gap(missing_skills):
    if not missing_skills:
        return [
            "You already have all the required skills for this role."
        ]

    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Consider learning {skill} to improve your suitability for this role."
        )

    return recommendations


def display_skill_gap(job_role, missing_skills):
    print(f"\nSkill Gap Analysis for {job_role}")
    print("-" * 40)

    if not missing_skills:
        print("- You already have all the required skills for this role.")
        return

    print("Skills to improve:")

    for skill in missing_skills:
        print(f"- {skill}")

    print("\nLearning Recommendations:")

    recommendations = analyze_skill_gap(missing_skills)

    for recommendation in recommendations:
        print(f"- {recommendation}")


if __name__ == "__main__":
    resume_path = "sample_resumes/resume.pdf"
    skills_path = "data/skill_dictionary.csv"
    job_roles_path = "data/job_roles.csv"

    print("\nAnalyzing resume for skill gaps...")

    resume_skills, results = analyze_resume(
        resume_path,
        skills_path,
        job_roles_path
    )

    print("\nTop 3 Recommended Roles and Skill Gaps:\n")

    for position, result in enumerate(results[:3], start=1):
        print(f"{position}. {result['job_role']}")
        print(f"Final Match Score: {result['final_score']}%")

        display_skill_gap(
            result["job_role"],
            result["missing_skills"]
        )

        print()