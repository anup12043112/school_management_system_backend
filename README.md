# School Management System — Backend

A RESTful backend for a School Management System built with Django and Django REST Framework. It provides role-based access and APIs for managing students, teachers, parents, sections, subjects, marks, attendance, and notices.

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework (DRF)**
- **Simple JWT** — JWT-based authentication
- **django-filter** — API filtering
- **django-cors-headers** — Cross-origin requests
- **PostgreSQL support** — psycopg
- **SQLite** — Local development database

## Features

- Role-based access for Admin, Teacher, Student, and Parent.
- JWT authentication and protected API endpoints.
- Student, teacher, parent, and section management.
- Subject and teaching assignment management.
- Examination marks management.
- Attendance tracking.
- Notice management.
- Search, filtering, sorting, and pagination where implemented.
- Permission-based access to protected resources.

## Project Structure

```text
Backend/
├── Backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── myApp/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

*The exact files inside `myApp/` may vary as the project evolves.*

## Prerequisites

- Python 3.13 or a compatible Python version.
- pip.
- Git.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/anup12043112/school_management_system_backend
cd Backend
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the backend root directory, alongside `manage.py`.

```env
DJANGO_SECRET_KEY="replace-with-a-new-secret-key"
```

Use a secure, randomly generated secret key for your own environment. Never commit `.env` to Git.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the account.

### 7. Start the development server

```bash
python manage.py runserver
```

The backend will normally be available at:

```text
http://127.0.0.1:8000/
```

## API Configuration

The frontend communicates with the backend through HTTP API requests. Authentication and permissions are enforced by the backend for protected endpoints.

During local development, the frontend origin is configured in Django's CORS settings. Update it if your frontend runs at a different origin.

## Environment and Security

- Keep `.env` and secret keys out of version control.
- Use a separate secret key for each environment.
- Configure `DEBUG`, `ALLOWED_HOSTS`, CORS, and CSRF settings appropriately before deployment.
- Use a production-ready database configuration when deploying.
- Never commit database credentials, access tokens, or other secrets.

## Development Status

This repository contains the backend for the School Management System. Deployment and production configuration may require additional setup.

## License

No license has been specified yet. All rights reserved unless a license is added to this repository.
