output "ci_test_bucket_name" {
  description = "Navnet på bucketen opprettet av CI/CD-pipelinen (Modul 6-test)"
  value       = aws_s3_bucket.ci_test.bucket
}