# backend/pdf_processing/final_bot_pdf_classifier.py

import fitz

TEXT_DENSITY_THRESHOLD = 800
DRAWING_THRESHOLD = 200


def classify_page(page):
    text = page.get_text("text") or ""
    text_len = len(text.strip())
    drawing_count = len(page.get_drawings())
    has_annots = bool(page.annots())

    if has_annots:
        return "annotated"

    if drawing_count > DRAWING_THRESHOLD and text_len < 300:
        return "cad_drawing"

    if "COMMENTS RESOLUTION SHEET" in text.upper():
        return "structured_crs"

    if text_len > TEXT_DENSITY_THRESHOLD:
        return "text_document"

    return "unknown"


def classify_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    page_types = [classify_page(page) for page in doc]
    doc.close()
    return page_types
