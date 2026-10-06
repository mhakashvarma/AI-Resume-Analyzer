import os
import tempfile
import pandas as pd
import streamlit as st

from src.final_matcher import analyze_resume
from src.resume_parser import extract_resume_text
from src.resume_improver import (
    check_resume_sections,
    check_contact_information,
    generate_improvement_suggestions
)
from src.resume_score import calculate_resume_score


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #555;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        margin-top: 35px;
        margin-bottom: 20px;
    }

    .skill-category {
        font-size: 18px;
        margin-bottom: 18px;
        line-height: 1.6;
    }

    .skill-category-name {
        font-weight: 700;
    }

    .skill-list {
        font-weight: 400;
    }

    .role-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .role-score {
        font-size: 18px;
        margin-bottom: 20px;
    }

    .small-label {
        font-size: 16px;
        color: #555;
        margin-bottom: 5px;
    }

    .score-number {
        font-size: 30px;
        font-weight: 600;
    }

    .matched {
        color: #16803c;
        font-weight: 600;
    }

    .missing {
        color: #c62828;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_skill(skill):
    """Convert a skill into a clean lowercase string."""

    if isinstance(skill, dict):
        value = (
            skill.get("skill")
            or skill.get("name")
            or skill.get("Skill")
            or skill.get("skills")
            or ""
        )
        return str(value).strip().lower()

    return str(skill).strip().lower()


def get_role_name(result):
    """
    final_matcher.py returns the role using the key 'role'.
    This function also supports older formats.
    """

    if not isinstance(result, dict):
        return str(result)

    return (
        result.get("role")
        or result.get("job_role")
        or result.get("title")
        or "Unknown Role"
    )


def get_skill_list(result, key):
    """Safely get matched or missing skills."""

    if not isinstance(result, dict):
        return []

    skills = result.get(key, [])

    if skills is None:
        return []

    if isinstance(skills, str):
        return [
            item.strip()
            for item in skills.split(",")
            if item.strip()
        ]

    return [
        normalize_skill(skill)
        for skill in skills
        if normalize_skill(skill)
    ]


def categorize_skills(resume_skills):
    """
    Organize detected skills into categories.

    This matches the categories shown in the UI:
    Programming
    Web Development
    Database
    Data Science
    AI/ML
    Tools
    """

    categories = {
        "Programming": [],
        "Web Development": [],
        "Database": [],
        "Data Science": [],
        "AI/ML": [],
        "Tools": [],
        "Other": []
    }

    category_mapping = {

        # Programming
        "python": "Programming",
        "java": "Programming",
        "c": "Programming",
        "c++": "Programming",
        "c#": "Programming",
        "javascript": "Programming",
        "typescript": "Programming",

        # Web Development
        "html": "Web Development",
        "css": "Web Development",
        "javascript": "Web Development",
        "react": "Web Development",
        "node.js": "Web Development",
        "node": "Web Development",
        "django": "Web Development",
        "flask": "Web Development",
        "fastapi": "Web Development",

        # Database
        "sql": "Database",
        "mysql": "Database",
        "mongodb": "Database",
        "postgresql": "Database",
        "oracle": "Database",

        # Data Science
        "pandas": "Data Science",
        "numpy": "Data Science",
        "matplotlib": "Data Science",
        "seaborn": "Data Science",
        "scipy": "Data Science",
        "statistics": "Data Science",
        "excel": "Data Science",
        "power bi": "Data Science",

        # AI / ML
        "machine learning": "AI/ML",
        "deep learning": "AI/ML",
        "scikit-learn": "AI/ML",
        "tensorflow": "AI/ML",
        "pytorch": "AI/ML",
        "nlp": "AI/ML",
        "transformers": "AI/ML",
        "hugging face": "AI/ML",
        "llm": "AI/ML",
        "rag": "AI/ML",
        "opencv": "AI/ML",
        "computer vision": "AI/ML",

        # Tools
        "git": "Tools",
        "github": "Tools",
        "docker": "Tools",
        "aws": "Tools",
        "azure": "Tools",
        "streamlit": "Tools",
        "jira": "Tools"
    }

    for skill in resume_skills:

        skill = normalize_skill(skill)

        if not skill:
            continue

        category = category_mapping.get(
            skill,
            "Other"
        )

        categories[category].append(skill)

    return categories


def display_role_card(result, position, show_rank=True):
    """Display one job role in a clean Streamlit card."""

    role_name = get_role_name(result)

    skill_score = result.get(
        "skill_score",
        0
    )

    tfidf_score = result.get(
        "tfidf_score",
        0
    )

    final_score = result.get(
        "final_score",
        0
    )

    matched_skills = get_skill_list(
        result,
        "matched_skills"
    )

    missing_skills = get_skill_list(
        result,
        "missing_skills"
    )

    with st.container(border=True):

        if show_rank:
            st.markdown(
                f"""
                <div class="role-title">
                    {position}. {role_name}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="role-title">
                    {role_name}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div class="role-score">
                Final Match Score:
                <strong>{final_score:.2f}%</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Skill Match",
                f"{skill_score:.2f}%"
            )

        with col2:
            st.metric(
                "TF-IDF Similarity",
                f"{tfidf_score:.2f}%"
            )

        with col3:
            st.metric(
                "Final Match Score",
                f"{final_score:.2f}%"
            )

        st.markdown("**Matched Skills**")

        if matched_skills:
            st.markdown(
                f"""
                <div class="matched">
                    {", ".join(matched_skills)}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write("No matching skills found.")

        st.markdown("**Missing Skills**")

        if missing_skills:
            st.markdown(
                f"""
                <div class="missing">
                    {", ".join(missing_skills)}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write("No major missing skills.")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Upload your resume to analyze your skills and find the most suitable career roles.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# FILE UPLOAD
# ============================================================

st.subheader("📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your PDF resume to start the analysis.",
    type=["pdf"],
    help="Upload a PDF resume."
)


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True
    ):

        resume_path = None

        try:

            # ------------------------------------------------
            # CREATE TEMPORARY PDF
            # ------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                resume_path = temp_file.name

            # ------------------------------------------------
            # ANALYZE RESUME
            #
            # IMPORTANT:
            # Your current final_matcher.py accepts ONLY:
            #
            # analyze_resume(resume_path)
            # ------------------------------------------------

            with st.spinner(
                "Analyzing your resume..."
            ):

                resume_skills, results = analyze_resume(
                    resume_path
                )

            # ------------------------------------------------
            # NORMALIZE SKILLS
            # ------------------------------------------------

            resume_skills = [
                normalize_skill(skill)
                for skill in resume_skills
                if normalize_skill(skill)
            ]

            # Remove duplicate skills
            resume_skills = list(
                dict.fromkeys(resume_skills)
            )

            # ------------------------------------------------
            # EXTRACT RESUME TEXT
            # ------------------------------------------------

            resume_text = extract_resume_text(
                resume_path
            )

            # ------------------------------------------------
            # RESUME SECTION ANALYSIS
            # ------------------------------------------------

            section_results = check_resume_sections(
                resume_text
            )

            # ------------------------------------------------
            # CONTACT INFORMATION
            # ------------------------------------------------

            contact_results = check_contact_information(
                resume_text
            )

            # ------------------------------------------------
            # IMPROVEMENT SUGGESTIONS
            # ------------------------------------------------

            suggestions = generate_improvement_suggestions(
                section_results,
                contact_results
            )

            # ------------------------------------------------
            # RESUME SCORE
            # ------------------------------------------------

            resume_score = calculate_resume_score(
                section_results,
                contact_results
            )

            # ------------------------------------------------
            # SORT RESULTS
            #
            # This guarantees:
            # ALL ROLES first
            # TOP 3 calculated from ALL roles
            # ------------------------------------------------

            results = sorted(
                results,
                key=lambda x: float(
                    x.get("final_score", 0)
                ),
                reverse=True
            )

            # =================================================
            # RESULTS HEADER
            # =================================================

            st.divider()

            st.header(
                "📊 Resume Analysis Results"
            )

            # =================================================
            # SUMMARY METRICS
            # =================================================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Resume Strength",
                    f"{resume_score}/100"
                )

            with col2:

                st.metric(
                    "Detected Skills",
                    len(resume_skills)
                )

            with col3:

                st.metric(
                    "Available Job Roles",
                    len(results)
                )

            # =================================================
            # DETECTED SKILLS
            # =================================================

            st.markdown(
                '<div class="section-title">🧠 Detected Skills</div>',
                unsafe_allow_html=True
            )

            if resume_skills:

                categorized_skills = categorize_skills(
                    resume_skills
                )

                for category, skills in categorized_skills.items():

                    if skills:

                        skills_text = ", ".join(
                            skills
                        )

                        st.markdown(
                            f"""
                            <div class="skill-category">
                                <span class="skill-category-name">
                                    {category}:
                                </span>
                                <span class="skill-list">
                                    {skills_text}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.warning(
                    "No skills were detected from the resume."
                )

            # =================================================
            # ALL AVAILABLE JOB ROLES
            # =================================================

            st.markdown(
                '<div class="section-title">💼 All Available Job Roles</div>',
                unsafe_allow_html=True
            )

            st.write(
                f"""
                Analysis completed for **{len(results)} job roles**.
                The roles below are ranked according to their final match score.
                """
            )

            # -------------------------------------------------
            # SHOW ALL ROLES
            # -------------------------------------------------

            for position, result in enumerate(
                results,
                start=1
            ):

                display_role_card(
                    result,
                    position,
                    show_rank=True
                )

            # =================================================
            # TOP 3 RECOMMENDATIONS
            # =================================================

            st.markdown(
                '<div class="section-title">🏆 Top 3 Job Recommendations</div>',
                unsafe_allow_html=True
            )

            st.write(
                """
                Based on the analysis of all available job roles,
                these are the three roles with the highest final match scores.
                """
            )

            top_3 = results[:3]

            for position, result in enumerate(
                top_3,
                start=1
            ):

                display_role_card(
                    result,
                    position,
                    show_rank=True
                )

            # =================================================
            # SKILL GAP ANALYSIS
            # =================================================

            st.markdown(
                '<div class="section-title">📚 Skill Gap Analysis</div>',
                unsafe_allow_html=True
            )

            st.write(
                """
                The following missing skills can help improve your suitability
                for the recommended roles.
                """
            )

            for result in top_3:

                role_name = get_role_name(
                    result
                )

                missing_skills = get_skill_list(
                    result,
                    "missing_skills"
                )

                with st.expander(
                    f"📌 {role_name}"
                ):

                    if missing_skills:

                        for skill in missing_skills:

                            st.write(
                                f"🔹 **{skill}** — "
                                f"Consider learning {skill} "
                                f"to improve your suitability "
                                f"for {role_name}."
                            )

                    else:

                        st.success(
                            "No major skill gaps detected."
                        )

            # =================================================
            # RESUME SECTION ANALYSIS
            # =================================================

            st.markdown(
                '<div class="section-title">📋 Resume Section Analysis</div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    "**Resume Sections**"
                )

                for section, found in section_results.items():

                    if found:

                        st.success(
                            f"✓ {section} section found"
                        )

                    else:

                        st.warning(
                            f"⚠ {section} section not detected"
                        )

            with col2:

                st.markdown(
                    "**Contact Information**"
                )

                for item, found in contact_results.items():

                    if found:

                        st.success(
                            f"✓ {item} found"
                        )

                    else:

                        st.warning(
                            f"⚠ {item} not detected"
                        )

            # =================================================
            # IMPROVEMENT SUGGESTIONS
            # =================================================

            st.markdown(
                '<div class="section-title">💡 Resume Improvement Suggestions</div>',
                unsafe_allow_html=True
            )

            if suggestions:

                for suggestion in suggestions:

                    st.info(
                        suggestion
                    )

            else:

                st.success(
                    "No major improvement suggestions."
                )

            # =================================================
            # COMPLETION
            # =================================================

            st.divider()

            st.success(
                "✅ Resume analysis completed successfully!"
            )

        except Exception as error:

            st.error(
                "An error occurred while analyzing the resume."
            )

            st.exception(error)

        finally:

            # ------------------------------------------------
            # REMOVE TEMPORARY FILE
            # ------------------------------------------------

            if (
                resume_path is not None
                and os.path.exists(resume_path)
            ):

                os.remove(resume_path)

else:

    st.info(
        "👆 Upload a PDF resume above to begin the analysis."
    )