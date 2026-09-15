output "bucket_arn" {
  description = "ARN til test-bucketen"
  value       = aws_s3_bucket.tf_test.arn
}

output "bucket_name" {
  description = "Det faktiske bucket-navnet"
  value       = aws_s3_bucket.tf_test.bucket
}

