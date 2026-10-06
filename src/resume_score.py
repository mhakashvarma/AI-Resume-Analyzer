def calculate_resume_score(section_results, contact_results):
    total_points = 0
    earned_points = 0

    section_weights = {
        "Education": 15,
        "Skills": 20,
        "Projects": 20,
        "Experience": 15,
        "Certifications": 10
    }

    contact_weights = {
        "Email": 5,
        "Phone": 5,
        "LinkedIn": 5,
        "GitHub": 5
    }

    for section, weight in section_weights.items():
        total_points += weight

        if section_results.get(section, False):
            earned_points += weight

    for contact, weight in contact_weights.items():
        total_points += weight

        if contact_results.get(contact, False):
            earned_points += weight

    score = (earned_points / total_points) * 100

    return round(score, 2)


def display_resume_score(score):
    print("\nResume Strength Score:")
    print("-" * 40)
    print(f"Score: {score}/100")

    if score >= 80:
        print("Overall assessment: Strong")
    elif score >= 60:
        print("Overall assessment: Good")
    elif score >= 40:
        print("Overall assessment: Needs improvement")
    else:
        print("Overall assessment: Needs significant improvement")


if __name__ == "__main__":
    from resume_parser import extract_resume_text
    from resume_improver import (
        check_resume_sections,
        check_contact_information
    )

    resume_path = "sample_resumes/resume.pdf"

    print("\nCalculating resume strength...")

    resume_text = extract_resume_text(resume_path)

    section_results = check_resume_sections(
        resume_text
    )

    contact_results = check_contact_information(
        resume_text
    )

    score = calculate_resume_score(
        section_results,
        contact_results
    )

    display_resume_score(score)