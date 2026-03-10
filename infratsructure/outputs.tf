output "ecr_repo" {
  value = aws_ecr_repository.credit_risk_api.repository_url
}

output "ecs_cluster" {
  value = aws_ecs_cluster.credit_risk_cluster.name
}