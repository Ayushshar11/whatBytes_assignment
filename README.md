# Healthcare Backend API

A Django REST API for managing patient records, doctor information, and patient-doctor assignments. This project was developed as part of a campus recruitment assignment to demonstrate backend development, REST API design, authentication, and database management.

## Project Overview

The application provides APIs for user registration and login, patient record management, doctor management, and assigning doctors to patients.

It uses Django REST Framework to handle API requests, PostgreSQL for data storage, and JWT authentication to protect endpoints that require a logged-in user.

## Tech Stack

- **Language:** Python
- **Backend Framework:** Django
- **API Framework:** Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JSON Web Tokens (JWT)
- **JWT Package:** djangorestframework-simplejwt
- **Database Access:** Django ORM
- **API Testing:** Postman and Django REST Framework testing utilities

## Features

- User registration and login.
- JWT-based authentication for protected APIs.
- Create, view, update, and delete patient records.
- Manage doctor records through REST APIs.
- Assign doctors to patients and remove assignments.
- Input validation and appropriate error responses.
- Access control for patient records.
- PostgreSQL database integration.

## Project Structure

```text
HealthcareBackend/
├── accounts/
│   ├── migrations/
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── doctors/
│   ├── migrations/
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── patients/
│   ├── migrations/
│   ├── mapping_urls.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

The structure above summarizes the main project files. Some additional files may be present in individual applications.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or a compatible version supported by the project dependencies.
- PostgreSQL.
- Git.
- Postman or another API client for testing the endpoints.

### 1. Clone the repository

```bash
git clone https://github.com/Ayushshar11/whatBytes_assignment.git
cd whatBytes_assignment
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On Git Bash, you can activate it using:

```bash
source .venv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database for the project.

Copy `.env.example` to `.env` and update the values according to your local database configuration.

Keep the actual `.env` file private. Do not commit database passwords or Django secret keys to GitHub.

Make sure the environment variable names in `.env` match those read by `config/settings.py`.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The local API server will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

All endpoints below use the `/api/` prefix.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Log in and obtain JWT tokens |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List the authenticated user's patients |
| GET | `/api/patients/<id>/` | Retrieve a patient |
| PUT | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

### Patient-Doctor Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List accessible mappings |
| GET | `/api/mappings/<patient_id>/` | Get doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove a patient-doctor assignment |

## Authentication

The login endpoint returns JWT tokens when valid credentials are supplied.

For protected endpoints, include the access token in the request headers:

```http
Authorization: Bearer <access_token>
```

Use the access token for authenticated API requests. If it expires, obtain a new one using the token refresh endpoint if configured.

## Testing

Run the project's automated tests with:

```bash
python manage.py test
```

Check the Django configuration with:

```bash
python manage.py check
```

To check whether model changes require new migrations:

```bash
python manage.py makemigrations --check --dry-run
```

API endpoints can also be tested using Postman. Test successful requests, invalid input, missing authentication, and attempts to access records belonging to another user.

## Security and Configuration

- Database credentials and other sensitive settings should be supplied through environment variables.
- Passwords should be stored using Django's password-hashing mechanism.
- JWT authentication is used for protected API requests.
- Patient record access should follow the ownership and permission rules implemented in the application.

## Author

**Ayush Sharma**

GitHub: [Ayushshar11](https://github.com/Ayushshar11)

## Assignment

Developed as part of a campus recruitment assignment focused on building a healthcare backend using Django REST Framework and PostgreSQL.
