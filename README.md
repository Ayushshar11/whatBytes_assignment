
# Healthcare Backend API

A RESTful healthcare backend built with Django, Django REST Framework (DRF), PostgreSQL, and JWT authentication.

## Features

- User registration and JWT login
- Authenticated patient management
- Doctor management APIs
- Patient-doctor assignment and removal
- PostgreSQL database integration
- Input validation and permission checks
- Environment-based configuration

## Tech Stack

- Python 3.10+
- Django
- Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt
- python-dotenv
- psycopg

## Project Structure

```text
HealthcareBackend/
├── accounts/
├── patients/
├── doctors/
├── config/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd HealthcareBackend
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and update the values.

Windows Command Prompt:

```cmd
copy .env.example .env
```

Generate a new Django secret key and use it in `.env`. Never commit `.env` to Git.

### 5. Create the PostgreSQL database

Open PostgreSQL using your local PostgreSQL account and run:

```sql
CREATE DATABASE healthcare_db;
```

If the database already exists, do not create it again.

Update `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in `.env` to match your local configuration.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Base URL:

`http://127.0.0.1:8000/`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |
| GET | `/api/auth/me/` | Get current user details |
| GET | `/api/auth/health/` | Health check |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List the current user's patients |
| GET | `/api/patients/<id>/` | Retrieve a patient |
| PUT/PATCH | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT/PATCH | `/api/doctors/<id>/` | Update a doctor |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

### Patient-Doctor Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List mappings for the current user |
| GET | `/api/mappings/<patient_id>/` | List doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove a mapping |

## Authentication

After logging in, use the returned access token for protected endpoints:

```http
Authorization: Bearer <ACCESS_TOKEN>
```

Send JSON request bodies with:

```http
Content-Type: application/json
```


## License

This project was developed as a Django healthcare backend assignment.
