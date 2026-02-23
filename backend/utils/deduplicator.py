def deduplicate_comments(comments):
    seen = set()
    unique = []

    for c in comments:
        key = c["comment"].strip().lower()

        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique
