import json
import os
from decimal import Decimal


def _to_json_number(value):
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    raise TypeError(f"Cannot serialize {type(value)}")


def build_response(items):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(items, default=_to_json_number),
    }


def get_rounds(table):
    items = table.scan()["Items"]
    return sorted(items, key=lambda item: item["start_time"], reverse=True)


def lambda_handler(event, context):
    import boto3  # imported here so the unit tests don't need boto3 installed

    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    return build_response(get_rounds(table))
