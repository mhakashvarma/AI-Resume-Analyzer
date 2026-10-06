# 📄 AI Resume Analyzer

An AI-powered resume analysis application built using Python and Streamlit.

The application analyzes a user's resume, detects skills, evaluates resume strength, identifies skill gaps, and recommends suitable job roles based on the candidate's skills and resume content.

## 🚀 Features

- 📄 Resume Analysis – Upload and analyze a PDF resume.
- 🧠 Skill Detection – Detect technical skills from the resume.
- 📊 Resume Strength Score – Calculate an overall resume score out of 100.
- 🔍 Resume Section Analysis – Check important resume sections.
- 📞 Contact Information Detection – Detect Email, Phone, LinkedIn, and GitHub.
- 💼 Job Role Matching – Compare the resume with available job roles.
- 📋 All Job Roles – Display and rank all available job roles.
- 🏆 Top 3 Recommendations – Recommend the three most suitable job roles.
- 💡 Skill Gap Analysis – Identify missing skills for a selected role.
- 📈 TF-IDF Similarity – Compare resume content with job descriptions.

## 🧮 Job Matching

The application uses two main factors to calculate the final job match score:

- Skill Match – 70%
- TF-IDF Similarity – 30%

Final Match Score:

Skill Match × 70% + TF-IDF Similarity × 30%

The system analyzes all available job roles, ranks them based on their final score, and selects the Top 3 recommended roles.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- PyPDF
- TF-IDF
- Cosine Similarity
- Regular Expressions
- Git
- GitHub

## 📁 Project Structure

AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
│
├── src/
│   ├── final_matcher.py
│   ├── job_matcher.py
│   ├── resume_improver.py
│   ├── resume_parser.py
│   ├── resume_score.py
│   ├── skill_analyzer.py
│   ├── skill_gap.py
│   └── tfidf_matcher.py
│
└── sample_resumes/

## ⚙️ Installation

### 1. Clone the Repository

git clone https://github.com/mhakashvarma/AI-Resume-Analyzer.git

### 2. Open the Project Folder

cd AI-Resume-Analyzer

### 3. Install Dependencies

pip install -r requirements.txt

## ▶️ Run the Application

Run the following command:

streamlit run app.py

The application will open in your browser at:

http://localhost:8501

## 📊 Output

The application provides:

- Detected Skills
- Resume Strength Score
- Resume Section Analysis
- Contact Information Analysis
- All Available Job Roles
- Skill Match Score
- TF-IDF Similarity
- Final Match Score
- Matched Skills
- Missing Skills
- Top 3 Job Recommendations

## 🎯 Purpose

This project is designed to help students and job seekers understand their resume strengths, identify missing skills, and discover suitable technical career roles.

## 🔮 Future Enhancements

- AI-based resume improvement suggestions
- Job description upload and matching
- Advanced NLP-based skill extraction
- Resume keyword optimization
- DOCX resume support
- Online deployment

## 👨‍💻 Author

M H Akash Varma

Computer Science Engineering Student

GitHub:
https://github.com/mhakashvarma/AI-Resume-Analyzer