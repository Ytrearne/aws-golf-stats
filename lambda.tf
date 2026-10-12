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