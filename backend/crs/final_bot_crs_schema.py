def build_crs_row(index, reference, comment):
    return {
        "s_no": str(index),
        "reference": reference,
        "reviewer_comment": comment,
        "contractor_response": "",
        "status": "Open"
    }
