from golf_stats.golfbox_parser import parse_scorearkiv
from decimal import Decimal
import os
from golf_stats.handler import get_location


def store_golfbox_rounds(text, table):
    """Parse GolfBox text and write each accepted round to the table."""
    result = parse_scorearkiv(text)
    for record in result.accepted:
        item = {**record, "handicap_before": Decimal(str(record["handicap_before"]))}
        table.put_item(Item=item)
    return {"stored": len(result.accepted), "discarded": len(result.discarded)}

def lambda_handler(event, context):
    """S3 upload trigger: read the GolfBox text file and store its rounds."""
    # boto3 is imported here so unit tests run without it installed.
    import boto3

    bucket, key = get_location(event)
    body = boto3.client("s3").get_object(Bucket=bucket, Key=key)["Body"].read()
    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    summary = store_golfbox_rounds(body.decode("utf-8-sig"), table)
    print(summary)
    return summary