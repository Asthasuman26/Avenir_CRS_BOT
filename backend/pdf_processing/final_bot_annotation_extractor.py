# backend/pdf_processing/final_bot_annotation_extractor.py

import fitz


def extract_annotations(pdf_path):

    doc = fitz.open(pdf_path)
    results = []

    for page_no, page in enumerate(doc, start=1):
        for annot in page.annots() or []:

            content = annot.info.get("content", "")

            if content:
                content = " ".join(content.split())

                results.append({
                    "reference": f"Page {page_no}",
                    "comment": content
                })

    doc.close()
    return results
