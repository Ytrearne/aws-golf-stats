resource "aws_api_gateway_rest_api" "golf" {
  name        = "golf-stats-api"
  description = "Read API for golf rounds"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "rounds" {
  rest_api_id = aws_api_gateway_rest_api.golf.id
  parent_id   = aws_api_gateway_rest_api.golf.root_resource_id
  path_part   = "rounds"
}

resource "aws_api_gateway_method" "get_rounds" {
  rest_api_id      = aws_api_gateway_rest_api.golf.id
  resource_id      = aws_api_gateway_resource.rounds.id
  http_method      = "GET"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_integration" "get_rounds" {
  rest_api_id             = aws_api_gateway_rest_api.golf.id
  resource_id             = aws_api_gateway_resource.rounds.id
  http_method             = aws_api_gateway_method.get_rounds.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.read.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.read.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.golf.execution_arn}/*/GET/rounds"
}

resource "aws_api_gateway_deployment" "golf" {
  rest_api_id = aws_api_gateway_rest_api.golf.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.rounds.id,
      aws_api_gateway_method.get_rounds.id,
      aws_api_gateway_integration.get_rounds.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "v1" {
  rest_api_id   = aws_api_gateway_rest_api.golf.id
  deployment_id = aws_api_gateway_deployment.golf.id
  stage_name    = "v1"
}

output "api_url" {
  value = "${aws_api_gateway_stage.v1.invoke_url}/rounds"
}
