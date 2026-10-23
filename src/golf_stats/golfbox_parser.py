from golf_stats.parser import ParseResult


def parse_scorearkiv(text):
    """Turn pasted GolfBox Scorearkiv text into round records."""
    result = ParseResult(accepted=[], discarded=[])
    for line in text.splitlines():
        fields = line.split("\t")
        if len(fields) != 5:
            continue
        date, course, hcp, gross, adjusted = fields
        try:
            day, month, year = date[:10].split(".")
            record = {
                "date": f"{year}-{month}-{day}",
                "course_text": course,
                "handicap_before": float(hcp.replace(",", ".")),
                "gross": int(gross),
                "adjusted_gross": int(adjusted),
            }
        except ValueError:
            result.discarded.append({"reason": "unreadable_value", "line": line})
            continue
        result.accepted.append(record)
    return result