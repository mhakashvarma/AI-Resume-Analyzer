import re

from src.resume_parser import extract_resume_text


# ============================================================
# 1. CHECK RESUME SECTIONS
# ============================================================

def check_resume_sections(resume_text):
    text = str(resume_text).lower()

    sections = {
        "Education": [
            "education",
            "academic"
        ],
        "Skills": [
            "skills",
            "technical skills"
        ],
        "Projects": [
            "projects",
            "project"
        ],
        "Experience": [
            "experience",
            "work experience",
            "internship"
        ],
        "Certifications": [
            "certifications",
            "certification"
        ]
    }

    results = {}

    for section, keywords in sections.items():
        found = any(keyword in text for keyword in keywords)
        results[section] = found

    return results


# ============================================================
# 2. CHECK CONTACT INFORMATION
# ============================================================

def check_contact_information(resume_text):

    text = str(resume_text)
    lower_text = text.lower()

    contact_results = {}

    # --------------------------------------------------------
    # EMAIL DETECTION
    # --------------------------------------------------------

    # Normal email format:
    # example@gmail.com

    normal_email_pattern = (
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    # Some PDF files remove the @ symbol while extracting text.
    #
    # Example extracted from your PDF:
    # akash.varma gmail.com
    #
    # This pattern detects that format too.

    broken_email_pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"\s+"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    email_found = (
        re.search(normal_email_pattern, text) is not None
        or
        re.search(broken_email_pattern, text) is not None
    )

    contact_results["Email"] = email_found

    # --------------------------------------------------------
    # PHONE NUMBER DETECTION
    # --------------------------------------------------------

    # Supports:
    # +919876543210
    # +91 9876543210
    # +91-9876543210
    # 9876543210

    phone_patterns = [
        r"\+91[\s-]?[6-9]\d{9}",
        r"\b[6-9]\d{9}\b"
    ]

    phone_found = False

    for pattern in phone_patterns:
        if re.search(pattern, text):
            phone_found = True
            break

    contact_results["Phone"] = phone_found

    # --------------------------------------------------------
    # LINKEDIN DETECTION
    # --------------------------------------------------------

    linkedin_found = (
        "linkedin.com" in lower_text
        or "www.linkedin.com" in lower_text
        or "linkedin" in lower_text
    )

    contact_results["LinkedIn"] = linkedin_found

    # --------------------------------------------------------
    # GITHUB DETECTION
    # --------------------------------------------------------

    github_found = (
        "github.com" in lower_text
        or "www.github.com" in lower_text
        or "github" in lower_text
    )

    contact_results["GitHub"] = github_found

    return contact_results


# ============================================================
# 3. GENERATE IMPROVEMENT SUGGESTIONS
# ============================================================

def generate_improvement_suggestions(
    section_results,
    contact_results
):

    suggestions = []

    # --------------------------------------------------------
    # MISSING RESUME SECTIONS
    # --------------------------------------------------------

    for section, found in section_results.items():

        if not found:

            if section == "Experience":
                suggestions.append(
                    "Consider adding an Experience section if you have relevant experience."
                )

            elif section == "Certifications":
                suggestions.append(
                    "Consider adding relevant certifications if you have completed any."
                )

            elif section == "Education":
                suggestions.append(
                    "Add an Education section with your degree and institution."
                )

            elif section == "Skills":
                suggestions.append(
                    "Add a Skills section listing your technical and professional skills."
                )

            elif section == "Projects":
                suggestions.append(
                    "Add a Projects section highlighting your technical projects."
                )

    # --------------------------------------------------------
    # MISSING CONTACT INFORMATION
    # --------------------------------------------------------

    if not contact_results.get("Email", False):
        suggestions.append(
            "Add a professional email address to your resume."
        )

    if not contact_results.get("Phone", False):
        suggestions.append(
            "Add a phone number if it is appropriate for your resume."
        )

    if not contact_results.get("LinkedIn", False):
        suggestions.append(
            "Consider adding your LinkedIn profile."
        )

    if not contact_results.get("GitHub", False):
        suggestions.append(
            "Consider adding your GitHub profile, especially for technical roles."
        )

    return suggestions


# ============================================================
# 4. DISPLAY RESUME ANALYSIS
# ============================================================

def display_resume_analysis(
    section_results,
    contact_results,
    suggestions
):

    print("\nResume Section Analysis:")
    print("-" * 40)

    for section, found in section_results.items():

        if found:
            print(f"✓ {section} section found")
        else:
            print(f"✗ {section} section not detected")

    print("\nContact Information:")
    print("-" * 40)

    for item, found in contact_results.items():

        if found:
            print(f"✓ {item} found")
        else:
            print(f"✗ {item} not detected")

    print("\nResume Improvement Suggestions:")
    print("-" * 40)

    if suggestions:

        for suggestion in suggestions:
            print(f"- {suggestion}")

    else:
        print("- No major improvements detected.")


# ============================================================
# 5. RUN RESUME ANALYSIS
# ============================================================

if __name__ == "__main__":

    resume_path = "sample_resumes/resume.pdf"

    print("\nAnalyzing resume...")

    # Extract text from PDF
    resume_text = extract_resume_text(resume_path)

    # --------------------------------------------------------
    # TEMPORARY DEBUG OUTPUT
    # --------------------------------------------------------
    # This lets us see exactly what the PDF extractor reads.
    # We can remove this later once everything is confirmed.



    # Check resume sections
    section_results = check_resume_sections(
        resume_text
    )

    # Check contact information
    contact_results = check_contact_information(
        resume_text
    )

    # Generate suggestions
    suggestions = generate_improvement_suggestions(
        section_results,
        contact_results
    )

    # Display results
    display_resume_analysis(
        section_results,
        contact_results,
        suggestions
    )