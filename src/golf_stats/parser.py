from dataclasses import dataclass, field


@dataclass
class ParseResult:
    accepted: list = field(default_factory=list)
    discarded: list = field(default_factory=list)


def parse_summary(payload):
    result = ParseResult()
    for rnd in payload["scorecardSummaries"]:
        if rnd["roundInProgress"]:
            result.discarded.append({"id": rnd["id"], "reason": "round_in_progress"})
            continue
        strokes = [h["strokes"] for h in rnd["holes"]]
        pars = [int(p) for p in rnd["holePars"]]
        played = [(s, p) for s, p in zip(strokes, pars) if s is not None]
        if len(played) != 18:
            result.discarded.append({"id": rnd["id"], "reason": "incomplete_round"})
            continue
        total_strokes = sum(s for s, _ in played)
        total_par = sum(p for _, p in played)
        result.accepted.append({
            "id": rnd["id"],
            "holes_played": len(played),
            "total_strokes": total_strokes,
            "score_to_par": total_strokes - total_par,
        })
    return result


