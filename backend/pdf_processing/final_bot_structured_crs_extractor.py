import pdfplumber


def extract_structured_crs(pdf_path):
    """
    Extracts COMPANY Comments column from structured CRS tables.
    """

    results = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):

            tables = page.extract_tables()
            if not tables:
                continue

            for table in tables:
                headers = [(cell or "").strip().upper() for cell in table[0]]

                if "COMPANY COMMENTS" in headers:
                    comment_index = headers.index("COMPANY COMMENTS")

                    for row in table[1:]:
                        if len(row) > comment_index:
                            comment = row[comment_index]

                            if comment:
                                # Merge into single paragraph
                                comment = " ".join(comment.split())

                                results.append({
                                    "reference": f"Page {page_no}",
                                    "comment": comment
                                })

    return results
