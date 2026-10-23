resource "aws_api_gateway_resource" "handicap" {
  rest_api_id = aws_api_gateway_rest_api.golf.id
  parent_id   = aws_api_gateway_rest_api.golf.root_resource_id
  path_part   = "handicap"
}

resource "aws_api_gateway_method" "get_handicap" {
  rest_api_id      = aws_api_gateway_rest_api.golf.id
  resource_id      = aws_api_gateway_resource.handicap.id
  http_method      = "GET"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_integration" "get_handicap" {
  rest_api_id             = aws_api_gateway_rest_api.golf.id
  resource_id             = aws_api_gateway_resource.handicap.id
  http_method             = aws_api_gateway_method.get_handicap.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.golfbox_read.invoke_arn
}

resource "aws_lambda_permission" "allow_apigw_handicap" {
  statement_id  = "AllowExecutionFromApiGatewayHandicap"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.golfbox_read.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.golf.execution_arn}/*/GET/handicap"
}