# Healthcare Backend API

A Django REST Framework API for user authentication, patient records, doctor
records, and patient-doctor assignments. The project uses PostgreSQL through
the Django ORM and JWT bearer tokens for API authentication.

## Technologies

- Python 3.10+
- Django 5.2
- Django REST Framework
- PostgreSQL with psycopg 3
- `djangorestframework-simplejwt`
- `python-dotenv`

## Project structure

```text
accounts/       Registration, email login, and current-user endpoints
patients/       Patient records and patient-doctor mappings
doctors/        Doctor records
config/         Django settings and root URL configuration
manage.py       Django management commands
requirements.txt
.env.example    Environment variable template
```

## Local setup on Windows

### Prerequisites

Install Python 3.10 or newer and PostgreSQL. Ensure the PostgreSQL service is
running and that you know the database username and password.

### Create the database

For example, connect to your local PostgreSQL server:

```powershell
psql -U postgres
```

Then create the development database:

```sql
CREATE DATABASE healthcare_db;
```

Use your own PostgreSQL username, password, host, and port if they differ from
the example values below.

### Create an environment and install dependencies

Run these commands from the repository directory:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment variables

Create a local `.env` file from the template:

```powershell
Copy-Item .env.example .env
```

Generate a secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Update `.env` with the generated `DJANGO_SECRET_KEY` and your PostgreSQL
credentials. The template contains placeholders and is not suitable for
production. `.env` is excluded from Git.

```dotenv
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=True
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

### Apply migrations and run

```powershell
python manage.py migrate
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`. The Django admin is at
`http://127.0.0.1:8000/admin/`; create an administrator with
`python manage.py createsuperuser` if needed.

## API endpoints

All API paths below are relative to `http://127.0.0.1:8000`.

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| POST | `/api/auth/register/` | No | Register an account |
| POST | `/api/auth/login/` | No | Obtain access and refresh JWTs using email/password |
| POST | `/api/auth/token/refresh/` | No | Obtain a new access token |
| GET | `/api/auth/me/` | JWT | Get the authenticated user's details |
| GET | `/api/auth/health/` | No | API health response |
| POST | `/api/patients/` | JWT | Create a patient owned by the authenticated user |
| GET | `/api/patients/` | JWT | List the authenticated user's patients |
| GET | `/api/patients/<id>/` | JWT | Retrieve an owned patient |
| PUT, PATCH | `/api/patients/<id>/` | JWT | Update an owned patient |
| DELETE | `/api/patients/<id>/` | JWT | Delete an owned patient |
| POST | `/api/doctors/` | JWT | Create a doctor |
| GET | `/api/doctors/` | JWT | List doctors |
| GET | `/api/doctors/<id>/` | JWT | Retrieve a doctor |
| PUT, PATCH | `/api/doctors/<id>/` | JWT | Update a doctor |
| DELETE | `/api/doctors/<id>/` | JWT | Delete a doctor |
| POST | `/api/mappings/` | JWT | Assign a doctor to an owned patient |
| GET | `/api/mappings/` | JWT | List mappings for the authenticated user's patients |
| GET | `/api/mappings/<patient_id>/` | JWT | List doctors assigned to an owned patient |
| DELETE | `/api/mappings/<mapping_id>/` | JWT | Delete a mapping for an owned patient |

Authenticated users may manage doctor records. A patient can only be accessed
by its owner; mapping list, detail, creation, and deletion are restricted to
the same owner. Assigning the same doctor to a patient more than once is
rejected.

## Authentication and examples

Register with a name, email, and password:

```http
POST /api/auth/register/
Content-Type: application/json
```

```json
{
  "name": "Jordan Smith",
  "email": "jordan@example.com",
  "password": "a-strong-password"
}
```

Registration returns the created user's public fields (including `id`, `name`,
`first_name`, `last_name`, and `email`); it never returns the password.

Example response shape:

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "Jordan Smith",
    "first_name": "Jordan Smith",
    "last_name": "",
    "email": "jordan@example.com"
  }
}
```

Log in with the same email and password:

```http
POST /api/auth/login/
Content-Type: application/json
```

```json
{
  "email": "jordan@example.com",
  "password": "a-strong-password"
}
```

The login response contains `access` and `refresh` token fields:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Send the access token on protected requests:

```http
Authorization: Bearer <access-token>
```

Create a patient with the access token; ownership is assigned from the token,
not from a client-supplied user ID:

```http
POST /api/patients/
Content-Type: application/json
Authorization: Bearer <access-token>
```

```json
{
  "name": "Jordan Smith",
  "age": 35,
  "gender": "Other",
  "address": "12 Sample Street",
  "phone": "+911234567890",
  "medical_history": "No known allergies"
}
```

Assign a doctor by using existing patient and doctor IDs:

```json
{
  "patient": 1,
  "doctor": 1
}
```

The patient and doctor IDs above are illustrative; use IDs returned by this
API.

## Checks and automated tests

With the virtual environment activated and `.env` configured, run:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Django creates a separate test database using the configured PostgreSQL
connection. The test suite does not use the development database for test data.
