from .final_bot_crs_schema import build_crs_row

def map_comments_to_crs(comments):
    rows = []
    for i, c in enumerate(comments, start=1):
        rows.append(
            build_crs_row(i, c["reference"], c["comment"])
        )
    return rows
