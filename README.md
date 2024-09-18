# Week-4-Task-Rest-Apis

This project provides a RESTful API for managing appointments using Django and Django REST Framework. It includes user authentication and role-based access to appointment data.



## Clone the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/your-username/Week-4-Task-Rest-Apis.git
cd Week-4-Task-Rest-Apis
```

## Virtual Environment Setup

Create and activate a virtual environment:
On Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
On macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Required Packages
Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## API Endpoints

### Users

- **POST /login/**: Allows users to login. Note that patients are not allowed to login.
- **POST /users/create/**: Only admins can create new users.
- **GET /users/**: Only admins can view all users and filter users based on roles.
- **GET /users/{pk}/**: Admins can view details of a single user.
- **PUT /users/{pk}/**: Admins can update details of a single user.
- **DELETE /users/{pk}/**: Admins can delete a user.

### Appointments

- **GET /appointments/**: Admins can view all appointments, while doctors can view only their own appointments.
- **GET /appointments/{pk}/**: Admins can retrieve, delete, and update all appointments, while doctors can only view the appointments related to them.
- **GET /appointments/summary/**: Only admins can view a summary of appointments between a start date and end date, and by doctor name.
- **POST /appointments/create/**: Only admins can create new appointments by providing the IDs of the patient and doctor.

## Testing
To run the tests for the project, use the following command:

```bash
python manage.py test
```
This will execute all the test cases defined in the project to ensure everything is functioning correctly.
