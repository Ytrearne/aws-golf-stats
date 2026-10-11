import logging

from golf_stats.parser import parse_summary

logger = logging.getLogger()


def store_rounds(payload, table):
    result = parse_summary(payload)

    for rec in result.accepted:
        item = dict(rec)
        item["round_id"] = item.pop("id")
        table.put_item(Item=item)

    for d in result.discarded:
        logger.warning("Discarded round %s: %s", d["id"], d["reason"])

    return {"stored": len(result.accepted), "discarded": len(result.discarded)}