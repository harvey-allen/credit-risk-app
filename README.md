# Django REST Credit Scoring API

This Django REST framework API calculates credit scores based on various credit risk parameters. Users can input both categorical and numerical data to obtain a credit score.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features

- Accepts credit risk parameters, including both categorical and numerical data.
- Calculates credit scores based on input data.
- Provides a RESTful API for interacting with the application.
- Customizable and extensible for different credit scoring models.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- Django
- Django REST framework
- Docker (optional for containerization)

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/harvey-allen/credit-risk-api.git
   cd credit-risk-api
   
2. Install project dependencies:
   ```bash
   pip install -r requirements.txt

### Running the App

1. Migrate the database:

   ```bash
   python manage.py migrate

2. Create a superuser account for admin access (optional):
   ```bash
   python manage.py createsuperuser

3. python manage.py runserver
   ```bash
   python manage.py runserver

## Usage

1. Create credit risk parameter records using the Django admin interface or API.
2. Use the API to calculate credit scores based on the provided data.

## API Endpoints

- List credit parameters: `/api/calculate/`
- Create credit parameter: `/api/calculate/create/`

For detailed API documentation, refer to the API documentation (link here).

## Customization

- Implement your custom credit scoring model.
- Modify the model fields and validation in `serializers.py` for specific requirements.

## Contributing

Contributions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).




