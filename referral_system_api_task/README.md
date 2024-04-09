# Django Referral System API

This project is a Django-based Referral System API that allows users to register, view their details, and view their referrals. The API is built using Django Rest Framework and is designed to be easily deployable using Docker.

## Features

- User Registration Endpoint
- User Details Endpoint
- Referrals Endpoint
- Token-based Authentication
- Docker & Docker Compose for easy deployment
- Unit tests for each endpoint
- Well-documented API endpoints

## Setup

1. **Clone the repository:**
   ```bash
   https://github.com/jay-chhaniyara/referral_system_api_task.git
   cd referral_system_api_task

2. **Create a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Apply database migrations:**
    ```bash
    python manage.py migrate

5. **Run the development server:**
    ```bash
    python manage.py runserver

## API Endpoints

### User Registration

- **URL:** `/api/register/`
- **Method:** `POST`
- **Description:** Register a new user.
- **Request Body:**
  ```json
  {
    "name": "Test Name",
    "email": "test@example.com",
    "password": "password123",
    "referral_code": "ABCD1234"
  }

### User Login

- **URL:** `/api/login/`
- **Method:** `POST`
- **Description:** Login to the system to obtain an authentication token
- **Request Body:**
  ```json
  {
    "email": "test@example.com",
    "password": "password123",
  }

### User Details

- **URL:** `/api/user-details/`
- **Method:** `GET`
- **Description:** Get details of the authenticated user.
- **Headers:** Authorization: Bearer `<token>`

### User Details

- **URL:** `/api/referrals/`
- **Method:** `GET`
- **Description:** Get referrals users list of  the authenticated user.
- **Headers:** Authorization: Bearer `<token>`