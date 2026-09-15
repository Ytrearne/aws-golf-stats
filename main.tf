terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_s3_bucket" "tf_test" {
  bucket = format(
    "bjarte-tf-test-%s-%s",
    data.aws_caller_identity.current.account_id,
    data.aws_region.current.name
  )

  tags = {
    Project = var.project_name
  }
}