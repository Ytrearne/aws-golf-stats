"""Lambda that reads a Garmin export from S3 and stores the rounds in DynamoDB."""
import json
import os
import logging
from urllib.parse import unquote_plus
from golf_stats.parser import parse_summary

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def store_rounds(payload, table):
    """Parse a Garmin export and save every accepted round in the table.

    put_item replaces the whole item, so uploading the same export again
    updates rounds instead of duplicating them. Returns how many rounds were
    stored and how many were discarded.
    """
    result = parse_summary(payload)

    for rec in result.accepted:
        item = dict(rec)
        item["round_id"] = item.pop("id")  # round_id is the table's partition key
        table.put_item(Item=item)

    for d in result.discarded:
        logger.warning("Discarded round %s: %s", d["id"], d["reason"])

    return {"stored": len(result.accepted), "discarded": len(result.discarded)}


def get_location(event):
    """Return (bucket, key) of the uploaded file from an S3 event.

    S3 URL-encodes the key (a space becomes "+"), so it has to be decoded.
    """
    s3_info = event["Records"][0]["s3"]
    bucket = s3_info["bucket"]["name"]
    key = unquote_plus(s3_info["object"]["key"])
    return bucket, key


def lambda_handler(event, context):
    """Entry point: runs when a .json file is uploaded to the S3 bucket."""
    # boto3 is imported here so the unit tests can run without it installed.
    import boto3

    bucket, key = get_location(event)

    s3 = boto3.client("s3")
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    payload = json.loads(body)

    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    summary = store_rounds(payload, table)

    logger.info("Processed s3://%s/%s: %s", bucket, key, summary)
    return summary
