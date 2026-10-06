from pathlib import Path
import re

from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_path):
    """Extract text from all pages of a PDF resume."""

    reader = PdfReader(file_path)

    all_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            all_text.append(page_text)

    return "\n".join(all_text)

def extract_text_from_docx(file_path):
    """Extract text from all paragraphs of a DOCX resume."""

    document = Document(file_path)

    all_text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            all_text.append(paragraph.text)

    return "\n".join(all_text)

def clean_resume_text(text):
    """Clean resume text before comparison."""

    text = text.lower()

    # Keep letters, numbers, spaces and important technical symbols.
    text = re.sub(r"[^\w\s+#.\-/]", " ", text)

    # Replace repeated spaces and line breaks with one space.
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def extract_resume_text(file_path):
    """Extract and clean text from a PDF or DOCX resume."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = file_path.suffix.lower()

    if file_extension == ".pdf":
        text = extract_text_from_pdf(file_path)

    elif file_extension == ".docx":
        text = extract_text_from_docx(file_path)

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    return clean_resume_text(text)

if __name__ == "__main__":
    print("Resume parser module is working.")