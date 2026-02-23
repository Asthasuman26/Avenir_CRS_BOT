import os
import time

from backend.pdf_processing.final_bot_pdf_classifier import classify_pdf
from backend.pdf_processing.final_bot_structured_crs_extractor import extract_structured_crs
from backend.pdf_processing.extract_drawing_comments import extract_drawing_comments
from backend.crs.final_bot_crs_mapper import map_comments_to_crs
from backend.crs.final_bot_crs_word_generator import generate_word_crs
from backend.utils.deduplicator import deduplicate_comments

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "storage", "outputs")

PDF_PATH = os.path.join(UPLOAD_DIR, "input.pdf")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- TEMPLATE HANDLING ----------------

DEFAULT_TEMPLATE_PATH = os.path.join(
    os.path.dirname(BASE_DIR),
    "templates",
    "FINAL_BOT_CRS_TEMPLATE.docx"
)

CUSTOM_TEMPLATE_PATH = os.path.join(
    UPLOAD_DIR,
    "custom_template.docx"
)

if os.path.exists(CUSTOM_TEMPLATE_PATH):
    TEMPLATE_PATH = CUSTOM_TEMPLATE_PATH
else:
    TEMPLATE_PATH = DEFAULT_TEMPLATE_PATH


def get_safe_output_path(base_path):
    name, ext = os.path.splitext(base_path)
    version = 1
    candidate = base_path

    while True:
        try:
            with open(candidate, "a"):
                return candidate
        except PermissionError:
            candidate = f"{name}_v{version}{ext}"
            version += 1
            time.sleep(0.1)


OUTPUT_PATH = get_safe_output_path(
    os.path.join(OUTPUT_DIR, "input_OUTPUT.docx")
)

# ---------------- EXTRACTION ----------------

page_types = classify_pdf(PDF_PATH)

comments = []

if "structured_crs" in page_types:
    comments.extend(extract_structured_crs(PDF_PATH))

comments.extend(extract_drawing_comments(PDF_PATH))

comments = deduplicate_comments(comments)

crs_rows = map_comments_to_crs(comments)

generate_word_crs(
    TEMPLATE_PATH,
    crs_rows,
    OUTPUT_PATH
)

print(f"CRS generated successfully: {OUTPUT_PATH}")
