from pathlib import Path

from pypdf import PdfReader
from docx import Document as DocxDocument

def extract_pdf(file_path: str) -> list[dict]:
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page_number": page_number,
            "text": text,
        })
    return pages


def extract_docx(file_path: str) -> list[dict]:
    document = DocxDocument(file_path)

    paragraphs = []

    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()

        if text:
            paragraphs.append({
                "paragraph_number": index,
                "text": text,
            })
    return paragraphs


def extract_text(file_path: str) -> list[dict]:
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


