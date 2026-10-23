from golf_stats.golfbox_handler import store_golfbox_rounds
from test_handler import FakeTable
from decimal import Decimal


TEXT = (
    "15.06.2026 00:00\tTestby GK\t12,3\t43\t43\n"
    "15.06.2026 00:00\tTestby GK\t12,5\t85\t84\n"
    "16.06.2026 00:00\tTestby GK\tx\t90\t90"
)


def test_store_golfbox_rounds_writes_accepted_rounds_with_round_key():
    table = FakeTable()

    summary = store_golfbox_rounds(TEXT, table)

    assert [item["round_key"] for item in table.items] == ["2026-06-15#2", "2026-06-15#1"]
    assert summary == {"stored": 2, "discarded": 1}

def test_store_golfbox_rounds_converts_handicap_to_decimal():
    table = FakeTable()

    store_golfbox_rounds(TEXT, table)

    handicap = table.items[0]["handicap_before"]
    assert isinstance(handicap, Decimal)
    assert handicap == Decimal("12.3")