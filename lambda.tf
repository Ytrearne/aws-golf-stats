resource "aws_cloudwatch_log_group" "lambda_ingest" {
  name              = "/aws/lambda/golf-stats-round-ingest"
  retention_in_days = 30
}

resource "aws_iam_role" "lambda_ingest" {
  name = "golf-stats-lambda-ingest"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_ingest" {
  name = "golf-stats-lambda-ingest-access"
  role = aws_iam_role.lambda_ingest.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ReadUploads"
        Effect   = "Allow"
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.csv_uploads.arn}/*"
      },
      {
        Sid      = "DecryptUploads"
        Effect   = "Allow"
        Action   = "kms:Decrypt"
        Resource = data.aws_kms_key.golf_key.arn
      },
      {
        Sid      = "WriteRounds"
        Effect   = "Allow"
        Action   = "dynamodb:PutItem"
        Resource = aws_dynamodb_table.rounds.arn
      },
      {
        Sid      = "WriteLogs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "${aws_cloudwatch_log_group.lambda_ingest.arn}:*"
      }
    ]
  })
}

data "archive_file" "lambda_ingest" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/build/lambda_ingest.zip"
  excludes    = ["**/__pycache__/**"]
}

resource "aws_lambda_function" "ingest" {
  function_name    = "golf-stats-round-ingest"
  role             = aws_iam_role.lambda_ingest.arn
  runtime          = "python3.13"
  architectures    = ["arm64"]
  handler          = "golf_stats.handler.lambda_handler"
  filename         = data.archive_file.lambda_ingest.output_path
  source_code_hash = data.archive_file.lambda_ingest.output_base64sha256
  timeout          = 30
  memory_size      = 128

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.rounds.name
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_ingest,
    aws_iam_role_policy.lambda_ingest,
  ]
}