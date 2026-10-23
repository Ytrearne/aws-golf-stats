data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_kms_key" "golf_key" {
  key_id = "alias/bjarte-golf-key"
}

resource "aws_s3_bucket" "csv_uploads" {
  bucket           = format("golf-stats-csv-uploads-%s-%s-an", data.aws_caller_identity.current.account_id, data.aws_region.current.region)
  bucket_namespace = "account-regional"
}

resource "aws_s3_bucket_versioning" "csv_uploads" {
  bucket = aws_s3_bucket.csv_uploads.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "csv_uploads" {
  bucket = aws_s3_bucket.csv_uploads.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = data.aws_kms_key.golf_key.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "csv_uploads" {
  bucket                  = aws_s3_bucket.csv_uploads.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_notification" "csv_uploads" {
  bucket = aws_s3_bucket.csv_uploads.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.ingest.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".json"
  }

  lambda_function {
    lambda_function_arn = aws_lambda_function.golfbox_ingest.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".txt"
  }

  depends_on = [
    aws_lambda_permission.allow_s3,
    aws_lambda_permission.allow_s3_golfbox,
  ]
}