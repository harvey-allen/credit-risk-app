variable "aws_access_key" {
  description = "AWS access key"
  type        = string
  default     = "test"
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
  default     = "test"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "localstack_endpoint" {
  description = "LocalStack endpoint"
  type        = string
  default     = "http://localhost:4566"
}