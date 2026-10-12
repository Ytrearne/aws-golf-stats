import json
import os
import logging
from urllib.parse import unquote_plus
from golf_stats.parser import parse_summary

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def store_rounds(payload, table):
    result = parse_summary(payload)

    for rec in result.accepted:
        item = dict(rec)
        item["round_id"] = item.pop("id")
        table.put_item(Item=item)

    for d in result.discarded:
        logger.warning("Discarded round %s: %s", d["id"], d["reason"])

    return {"stored": len(result.accepted), "discarded": len(result.discarded)}


def get_location(event):
    s3_info = event["Records"][0]["s3"]
    bucket = s3_info["bucket"]["name"]
    key = unquote_plus(s3_info["object"]["key"])
    return bucket, key


def lambda_handler(event, context):
    import boto3  

    bucket, key = get_location(event)

    s3 = boto3.client("s3")
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    payload = json.loads(body)

    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    summary = store_rounds(payload, table)

    logger.info("Processed s3://%s/%s: %s", bucket, key, summary)
    return summary