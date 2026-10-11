from golf_stats.handler import store_rounds
from test_parser import make_round


class FakeTable:
    def __init__(self):
        self.items = []

    def put_item(self, Item):
        self.items.append(Item)


def test_store_rounds_writes_accepted_rounds_with_round_id():
    table = FakeTable()
    payload = {
        "totalRows": 2,
        "scorecardSummaries": [make_round(id=1), make_round(id=2, played=14)],
    }

    summary = store_rounds(payload, table)

    assert [item["round_id"] for item in table.items] == [1]
    assert "id" not in table.items[0]
    assert summary == {"stored": 1, "discarded": 1}