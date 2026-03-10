terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {

  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.aws_region

  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    ecs = var.localstack_endpoint
    ecr = var.localstack_endpoint
    iam = var.localstack_endpoint
  }
}