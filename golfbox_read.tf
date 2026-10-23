resource "aws_cloudwatch_log_group" "lambda_golfbox_read" {
  name              = "/aws/lambda/golf-stats-golfbox-read"
  retention_in_days = 30
}

resource "aws_iam_role" "lambda_golfbox_read" {
  name = "golf-stats-lambda-golfbox-read"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_golfbox_read" {
  name = "golf-stats-lambda-golfbox-read-access"
  role = aws_iam_role.lambda_golfbox_read.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ReadGolfboxRounds"
        Effect   = "Allow"
        Action   = "dynamodb:Scan"
        Resource = aws_dynamodb_table.golfbox.arn
      },
      {
        Sid      = "WriteLogs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "${aws_cloudwatch_log_group.lambda_golfbox_read.arn}:*"
      }
    ]
  })
}

resource "aws_lambda_function" "golfbox_read" {
  function_name    = "golf-stats-golfbox-read"
  role             = aws_iam_role.lambda_golfbox_read.arn
  runtime          = "python3.13"
  architectures    = ["arm64"]
  handler          = "golf_stats.golfbox_reader.lambda_handler"
  filename         = data.archive_file.lambda_ingest.output_path
  source_code_hash = data.archive_file.lambda_ingest.output_base64sha256
  timeout          = 10
  memory_size      = 512

  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.golfbox.name }
  }

  depends_on = [aws_cloudwatch_log_group.lambda_golfbox_read, aws_iam_role_policy.lambda_golfbox_read]
}