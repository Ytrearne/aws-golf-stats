resource "aws_dynamodb_table" "rounds" {
  name         = "golf-stats-rounds"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "round_id"

  attribute {
    name = "round_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}