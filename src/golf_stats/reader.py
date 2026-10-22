"""Lambda behind the API: returns all rounds as JSON, newest first."""
import json
import os
from decimal import Decimal


def _to_json_number(value):
    """Convert a DynamoDB Decimal to int or float, which json.dumps can handle."""
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    raise TypeError(f"Cannot serialize {type(value)}")


def build_response(items):
    """Wrap the rounds in the response format API Gateway expects."""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items, default=_to_json_number),
    }


def get_rounds(table):
    """Return all rounds, newest first.

    Scan returns items in no particular order, so they are sorted here.
    One Scan reads at most 1 MB, which is plenty for a few hundred rounds.
    """
    items = table.scan()["Items"]
    return sorted(items, key=lambda item: item["start_time"], reverse=True)


def lambda_handler(event, context):
    """Entry point: runs when API Gateway receives GET /rounds."""
    # boto3 is imported here so the unit tests can run without it installed.
    import boto3

    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    return build_response(get_rounds(table))
