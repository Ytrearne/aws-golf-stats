resource "aws_api_gateway_api_key" "golf" {
  name = "golf-stats-dashboard"
}

resource "aws_api_gateway_usage_plan" "golf" {
  name = "golf-stats-plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.golf.id
    stage  = aws_api_gateway_stage.v1.stage_name
  }

  throttle_settings {
    rate_limit  = 5
    burst_limit = 10
  }

  quota_settings {
    limit  = 1000
    period = "DAY"
  }
}

resource "aws_api_gateway_usage_plan_key" "golf" {
  key_id        = aws_api_gateway_api_key.golf.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.golf.id
}
