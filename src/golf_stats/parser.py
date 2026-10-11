from dataclasses import dataclass, field

EXPECTED_HOLES = {"ALL": 18, "FRONT_9": 9, "BACK_9": 9}


@dataclass
class ParseResult:
    accepted: list = field(default_factory=list)
    discarded: list = field(default_factory=list)


def parse_summary(payload):
    result = ParseResult()
    seen_ids = set()
    for rnd in payload["scorecardSummaries"]:
        if rnd.get("id") is None:
            result.discarded.append({"id": None, "reason": "missing_id"})
            continue
        if rnd["id"] in seen_ids:
            continue
        seen_ids.add(rnd["id"])
        if rnd["roundInProgress"]:
            result.discarded.append({"id": rnd["id"], "reason": "round_in_progress"})
            continue
        if rnd["roundType"] not in EXPECTED_HOLES:
            result.discarded.append({"id": rnd["id"], "reason": "unknown_round_type"})
            continue
        strokes = [h["strokes"] for h in rnd["holes"]]
        pars = [int(p) for p in rnd["holePars"]]
        played = [(s, p) for s, p in zip(strokes, pars) if s is not None]
        if len(played) != EXPECTED_HOLES[rnd["roundType"]]:
            result.discarded.append({"id": rnd["id"], "reason": "incomplete_round"})
            continue    
        total_strokes = sum(s for s, _ in played)
        total_par = sum(p for _, p in played)
        result.accepted.append({
            "id": rnd["id"],
            "course_name": rnd["courseName"],
            "start_time": rnd["startTime"],
            "end_time": rnd["endTime"],
            "round_type": rnd["roundType"],
            "holes_played": len(played),
            "total_strokes": total_strokes,
            "score_to_par": total_strokes - total_par,
            "hole_strokes": strokes,
            "hole_pars": pars,
        })
    return result


