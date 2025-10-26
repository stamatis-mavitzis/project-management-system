# Project Management System (ΠΛΗ513)

A web-based Project Management System (PMS) developed for the course ΠΛΗ513 – Υπηρεσίες στο Υπολογιστικό Νέφος και την Ομίχλη.  
The system supports multiple user roles — Admin, Team Leader, and Team Member — allowing the management of teams, tasks, and comments.

## Features

- User Authentication and Role Management
- Admin Panel for managing users, teams, and roles
- Team Leader Dashboard for creating and managing teams and tasks
- Task creation, assignment, and status tracking
- Comment system for tasks
- PostgreSQL database integration
- HTML/CSS/Jinja2 frontend templates
- Flask backend application

## Project Structure

Project/
|-- backend_server_app.py           # Flask application entry point
|-- config.py                       # Configuration (DB credentials)
|-- db.py                           # PostgreSQL connection handler
|-- README.md                       # The README file
|-- source_run_flash.sh             # This file runs all the commands to run flask
|-- requirements.txt                # required libraries for the app
|-- databe_sql/                     
|     |-- create_tables.sql         # This script creates the tables and fills some data
|-- routes/                         # The routes which implement the app
|     |-- admin_authenticate.py
|     |-- admin_mainpage.py
|     |-- admin_teamLeader_member_options.py
|     |-- homepage.py
|     |-- member_authenticate.py
|     |-- member_mainpage.py
|     |-- teamLeader_authenticate.py
|     |-- teamLeader_mainpage.py
|-- static/                         #styling, javascript and user upload files
|     |-- css/
|     |     |-- style.css
|     |     |-- style2.css
|     |-- script/
|     |     |-- script.js
|     |-- uploads/
|-- templates/                   # All the html pages
|     |-- admin_login.html
|     |-- admin_mainpage.html
|     |-- admin_manageTeams.html
|     |-- admin_manageUsers.html
|     |-- admin_or_teamLeader_or_member.html
|     |-- admin_show_tasks_and_projects.html
|     |-- index.html
|     |-- member_addComment.html
|     |-- member_login.html
|     |-- member_mainpage.html
|     |-- member_notifications_and_deadlines.html
|     |-- member_signin_or_login.html
|     |-- member_signup.html
|     |-- member_teamsIncluded.html
|     |-- member_viewTask.html
|     |-- member_viewTasks.html
|     |-- member_viewTeam.html
|     |-- teamLeader_editTask.html
|     |-- teamLeader_login.html
|     |-- teamLeader_mainpage.html
|     |-- teamLeader_manageTasksProjects.html
|     |-- teamLeader_manageTeams.html
|     |-- teamLeader_signin_or_login.html
|     |-- teamLeader_signup.html
|     |-- teamLeader_teamDetails.html
|     |-- teamLeader_viewTask.html
|-- utils/
|     |-- file_utils.py       # Declare the file type for uploading
| -- venv/                    # Python virtual environment



## Database Schema

Run the SQL script create_tables.sql before launching the app.

Example:
psql -U postgres -d project_db -f create_tables.sql

Main tables:
- users
- teams
- team_members
- tasks
- comments
- attachments

## Installation and Setup

1. Clone the Repository
   git clone https://github.com/stamatis-mavitzis/project-management-system.git
   cd project-management-system

2. Create Virtual Environment
   python3 -m venv venv
   source venv/bin/activate   # Linux or macOS
   venv\Scripts\activate      # Windows

3. Install Dependencies
   pip install -r requirements.txt

4. Database Configuration
   Edit the file config.py and update your PostgreSQL credentials:
   DB_CONFIG = {
       "dbname": "project_db",
       "user": "postgres",
       "password": "your_password",
       "host": "localhost",
       "port": "5432"
   }

5. Initialize the Database
   psql -U postgres -d project_db -f create_tables.sql

6. Make the source_run_flask.sh executable
   chmod +x source_run_flask.sh

7. Run the Application
   source source_run_flask.sh

8. Access the app at http://127.0.0.1:5000/

## Required Libraries

List of dependencies (defined in requirements.txt):

Flask
psycopg2-binary
python-dotenv
Werkzeug
Jinja2

Install with:
pip install -r requirements.txt

## User Roles Overview

   Role     | Permissions
------------|-----------------------------------------------
Admin       | Manage users, teams, and roles
Team Leader | Manage teams, assign tasks, comment on tasks
Team Member | View assigned tasks, comment on tasks

## Usage Guide

1. Start the Flask app.
2. Open the home page / and select your role (Admin, Team Leader, or Member).
3. Admins can:
   - Approve or deactivate users
   - Create teams and assign leaders
4. Team Leaders can:
   - Manage teams and members
   - Create, assign, and edit tasks
5. Members can:
   - View assigned tasks
   - Add comments

## Folder Explanation

Folder/File       | Description
------------------|-------------
/static/css       | CSS stylesheets
/static/script    | JavaScript files
/templates        | Jinja2 HTML templates
db.py             | Database connection functions
config.py         | App configuration settings
admin_*.py        | Admin-related functionality
teamLeader_*.py   | Team Leader functionality
member_*.py       | Member functionality
homepage.py       | Homepage and role routing

## Optional: Docker Setup

You can containerize the application using Docker.

Example Dockerfile:
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]

Build and run:
docker build -t pms-app .
docker run -p 5000:5000 pms-app

## Authors

Stamatios Mavitzis
2018030040 

For course ΠΛΗ513 – Υπηρεσίες στο Υπολογιστικό Νέφος και την Ομίχλη

## License

This project is open-source and provided for educational purposes.
