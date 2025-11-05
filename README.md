# Project Management System (ΠΛΗ513)

A complete **web-based Project Management System (PMS)** developed as part of the course **ΠΛΗ513 – Υπηρεσίες στο Υπολογιστικό Νέφος και την Ομίχλη**.
This system implements a simplified version of tools like **Jira** or **Trello**, focusing on team collaboration, task management, and progress tracking — built using **Flask (Python)** and **PostgreSQL**.

---

## Overview

This application allows different roles of users — **Admin**, **Team Leader**, and **Team Member** — to manage teams, create and assign tasks, and collaborate through comments and notifications.

It follows a **modular microservice-inspired structure** with clear separation between:

* User Authentication
* Team Management
* Task and Comment Management
* Frontend (UI) Rendering

The backend is implemented using **Flask Blueprints**, and the frontend is composed of **Jinja2 HTML templates** integrated with CSS and JavaScript.

---

## Features and Capabilities

### Core Features

* Multi-role user authentication (Admin / Team Leader / Member)
* Session-based login/logout system
* Role-based dashboards and permissions
* Team creation and member management
* Task lifecycle tracking (TODO → IN PROGRESS → DONE)
* Task priority and deadline management
* Comment and collaboration system per task
* User activation/deactivation by Admin
* PostgreSQL relational data model
* File upload support for extensions defined in configuration
* HTML/Jinja2 templating and static asset management

### Admin Panel

* Manage all users (activate, deactivate, change roles)
* Create, delete, and view teams
* Assign team leaders
* View all projects and tasks across the system

### Team Leader Dashboard

* Create and manage teams
* Add or remove team members
* Create, assign, edit, or delete tasks
* Add comments on tasks
* View aggregated team tasks and statuses

### Team Member Dashboard

* View assigned tasks with deadlines and priorities
* Comment on tasks
* Change task status (TODO, IN_PROGRESS, DONE)
* See team membership and leader information
* Receive updates and notifications about deadlines and comments

---

## Project Structure

```
Project/
│
├── backend_server_app.py                 # Main Flask application entry point; registers all blueprints
├── config.py                             # Central configuration for DB, secret keys, and paths
├── db.py                                 # Database connection logic (PostgreSQL / SQLite)
├── requirements.txt                      # Python dependencies for the backend
├── source_run_flash.sh                   # Shell script to start the Flask server
│
├── database_sql/                         # Database schema and setup files
│   ├── create_tables.sql                 # SQL script for creating tables and inserting initial data
│   └── database.db                       # SQLite or PostgreSQL export (sample database)
│
├── routes/                               # Flask Blueprints (Microservices logic)
│   ├── homepage.py                       # Landing page and role selection routes
│   ├── admin_authenticate.py             # Admin login, signup, and authentication routes
│   ├── admin_mainpage.py                 # Admin main dashboard & management functions
│   ├── admin_teamLeader_member_options.py# Handles transitions between user roles
│   ├── teamLeader_authenticate.py        # Team Leader login/signup and authentication
│   ├── teamLeader_mainpage.py            # Team Leader dashboard & task management routes
│   ├── member_authenticate.py            # Member authentication routes (login/signup)
│   └── member_mainpage.py                # Member dashboard, tasks, and comments routes
│
├── static/                               # Static resources (CSS, JS, images, uploads)
│   ├── css/
│   │   ├── style.css                     # General layout and color scheme
│   │   ├── mainpage.css                  # Dashboard layout and overview styling
│   │   ├── teamLeader.css                # Team Leader page styling
│   │   ├── admin.css                     # Admin interface styles
│   │   └── member.css                    # Member UI and forms styling
│   │
│   ├── script/
│   │   └── script.js                     # Global client-side scripts (buttons, alerts, etc.)
│   │
│   ├── images/
│   │   └── icon_pms.svg                  # Application logo / favicon
│   │
│   └── uploads/                          # Uploaded attachments (user files, comments)
│
├── templates/                            # Jinja2 HTML templates for Flask frontend
│   ├── index.html                        # Homepage (role selection and intro)
│   ├── admin_login.html                  # Admin login form
│   ├── admin_signup.html                 # Admin signup form
│   ├── admin_mainpage.html               # Admin dashboard view
│   ├── admin_manageUsers.html            # Admin panel for managing user accounts
│   ├── admin_manageTeams.html            # Admin interface for team creation/deletion
│   ├── admin_show_tasks.html             # Admin view of all tasks and projects
│   ├── admin_or_teamLeader_or_member.html# Common page for selecting user role
│   ├── teamLeader_mainpage.html          # Team Leader main dashboard
│   ├── teamLeader_teamDetails.html       # Detailed view of a specific team and its members
│   ├── teamLeader_manageTasks.html       # Manage team tasks (create/edit/delete)
│   ├── teamLeader_viewTask.html          # Task detail page for Team Leader
│   ├── edit_task.html                    # Task editing interface (Team Leader)
│   ├── view_task.html                    # View task details (generic)
│   ├── member_mainpage.html              # Member main page (overview of personal tasks)
│   ├── member_viewTasks.html             # View all assigned tasks
│   ├── member_viewTask.html              # Task detail view for member
│   ├── member_addComment.html            # Add comments to tasks
│   ├── member_notifications.html         # View notifications and deadlines
│   ├── member_teamsIncluded.html         # View all teams a member belongs to
│   ├── member_viewTeam.html              # Detailed team view for member
│   ├── teamLeader_login.html             # Team Leader login page
│   ├── teamLeader_signup.html            # Team Leader signup page
│   ├── member_login.html                 # Member login page
│   └── member_signup.html                # Member signup page
│
├── utils/
│   └── file_utils.py                     # Helper for file handling and uploads
│
├── __pycache__/                          # Compiled Python cache directories (auto-generated)
│   └── *.pyc                             # Bytecode-compiled Python files
│
└── venv/                                 # Virtual environment for Python dependencies
    ├── bin/                              # Executables and activation scripts
    ├── Lib/                              # Installed Python packages (Flask, psycopg2, etc.)
    ├── Include/                          # C headers for installed modules
    └── pyvenv.cfg                        # Virtual environment configuration file                              # Virtual environment (optional)
```

---

## Database Schema

The PostgreSQL schema is defined in **`create_tables.sql`** and includes:

| Table            | Description                                               |
| ---------------- | --------------------------------------------------------- |
| **users**        | Stores all system users (admins, leaders, members)        |
| **teams**        | Represents team entities with assigned leaders            |
| **team_members** | Many-to-many relationship between teams and users         |
| **tasks**        | Represents team tasks with priority, status, and due date |
| **comments**     | Stores user comments per task (with timestamps)           |

To initialize the database:

```bash
psql -U postgres -d project_db -f databe_sql/create_tables.sql
```

---

## Configuration

File: `config.py`

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "project_db",
    "user": "postgres",
    "password": "your_password"
}

SECRET_KEY = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
```

---

## Installation & Execution

### 1. Clone the Repository

```bash
git clone https://github.com/stamatis-mavitzis/project-management-system.git
cd project-management-system
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Update credentials in `config.py` and create the database schema:

```bash
psql -U postgres -d project_db -f databe_sql/create_tables.sql
```

### 5. Run Flask Application

```bash
source source_run_flash.sh
# or manually:
python3 backend_server_app.py
```

### 6. Access Application

Open your browser at:

```
http://127.0.0.1:5000/
```

---

## Role Functionality Summary

| Role            | Capabilities                                                |
| --------------- | ----------------------------------------------------------- |
| **Admin**       | Manage users, teams, and roles; view all projects and tasks |
| **Team Leader** | Manage teams, create tasks, edit tasks, add comments        |
| **Team Member** | View assigned tasks, change task status, comment            |

---

## Tech Stack

| Layer             | Technology                               |
| ----------------- | ---------------------------------------- |
| **Backend**       | Python 3, Flask                          |
| **Database**      | PostgreSQL                               |
| **Frontend**      | HTML, CSS, JavaScript, Jinja2            |
| **Hosting Ready** | Docker-compatible structure              |
| **Libraries**     | Flask, psycopg2-binary, Werkzeug, Jinja2 |

---

## Development and Deployment

### Local Development

Run all Flask services through `source_run_flash.sh` for quick setup.

### Docker Deployment (optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
```

Run:

```bash
docker build -t pms-app .
docker run -p 5000:5000 pms-app
```

---

## Author

**Stamatios Mavitzis**
Student ID: *2018030040*
Course: *ΠΛΗ513 – Υπηρεσίες στο Υπολογιστικό Νέφος και την Ομίχλη*
Technical University of Crete

---

## License

This project is open-source and distributed for **educational and academic use** only.
