"""Lambda behind the API: returns GolfBox rounds as JSON, oldest first."""
import os

from golf_stats.reader import build_response


def _sort_key(item):
    """Split '2026-06-15#10' into ('2026-06-15', 10) so the sequence sorts as a number."""
    date, sequence = item["round_key"].split("#")
    return date, int(sequence)


def get_golfbox_rounds(table):
    """Return all GolfBox rounds, oldest first (the order a graph is drawn in)."""
    items = table.scan()["Items"]
    return sorted(items, key=_sort_key)


def lambda_handler(event, context):
    """Entry point: runs when API Gateway receives GET /handicap."""
    # boto3 is imported here so the unit tests can run without it installed.
    import boto3

    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    return build_response(get_golfbox_rounds(table))