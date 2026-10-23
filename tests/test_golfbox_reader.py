from golf_stats.golfbox_reader import get_golfbox_rounds
from test_reader import FakeTable


def test_get_golfbox_rounds_returns_oldest_round_first():
    table = FakeTable(
        [
            {"round_key": "2026-06-15#10"},
            {"round_key": "2026-06-15#2"},
            {"round_key": "2026-06-01#1"},
        ]
    )

    rounds = get_golfbox_rounds(table)

    keys = [r["round_key"] for r in rounds]
    assert keys == ["2026-06-01#1", "2026-06-15#2", "2026-06-15#10"]