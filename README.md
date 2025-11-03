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
├── backend_server_app.py                 # Flask application entry point and blueprint registration
├── config.py                             # Configuration for database, secrets, upload paths
├── db.py                                 # PostgreSQL connection and error handling
├── requirements.txt                      # Python dependencies
├── source_run_flash.sh                   # Shell script to launch Flask server
│
├── databe_sql/
│   ├── create_tables.sql                 # SQL schema and initial dataset
│   └── database.db                       # Optional database export
│
├── routes/                               # Modular Flask blueprints
│   ├── homepage.py                       # Entry route for role selection
│   ├── admin_authenticate.py             # Admin signup/login/logout
│   ├── admin_mainpage.py                 # Admin dashboard and management actions
│   ├── admin_teamLeader_member_options.py# Role selection pages
│   ├── teamLeader_authenticate.py        # Team Leader authentication routes
│   ├── teamLeader_mainpage.py            # Team Leader task and team management
│   ├── member_authenticate.py            # Member authentication routes
│   └── member_mainpage.py                # Member dashboard and task management
│
├── static/                               # Static assets (CSS, JS, uploads)
│   ├── css/
│   │   ├── style.css
│   │   └── style2.css
│   ├── script/
│   │   └── script.js
│   └── uploads/                          # Uploaded user files
│
├── templates/                            # HTML pages (Jinja2)
│   ├── index.html                        # Homepage
│   ├── admin_login.html
│   ├── admin_mainpage.html
│   ├── admin_manageUsers.html
│   ├── admin_manageTeams.html
│   ├── admin_show_tasks_and_projects.html
│   ├── admin_or_teamLeader_or_member.html
│   ├── teamLeader_mainpage.html
│   ├── teamLeader_teamDetails.html
│   ├── teamLeader_manageTasksProjects.html
│   ├── member_mainpage.html
│   ├── member_viewTasks.html
│   ├── member_viewTask.html
│   ├── member_addComment.html
│   ├── member_notifications_and_deadlines.html
│   ├── member_teamsIncluded.html
│   ├── member_viewTeam.html
│   ├── signup and login forms (for all roles)
│   └── other helper templates
│
├── utils/
│   └── file_utils.py                     # File validation and upload handling
│
└── venv/                                 # Virtual environment (optional)
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
