variable "aws_region" {
  description = "AWS-region ressursene skal opprettes i"
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Prosjektnavn, brukt til tagging"
  type        = string
  default     = "golf-stats-learning"
}
