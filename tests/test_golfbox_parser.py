from golf_stats.golfbox_parser import parse_scorearkiv

LINE = "07.10.2026 00:00\tAtlungstad GK\t3,9\t79\t79"


def test_parses_one_round_line():
    result = parse_scorearkiv(LINE)
    assert result.discarded == []
    assert result.accepted == [
        {
            "date": "2026-10-07",
            "course_text": "Atlungstad GK",
            "handicap_before": 3.9,
            "gross": 79,
            "adjusted_gross": 79,
        }
    ]


def test_skips_lines_that_are_not_round_rows():
    result = parse_scorearkiv("Scorearkiv 2026\n" + LINE)
    assert len(result.accepted) == 1
    assert result.discarded == []


def test_discards_row_with_unreadable_handicap():
    bad = "07.10.2026 00:00\tAtlungstad GK\tx\t79\t79"
    result = parse_scorearkiv(bad + "\n" + LINE)
    assert len(result.accepted) == 1
    assert len(result.discarded) == 1