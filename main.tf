terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "golf-stats-tfstate-790873128115-eu-north-1"
    key          = "golf-stats/terraform.tfstate"
    region       = "eu-north-1"
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_s3_bucket" "ci_test" {
  bucket = format(
    "golf-stats-ci-test-%s-%s",
    data.aws_caller_identity.current.account_id,
    data.aws_region.current.name
  )

  tags = {
    Project = var.project_name
    Purpose = "CI/CD pipeline test - Modul 6"
  }
}