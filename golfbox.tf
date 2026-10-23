resource "aws_dynamodb_table" "golfbox" {
  name         = "golf-stats-golfbox"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "round_key"

  attribute {
    name = "round_key"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_cloudwatch_log_group" "lambda_golfbox" {
  name              = "/aws/lambda/golf-stats-golfbox-ingest"
  retention_in_days = 30
}

resource "aws_iam_role" "lambda_golfbox" {
  name = "golf-stats-lambda-golfbox"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_golfbox" {
  name = "golf-stats-lambda-golfbox-access"
  role = aws_iam_role.lambda_golfbox.id

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
        Sid      = "WriteGolfboxRounds"
        Effect   = "Allow"
        Action   = "dynamodb:PutItem"
        Resource = aws_dynamodb_table.golfbox.arn
      },
      {
        Sid      = "WriteLogs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "${aws_cloudwatch_log_group.lambda_golfbox.arn}:*"
      }
    ]
  })
}

resource "aws_lambda_function" "golfbox_ingest" {
  function_name    = "golf-stats-golfbox-ingest"
  role             = aws_iam_role.lambda_golfbox.arn
  runtime          = "python3.13"
  architectures    = ["arm64"]
  handler          = "golf_stats.golfbox_handler.lambda_handler"
  filename         = data.archive_file.lambda_ingest.output_path
  source_code_hash = data.archive_file.lambda_ingest.output_base64sha256
  timeout          = 30
  memory_size      = 512

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.golfbox.name
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_golfbox,
    aws_iam_role_policy.lambda_golfbox,
  ]
}

resource "aws_lambda_permission" "allow_s3_golfbox" {
  statement_id   = "AllowExecutionFromS3Golfbox"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.golfbox_ingest.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.csv_uploads.arn
  source_account = data.aws_caller_identity.current.account_id
}