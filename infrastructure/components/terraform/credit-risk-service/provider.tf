terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {

  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key

  # LocalStack compatibility flags
  s3_use_path_style           = true
  skip_credentials_validation = var.use_localstack
  skip_metadata_api_check     = var.use_localstack
  skip_requesting_account_id  = var.use_localstack

  dynamic "endpoints" {
    for_each = var.use_localstack ? [1] : []
    content {
      ecs = var.localstack_endpoint
      ecr = var.localstack_endpoint
      iam = var.localstack_endpoint
    }
  }
}