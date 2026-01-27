# Credit Risk Assessment - Frontend

This is the React frontend for the Credit Risk Assessment application.

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run the Development Server

```bash
npm start
```

The app will run on [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm build
```

## Features

- Credit parameters form with all required fields
- Real-time validation
- Communicates with Django backend API
- Displays credit score prediction results

## API Configuration

The frontend is configured to proxy API requests to `http://localhost:8000` (Django backend).
Make sure your Django server is running before submitting the form.
