from golf_stats.parser import ParseResult
from collections import Counter


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
                "gross": int(gross) if gross.strip() else None,
                "adjusted_gross": int(adjusted),
            }
        except ValueError:
            result.discarded.append({"reason": "unreadable_value", "line": line})
            continue
        result.accepted.append(record)
    per_date = Counter()
    for record in reversed(result.accepted):
        per_date[record["date"]] += 1
        record["round_key"] = f"{record['date']}#{per_date[record['date']]}"
    return result