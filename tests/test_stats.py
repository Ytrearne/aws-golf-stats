from dashboard_stats import summarize


def make_round(holes_played, score_to_par):
    return {"holes_played": holes_played, "score_to_par": score_to_par}


def test_counts_all_rounds_and_full_rounds_separately():
    rounds = [make_round(18, 10), make_round(9, 2), make_round(18, 14)]
    result = summarize(rounds)
    assert result["rounds"] == 3
    assert result["full_rounds"] == 2


def test_best_and_average_use_only_18_hole_rounds():
    rounds = [make_round(18, 10), make_round(18, 14), make_round(18, 6), make_round(9, -3)]
    result = summarize(rounds)
    assert result["best_full_round"] == 6
    assert result["average_full_round"] == 10.0


def test_empty_list_gives_no_best_or_average():
    result = summarize([])
    assert result["rounds"] == 0
    assert result["best_full_round"] is None
    assert result["average_full_round"] is None
