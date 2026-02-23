from docx import Document


def detect_crs_table(document):
    """
    Automatically detect the CRS table in any uploaded template.
    The table must:
    - Have at least 3 columns
    - Contain header text like COMMENT / REFERENCE / RESPONSE
    """

    for table in document.tables:
        if len(table.rows) == 0:
            continue

        header_cells = table.rows[0].cells
        if len(header_cells) < 3:
            continue

        header_text = " ".join([c.text.strip() for c in header_cells]).upper()

        if any(word in header_text for word in ["COMMENT", "REFERENCE", "PAGE", "RESPONSE"]):
            return table

    return None


def map_columns(table):
    """
    Dynamically map template columns based on header names.
    Works with different CRS formats.
    """

    header_cells = table.rows[0].cells
    col_map = {}

    for idx, cell in enumerate(header_cells):
        text = cell.text.strip().upper()

        if "S" in text and "NO" in text:
            col_map["sno"] = idx
        elif "REFERENCE" in text or "PAGE" in text:
            col_map["reference"] = idx
        elif "COMMENT" in text:
            col_map["comment"] = idx
        elif "RESPONSE" in text:
            col_map["response"] = idx
        elif "STATUS" in text or "REMARK" in text:
            col_map["status"] = idx

    return col_map


def generate_word_crs(template_path, crs_rows, output_path):

    doc = Document(template_path)

    table = detect_crs_table(doc)

    if not table:
        raise Exception("No valid CRS table found in uploaded template.")

    col_map = map_columns(table)

    for i, row in enumerate(crs_rows, start=1):
        new_row = table.add_row()

        if "sno" in col_map:
            new_row.cells[col_map["sno"]].text = str(i)

        if "reference" in col_map:
            new_row.cells[col_map["reference"]].text = row.get("reference", "")

        if "comment" in col_map:
            new_row.cells[col_map["comment"]].text = row.get("reviewer_comment", "")

        if "response" in col_map:
            new_row.cells[col_map["response"]].text = ""

        if "status" in col_map:
            new_row.cells[col_map["status"]].text = ""

    doc.save(output_path)
