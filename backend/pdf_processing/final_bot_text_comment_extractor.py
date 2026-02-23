# backend/pdf_processing/final_bot_text_comment_extractor.py

import pdfplumber
from backend.utils.cleaner import is_valid_comment, clean_text

KEYWORDS = [
    "WHY", "UPDATE", "CHECK", "NOT MATCHING",
    "SUBJECT TO", "CLARIFY", "CORRECT",
    "REVISE", "ADD", "REMOVE"
]


def extract_printed_comments(pdf_path):
    results = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            for line in text.split("\n"):
                if any(k in line.upper() for k in KEYWORDS):
                    if is_valid_comment(line):
                        results.append({
                            "reference": f"Page {page_no}",
                            "comment": clean_text(line)
                        })

    return results
