import fitz
import re


def is_real_comment(text: str) -> bool:
    text = text.strip()

    if not text:
        return False

    normalized = " ".join(text.split())

    # Minimum length
    if len(normalized) < 18:
        return False

    # At least 3 words
    words = normalized.split()
    if len(words) < 3:
        return False

    # Reject pure numeric blocks
    if re.fullmatch(r"[0-9\.\-\s×x,/]+", normalized):
        return False

    # Reject numeric-dominated blocks (dimensions, coordinates)
    digit_ratio = sum(c.isdigit() for c in normalized) / len(normalized)
    if digit_ratio > 0.4:
        return False

    # Reject short ALL CAPS identifiers
    if normalized.isupper() and len(normalized) < 45:
        return False

    # Reject short label-style blocks
    if len(words) <= 4 and all(w.isalnum() for w in words):
        return False

    return True


def extract_drawing_comments(pdf_path: str):
    doc = fitz.open(pdf_path)
    results = []

    for page_no, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4]

            if is_real_comment(text):
                clean = " ".join(text.split())

                results.append({
                    "reference": f"Page {page_no}",
                    "comment": clean
                })

    doc.close()
    return results
