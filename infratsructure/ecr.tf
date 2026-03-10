resource "aws_ecr_repository" "credit_risk_api" {
  name = "credit-risk-api"

  image_scanning_configuration {
    scan_on_push = false
  }
}