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

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using Docker (Recommended)](#using-docker-recommended)
  - [Manual Setup](#manual-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
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

2. Create a `.env` file in the `src` directory:
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

## 📁 Project Structure

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
└── README.md                     # This file
```

## 📚 API Documentation

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

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Harvey Allen

## Acknowledgments

- Credit risk data and initial research conducted in January 2023
- Built with Django REST Framework and React
- Machine learning model powered by scikit-learn
