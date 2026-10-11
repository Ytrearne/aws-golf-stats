from golf_stats.handler import get_location, store_rounds
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


def test_get_location_reads_bucket_and_key_from_s3_event():
    event = {
        "Records": [
            {"s3": {"bucket": {"name": "my-bucket"}, "object": {"key": "uploads/garmin.json"}}}
        ]
    }

    assert get_location(event) == ("my-bucket", "uploads/garmin.json")
