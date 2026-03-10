resource "aws_ecs_cluster" "credit_risk_cluster" {
  name = "credit-risk-cluster"
}

resource "aws_ecs_task_definition" "api_task" {

  family                   = "credit-risk-api"
  requires_compatibilities = ["FARGATE"]

  cpu    = "256"
  memory = "512"

  network_mode = "awsvpc"

  container_definitions = jsonencode([
    {
      name  = "credit-risk-api"
      image = "credit-risk-api:latest"

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]

      environment = [
        {
          name  = "ENV"
          value = "local"
        }
      ]
    }
  ])
}