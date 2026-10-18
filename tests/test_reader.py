import json
from decimal import Decimal

from golf_stats.reader import build_response, get_rounds


class FakeTable:
    def __init__(self, items):
        self.items = items

    def scan(self):
        return {"Items": self.items}


def test_build_response_converts_decimal_numbers_to_json():
    items = [
        {
            "round_id": Decimal("386028138"),
            "total_strokes": Decimal("84"),
            "course_name": "Atlungstad Golf",
        }
    ]

    response = build_response(items)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body[0]["round_id"] == 386028138
    assert body[0]["total_strokes"] == 84


def test_get_rounds_returns_newest_round_first():
    table = FakeTable(
        [
            {"round_id": 1, "start_time": "2026-06-01T10:00:00.0"},
            {"round_id": 2, "start_time": "2026-09-01T10:00:00.0"},
            {"round_id": 3, "start_time": "2026-07-15T10:00:00.0"},
        ]
    )

    rounds = get_rounds(table)

    assert [r["round_id"] for r in rounds] == [2, 3, 1]
