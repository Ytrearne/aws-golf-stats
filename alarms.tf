locals {
  alarm_topic_arn = "arn:aws:sns:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:golf-stats-alarms"
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "golf-stats-round-ingest-errors"
  alarm_description   = "Ingest Lambda failed at least once in 5 minutes"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  dimensions          = { FunctionName = aws_lambda_function.ingest.function_name }
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [local.alarm_topic_arn]
}