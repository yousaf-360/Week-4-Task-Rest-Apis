# Week-4-Task-Rest-Apis

This project provides a RESTful API for managing appointments using Django and Django REST Framework. It includes user authentication and role-based access to appointment data.

## Table of Contents

- [Project Setup](#project-setup)
- [API Endpoints](#api-endpoints)
  - [ssers](#users)
  - [appointments](#appointments)

## Project Setup

### 1. Clone the Repository

Clone the project repository from GitHub:

```bash
git clone https://github.com/your-username/Week-4-Task-Rest-Apis.git
cd Week-4-Task-Rest-Apis
2. Set Up the Virtual Environment
Create and activate a virtual environment:

On Windows:
bash
Copy code
python -m venv .venv
.venv\Scripts\activate
On macOS/Linux:
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
3. Install Required Packages
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
4. Apply Migrations
Apply the database migrations:

bash
Copy code
python manage.py migrate
5. Create a Superuser
Create a superuser to access the Django admin interface:

bash
python manage.py createsuperuser
6. Run the Development Server
Start the development server:

bash
python manage.py runserver
API Endpoints

Users
POST /login/: Allows users to login. Note that patients are not allowed to login.
POST /users/create/: Only admin can create new users.
GET /users/: Only admin can view all users and view users based on roles.
GET /users/int:pk/: Admin can view details of a single user.
PUT /users/int:pk/: Admin can update details of a single user.
DELETE /users/int:pk/: Admin can delete a user.
Appointments
GET /appointments/: Admins can view all appointments, while doctors can view only their own appointments.
GET /appointments/int:pk/: Admins can retrieve, delete, and update all appointments, while doctors can only view the appointments related to them.
GET /appointments/summary/: Only admin can view a summary of appointments between a start date and end date, and by doctor name.
POST /appointments/create/: Only admin can create new appointments by providing the IDs of the patient and doctor.
Testing
To run the tests for the project, use the following command:
bash
python manage.py test
This will execute all the test cases defined in the project to ensure everything is functioning correctly.
