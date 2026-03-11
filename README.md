# Credit Risk Assessment Application

A full-stack web application for credit risk assessment and credit score prediction using machine learning. This application consists of a Django REST API backend and a React frontend, providing an intuitive interface for evaluating creditworthiness based on various financial parameters.

## Features

- **Credit Score Prediction**: Machine learning-based credit scoring using scikit-learn
- **RESTful API**: Django REST Framework backend with comprehensive API endpoints
- **Interactive Frontend**: React-based user interface for data entry and results display
- **User Management**: Built-in user authentication and management system
- **Real-time Validation**: Form validation and error handling
- **PostgreSQL Database**: Production-ready database support
- **Docker Support**: Containerized deployment with Docker Compose
- **API Documentation**: Auto-generated API documentation with drf-spectacular
- **Infrastructure as Code**: Terraform-managed AWS infrastructure (ECR + ECS Fargate)

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using Docker (Recommended)](#using-docker-recommended)
  - [Manual Setup](#manual-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Infrastructure](#infrastructure)
  - [Overview](#overview)
   - [Atmos Layout](#atmos-layout)
   - [Resources](#resources)
   - [Atmos Workflow](#atmos-workflow)
  - [LocalStack Development](#localstack-development)
  - [Deploying to AWS](#deploying-to-aws)
- [Development](#development)
- [Research](#research)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The application is structured as a monorepo containing:

- **Backend (`/src`)**: Django REST API with machine learning integration
- **Frontend (`/frontend`)**: React application for user interaction
- **Research (`/research`)**: Jupyter notebooks for model development and analysis

### Technology Stack

**Backend:**
- Django 4.1.5
- Django REST Framework
- PostgreSQL (with psycopg2)
- scikit-learn (Machine Learning)
- pandas (Data processing)
- drf-spectacular (API documentation)

**Frontend:**
- React 18.2.0
- Axios (HTTP client)
- React Scripts 5.0.1

**Infrastructure (IaC):**
- Terraform (AWS provider ~> 5.0)
- Amazon ECR (container image registry)
- Amazon ECS Fargate (serverless container runtime)
- LocalStack (local AWS cloud emulation for development)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- Node.js 14+ and npm
- PostgreSQL 12+ (or use Docker)
- Docker and Docker Compose (optional, but recommended)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/harvey-allen/credit-risk-app.git
   cd credit-risk-app
   ```

2. Create a `.env` file in the `src/` directory:
   ```bash
   cd src
   cp .env.example .env  # If example exists, or create manually
   ```
   
   Add the following environment variables:
   ```
   POSTGRES_DB=creditrisk
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

3. Start the services using Docker Compose:
   ```bash
   cd src/docker
   docker-compose up -d
   ```

4. Run database migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Manual Setup

#### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/harvey-allen/credit-risk-app.git
   cd credit-risk-app/src
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your database and configure environment variables in `.env`

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Access the Application**: Open your browser and navigate to `http://localhost:3000`

2. **Enter Credit Parameters**: Fill out the form with the following information:
   - Personal Information (Name, Age, Occupation)
   - Financial Details (Annual Income, Monthly Salary, Outstanding Debt)
   - Credit Information (Number of Credit Cards, Loans, Payment Behavior)
   - Account Details (Bank Accounts, Credit Mix, Payment History)

3. **Submit for Analysis**: Click submit to send the data to the backend API

4. **View Results**: The application will display the predicted credit score classification:
   - Poor Credit
   - Standard Credit
   - Good Credit

## Project Structure

```
credit-risk-app/
├── src/                          # Django backend
│   ├── calculate/                # Credit calculation app
│   │   ├── api/                  # API viewsets and serializers
│   │   ├── migrations/           # Database migrations
│   │   ├── tests/                # Unit tests
│   │   └── models.py             # Credit models
│   ├── creditAPI/                # Django project settings
│   ├── users/                    # User management app
│   ├── helpers/                  # Utility functions
│   ├── model/                    # ML model directory
│   ├── docker/                   # Docker configuration
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
├── frontend/                     # React frontend
│   ├── public/                   # Static files
│   ├── src/                      # React source code
│   │   ├── components/           # React components
│   │   ├── App.js                # Main app component
│   │   └── index.js              # Entry point
│   ├── package.json              # Node dependencies
│   └── README.md                 # Frontend documentation
├── research/                     # Research and analysis
│   ├── credit_model.ipynb        # Model development notebook
│   └── data/                     # Training data
├── infrastructure/               # Atmos + Terraform IaC configuration
│   ├── atmos.yaml                # Atmos root config
│   ├── components/terraform/     # Terraform components
│   │   └── credit-risk-service/  # ECR + ECS service component
│   └── stacks/                   # Stack manifests (env + region)
└── README.md                     # This file
```

## API Documentation

The API provides the following main endpoints:

- `GET /api/calculate/` - List all credit parameter records
- `POST /api/calculate/create/` - Create a new credit assessment
- `GET /api/schema/` - OpenAPI schema
- `GET /api/docs/` - Interactive API documentation (Swagger UI)

### Example API Request

```bash
curl -X POST http://localhost:8000/api/calculate/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 30,
    "occupation": "Engineer",
    "annual_income": 75000.00,
    "monthly_in_hand_salary": 5500.00,
    "number_of_bank_accounts": 3,
    "number_of_credit_cards": 2,
    "interest_rate": 12.5,
    "number_of_loans": 2,
    "delay_from_due_date": "0",
    "number_of_delayed_payment": 0,
    "changed_credit_limit": "No",
    "num_credit_inquiries": 2,
    "credit_mix": "Good",
    "outstanding_debt": 5000.00,
    "credit_utilization_ratio": 30.5,
    "payment_of_minimum_amount": "Yes",
    "total_emi_per_month": 800.00,
    "amount_invested_monthly": 500.00,
    "monthly_balance": 2000.00,
    "payment_behaviour": "high_spend_medium_value_payments"
  }'
```

## Infrastructure

### Overview

The cloud infrastructure is defined as code using [Terraform](https://www.terraform.io/) and orchestrated with [Atmos](https://atmos.tools/). It lives in the `infrastructure/` directory and targets **AWS**. [LocalStack](https://www.localstack.cloud/) is used to emulate AWS services locally during development.

### Atmos Layout

- Atmos config: `infrastructure/atmos.yaml`
- Terraform component: `infrastructure/components/terraform/credit-risk-service/`
- Stack manifests:
   - `infrastructure/stacks/orgs/environment/development/eu-west-2.yaml`
   - `infrastructure/stacks/orgs/environment/development/us-east-1.yaml`
   - `infrastructure/stacks/orgs/environment/production/eu-west-2.yaml`
   - `infrastructure/stacks/orgs/environment/production/us-east-1.yaml`

Resolved Atmos stack names are:
- `orgs-environment-dev-eu-west-2`
- `orgs-environment-dev-us-east-1`
- `orgs-environment-prod-eu-west-2`
- `orgs-environment-prod-us-east-1`

| Component | AWS Service | Purpose |
|-----------|-------------|-----------------------------|
| Container registry | Amazon ECR | Stores the Docker image for the API |
| Container runtime | Amazon ECS (Fargate) | Runs the API container serverlessly |

### Resources

**ECR Repository** (`components/terraform/credit-risk-service/ecr.tf`)
- Repository name: `credit-risk-api`
- Image scanning on push is disabled (enable for production)

**ECS Cluster & Task Definition** (`components/terraform/credit-risk-service/ecs.tf`)
- Cluster name is stack-driven (`cluster_name` variable)
- Launch type: `FARGATE` (serverless, no EC2 instances to manage)
- Network mode: `awsvpc`
- CPU: `256` units · Memory: `512` MB
- Container port: `8000` (Django API)

**Outputs** (`components/terraform/credit-risk-service/outputs.tf`)
- `ecr_repo` – ECR repository URL (use as the image URI when pushing)
- `ecs_cluster` – ECS cluster name

### Atmos Workflow

From the `infrastructure/` directory:

```bash
atmos list stacks
atmos list components -s orgs-environment-dev-eu-west-2
atmos terraform validate credit-risk-service -s orgs/environment/development/eu-west-2
atmos terraform plan credit-risk-service -s orgs/environment/development/eu-west-2
atmos terraform apply credit-risk-service -s orgs/environment/development/eu-west-2
```

**Input Variables** (`components/terraform/credit-risk-service/variables.tf`)

| Variable | Default | Description |
|---|---|---|
| `aws_access_key` | n/a | AWS access key (provided via stack vars or env) |
| `aws_secret_key` | n/a | AWS secret key (provided via stack vars or env) |
| `aws_region` | n/a | Target AWS region (set per stack) |
| `localstack_endpoint` | `http://localhost:4566` | LocalStack endpoint for local dev |
| `use_localstack` | `true` | Enables LocalStack provider endpoints and skip checks |

For detailed infrastructure-only guidance, see `infrastructure/README.md`.

### LocalStack Development

[LocalStack](https://www.localstack.cloud/) lets you provision and test the AWS resources on your local machine without incurring cloud costs.

1. Install and start LocalStack:
   ```bash
   pip install localstack
   localstack start
   ```

2. Initialise and validate with Atmos:
   ```bash
   cd infrastructure
   atmos terraform validate credit-risk-service -s orgs/environment/development/eu-west-2
   atmos terraform plan credit-risk-service -s orgs/environment/development/eu-west-2
   atmos terraform apply credit-risk-service -s orgs/environment/development/eu-west-2
   ```

3. Confirm the resources were created:
   ```bash
   atmos terraform output credit-risk-service -s orgs/environment/development/eu-west-2
   ```

### Deploying to AWS

Override the LocalStack defaults with real AWS credentials when targeting a live environment:

```bash
cd infrastructure
atmos terraform apply credit-risk-service -s orgs/environment/production/eu-west-2 \
   -- \
   -var="aws_access_key=<YOUR_ACCESS_KEY>" \
   -var="aws_secret_key=<YOUR_SECRET_KEY>" \
   -var="aws_region=eu-west-2" \
   -var="use_localstack=false"
```

> **Security tip:** Never commit real credentials to source control. Use environment variables (`TF_VAR_aws_access_key`, `TF_VAR_aws_secret_key`) or an AWS credentials file instead.

After applying, push the Docker image to the ECR repository:
```bash
# Get the ECR URL from Atmos output and copy the `ecr_repo` value
atmos terraform output credit-risk-service -s orgs/environment/production/eu-west-2

# Authenticate Docker with ECR
aws ecr get-login-password --region eu-west-2 | \
   docker login --username AWS --password-stdin <ECR_REPOSITORY_URL>

# Build and push
docker build -t credit-risk-api ./src
docker tag credit-risk-api:latest <ECR_REPOSITORY_URL>:latest
docker push <ECR_REPOSITORY_URL>:latest
```

## Development

### Running Tests

Backend tests:
```bash
cd src
python manage.py test
```

Frontend tests:
```bash
cd frontend
npm test
```

### Linting

The project includes linting configuration. To run linting:
```bash
cd src/docker
docker-compose run lint
```

### Database Migrations

Create new migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Research

The `/research` directory contains Jupyter notebooks used for:
- Exploratory Data Analysis (EDA)
- Feature engineering
- Model training and evaluation
- Credit score prediction model development

The trained model (`credit_model.sav`) is located in the `src` directory and is used by the Django application for predictions.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Harvey Allen

## Acknowledgments

- Credit risk data and initial research conducted in January 2023
- Built with Django REST Framework and React
- Machine learning model powered by scikit-learn
