from golf_stats.parser import parse_summary

# Par 4,3,5,4,3,4,5,4,3 på begge niere = 35 + 35 = 70
PARS = "435434543" * 2


def make_round(id=1, played=18):
    """Bygger én falsk Garmin-runde: 5 slag på de første `played` hullene."""
    return {
        "id": id,
        "scoreType": "STROKE_PLAY",
        "courseName": "Testbanen GK",
        "startTime": "2026-06-01T10:00:00.0",
        "endTime": "2026-06-01T14:00:00.0",
        "roundInProgress": False,
        "holesCompleted": played,
        "roundType": "ALL",
        "holePars": PARS,
        "holes": [
            {"number": n, "strokes": 5 if n <= played else None}
            for n in range(1, 19)
        ],
    }


def test_full_18_hole_round_is_accepted():
    payload = {"totalRows": 1, "scorecardSummaries": [make_round()]}

    result = parse_summary(payload)

    assert len(result.accepted) == 1
    rec = result.accepted[0]
    assert rec["id"] == 1
    assert rec["holes_played"] == 18
    assert rec["total_strokes"] == 90
    assert rec["score_to_par"] == 20  # 90 slag - par 70


def test_round_in_progress_is_discarded():
    rnd = make_round()
    rnd["roundInProgress"] = True
    payload = {"totalRows": 1, "scorecardSummaries": [rnd]}

    result = parse_summary(payload)

    assert result.accepted == []
    assert result.discarded == [{"id": 1, "reason": "round_in_progress"}]


def test_incomplete_round_is_discarded():
    payload = {"totalRows": 1, "scorecardSummaries": [make_round(id=7, played=17)]}

    result = parse_summary(payload)

    assert result.accepted == []
    assert result.discarded == [{"id": 7, "reason": "incomplete_round"}]