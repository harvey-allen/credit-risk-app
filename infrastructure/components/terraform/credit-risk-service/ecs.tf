resource "aws_ecs_cluster" "credit_risk_cluster" {
  name = var.cluster_name
}

resource "aws_ecs_task_definition" "api_task" {

  family                   = var.task_family
  requires_compatibilities = ["FARGATE"]

  cpu    = var.container_cpu
  memory = var.container_memory

  network_mode = "awsvpc"

  container_definitions = jsonencode([
    {
      name  = var.container_name
      image = var.container_image

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]

      environment = [
        {
          name  = "ENV"
          value = var.environment
        }
      ]
    }
  ])
}