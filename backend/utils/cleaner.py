# backend/utils/cleaner.py

import re

def is_valid_comment(text: str) -> bool:
    """
    Filters out CAD garbage, numeric junk,
    coordinate values, tags, and short noise.
    """

    if not text:
        return False

    text = text.strip()

    if len(text) < 12:
        return False

    # Reject mostly numeric strings
    if re.fullmatch(r"[0-9\.\-\s]+", text):
        return False

    # Reject coordinate-like patterns (e.g., 123.456)
    if re.search(r"\d{2,}\.\d{2,}", text):
        return False

    # Reject short CAD tag patterns like U-5716-02
    if re.fullmatch(r"[A-Z0-9\-]{3,15}", text):
        return False

    words = text.split()
    if len(words) < 3:
        return False

    return True


def clean_text(text: str) -> str:
    """
    Cleans whitespace and removes invisible characters.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\x00", "")
    return text.strip()
