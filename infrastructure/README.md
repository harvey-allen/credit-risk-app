# Infrastructure (Atmos + Terraform)

This directory contains Infrastructure as Code for the credit risk service.

## Directory Layout

```text
infrastructure/
├── atmos.yaml
├── components/
│   └── terraform/
│       └── credit-risk-service/
│           ├── provider.tf
│           ├── variables.tf
│           ├── ecr.tf
│           ├── ecs.tf
│           └── outputs.tf
└── stacks/
    └── orgs/environment/
        ├── development/
        │   ├── eu-west-2.yaml
        │   └── us-east-1.yaml
        └── production/
            ├── eu-west-2.yaml
            └── us-east-1.yaml
```

## Stacks

Stack files are written as path-based identifiers:

- `orgs/environment/development/eu-west-2`
- `orgs/environment/development/us-east-1`
- `orgs/environment/production/eu-west-2`
- `orgs/environment/production/us-east-1`

Resolved Atmos stack names:

- `orgs-environment-dev-eu-west-2`
- `orgs-environment-dev-us-east-1`
- `orgs-environment-prod-eu-west-2`
- `orgs-environment-prod-us-east-1`

## Prerequisites

- `terraform` (>= 1.5)
- `atmos`
- `localstack` (for local development)

## Common Commands

Run from this directory:

```bash
atmos list stacks
atmos list components -s orgs-environment-dev-eu-west-2 -f table
atmos terraform validate credit-risk-service -s orgs/environment/development/eu-west-2
atmos terraform plan credit-risk-service -s orgs/environment/development/eu-west-2
atmos terraform apply credit-risk-service -s orgs/environment/development/eu-west-2
atmos terraform output credit-risk-service -s orgs/environment/development/eu-west-2
```

## LocalStack Notes

- `use_localstack` defaults to `true` in the Terraform component.
- Stack vars provide endpoint/credentials values for local execution.
- To target real AWS, set `use_localstack=false` and provide valid credentials.

## Production Example

```bash
atmos terraform apply credit-risk-service -s orgs/environment/production/eu-west-2 -- \
  -var="aws_access_key=<YOUR_ACCESS_KEY>" \
  -var="aws_secret_key=<YOUR_SECRET_KEY>" \
  -var="aws_region=eu-west-2" \
  -var="use_localstack=false"
```
