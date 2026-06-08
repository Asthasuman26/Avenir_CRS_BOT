import fitz


def clean_annotation_text(text: str) -> str:
    """
    Normalize PDF annotation text while keeping only the actual reviewer note.
    """
    return " ".join((text or "").replace("\x00", "").split())


def extract_drawing_comments(pdf_path: str):
    """
    Extract only reviewer comments that are written on top of the PDF as
    annotations.

    Earlier this extractor read every text block from the PDF page. That also
    picked up drawing headings, title blocks, labels, and other native PDF text.
    Using the annotation layer keeps the CRS output limited to comments added
    over the PDF, such as sticky notes and free-text comments.
    """
    doc = fitz.open(pdf_path)
    results = []

    for page_no, page in enumerate(doc, start=1):
        for annot in page.annots() or []:
            comment = clean_annotation_text(annot.info.get("content", ""))

            if not comment:
                continue

            results.append({
                "reference": f"Page {page_no}",
                "comment": comment
            })

    doc.close()
    return results
