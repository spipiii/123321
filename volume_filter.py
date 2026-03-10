
def filter_low_volume(rows, min_volume):

    filtered = []

    for r in rows:

        if r["volume"] >= min_volume:
            filtered.append(r)

    return filtered
