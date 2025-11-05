# Project Management System (ΠΛΗ513)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-3.0-lightgrey)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue)
![Docker](https://img.shields.io/badge/docker-compose-blue)
![License](https://img.shields.io/badge/license-Educational-green)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [User Roles & Permissions](#user-roles--permissions)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Quickstart Guide](#quickstart-guide)
- [Docker Deployment](#docker-deployment)
- [GCP Deployment (Ubuntu VM)](#gcp-deployment-ubuntu-vm)
- [API Overview & Examples](#api-overview--examples)
- [Security & Error Handling](#security--error-handling)
- [Troubleshooting](#troubleshooting)
- [Contributing & Roadmap](#contributing--roadmap)
- [Credits & License](#credits--license)
- [Database Recreation Script](#database-recreation-script)
---

## Overview

The Project Management System (PMS) is a web platform designed to streamline teamwork and task management.  
Developed as part of the ΠΛΗ513 – Services in Cloud and Fog Computing course at the Technical University of Crete, it emulates simplified functionality of tools like Jira or Trello, focusing on collaboration, progress tracking, and team communication.

The system supports different user roles (Admin, Team Leader, Team Member) and allows the creation, assignment, and monitoring of tasks in an organized environment.

---

## Features

### Core Capabilities
- Multi-role user authentication (Admin / Team Leader / Member)
- Team and member management
- Task lifecycle tracking (TODO → IN PROGRESS → DONE)
- Deadlines and task priorities
- Comment and discussion threads
- File uploads for task attachments
- Notifications for comments or changes

### Optional / Bonus Features
- Dashboard analytics and team progress charts
- File attachments in comments
- Real-time notifications via WebSockets (optional)

---

## System Architecture

The PMS follows a modular architecture consisting of:

- Frontend Layer: Jinja2 templates, HTML/CSS/JS
- Backend Layer: Flask blueprints for modular services
- Database Layer: PostgreSQL relational schema

### Data Flow
```
User → Flask Routes (Blueprints) → Service Logic → PostgreSQL DB
```

### Main Components
| Component       | Description                               |
|-----------------|-------------------------------------------|
| Auth Service    | Manages user authentication and sessions  |
| Team Service    | Handles teams and members                 |
| Task Service    | Manages tasks and statuses                |
| Comment Service | Adds comments to tasks                    |

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

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3.12, Flask 3.0            |
| Database    | PostgreSQL 16                     |
| Frontend    | HTML5, CSS3, JavaScript, Jinja2   |
| Deployment  | Docker & Docker Compose           |
| Hosting     | Google Cloud Platform (Ubuntu VM) |

---

## User Roles & Permissions

| Role        | Capabilities                                              |
|-------------|-----------------------------------------------------------|
| Admin       | Approve users, assign roles, manage all teams and tasks   |
| Team Leader | Create/edit tasks, manage team, comment on tasks          |
| Member      | View and update assigned tasks, add comments              |

---

## Database Schema

### Entities

The PostgreSQL schema is defined in **`create_tables.sql`** and includes:

| Table            | Description                                               |
| ---------------- | --------------------------------------------------------- |
| **users**        | Stores all system users (admins, leaders, members)        |
| **teams**        | Represents team entities with assigned leaders            |
| **team_members** | Many-to-many relationship between teams and users         |
| **tasks**        | Represents team tasks with priority, status, and due date |
| **comments**     | Stores user comments per task (with timestamps)           |


- users(user_id, username, email, password, role, is_active)
- teams(team_id, name, description, leader_id, created_at)
- team_members(team_id, user_id) (many-to-many)
- tasks(task_id, title, description, status, priority, due_date, created_by, assigned_to)
- comments(comment_id, task_id, user_id, text, created_at)

To initialize the database:

```bash
psql -U postgres -d project_db -f databe_sql/create_tables.sql
```

Initialize schema and data (sequentially):

```bash
psql -U postgres -d project_db -f databe_sql/create_tables.sql
psql -U postgres -d project_db -f databe_sql/create_data.sql
```



### ER Diagram (conceptual)
```
Users ---< TeamMembers >--- Teams
Teams ---< Tasks >--- Comments
```

---

## Configuration

Example: `config.py`
```python
DB_CONFIG = {
    "host": "localhost",
    "database": "project_db",
    "user": "postgres",
    "password": "xotour"
}
SECRET_KEY = "supersecretkey"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "pdf"}
```

---

## Quickstart Guide

### Local Environment

```bash
git clone https://github.com/stamatis-mavitzis/project-management-system.git
cd project-management-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
psql -U postgres -d project_db -f database_sql/create_tables.sql
python backend_server_app.py
```
Then visit: **http://127.0.0.1:5000**

---

## Docker Deployment

This project includes a Docker Compose setup running both Flask & PostgreSQL.

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    container_name: project_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: xotour
      POSTGRES_DB: postgres
    ports:
      - "5433:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./database_sql/create_tables.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
      timeout: 5s
    restart: unless-stopped

  web:
    build: .
    container_name: project_app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      FLASK_APP: backend_server_app.py
      FLASK_ENV: development
      DB_HOST: db
      DB_USER: postgres
      DB_PASSWORD: xotour
      DB_NAME: postgres
    command: flask run --host=0.0.0.0 --port=5000
    restart: unless-stopped

volumes:
  pgdata:
```

Run:
```bash
docker compose up --build
```

Stop:
```bash
docker compose down
```

Access App: [http://localhost:5000](http://localhost:5000)

---

## GCP Deployment (Ubuntu VM)

1. **Create a VM Instance**
   - Platform: Google Cloud Console → Compute Engine → VM Instances
   - OS: Ubuntu 22.04 LTS
   - Firewall: Allow HTTP/HTTPS traffic

2. **Connect via SSH**
```bash
gcloud compute ssh <instance-name> --zone=<your-zone>
```

3. **Install Dependencies**
```bash
sudo apt update && sudo apt install -y docker.io docker-compose git
```

4. **Clone the Repository**
```bash
git clone https://github.com/stamatis-mavitzis/project-management-system.git
cd project-management-system
```

5. **Run the App**
```bash
sudo docker compose up --build -d
```

6. **Open Port**
Ensure port 5000 is open under VPC Network → Firewall Rules.

Access the app at:
```
http://<VM_EXTERNAL_IP>:5000
```

---

## API Overview & Examples

### Auth Service
**POST /signup**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secret",
  "role": "member"
}
```
Response:
```json
{"message": "User created successfully. Awaiting admin approval."}
```

**POST /login**
```json
{"username": "john_doe", "password": "secret"}
```
Response:
```json
{"message": "Login successful", "role": "Team Leader"}
```

---

### Team Service
**POST /teams** (Admin only)
```json
{"team_name": "DevOps", "description": "CI/CD team", "leader_id": 3}
```

**GET /teams**
Returns all teams related to the logged-in user.

---

### Task Service
**POST /tasks**
```json
{
  "title": "Implement Login",
  "description": "Add authentication",
  "assigned_to": 5,
  "priority": "High",
  "due_date": "2025-12-01"
}
```

**PATCH /tasks/5**
```json
{"status": "DONE"}
```

---

### Comment Service
**POST /tasks/<task_id>/comments**
```json
{"comment_text": "Testing completed", "user_id": 4}
```

**GET /tasks/<task_id>/comments**
Retrieves all comments for the specified task.

---

## Security & Error Handling

- Passwords hashed using Werkzeug.
- Flask session-based authentication.
- Input validation for SQL safety.
- Custom error messages and flash notifications.

Error example:
```json
{"error": "Invalid credentials"}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|--------|--------|-----------|
| Port 5000 busy | Another app running | Change host port in docker-compose.yml |
| Database connection error | Postgres not healthy | Run `docker compose logs db` |
| Flask not reloading | Missing volume bind | Ensure `- .:/app` is included |

---

## Contributing & Roadmap

### How to Contribute
1. Fork the repo  
2. Create a feature branch (`feature/new-module`)  
3. Commit changes (`git commit -m "Add new feature"`)  
4. Push and create a Pull Request

### Roadmap
- [ ] Add RESTful API documentation (Swagger/OpenAPI)
- [ ] Implement WebSocket notifications
- [ ] Add analytics dashboard
- [ ] Set up CI/CD pipeline (GitHub Actions)

---

## Credits & License

**Author:** Stamatios Mavitzis  
**Student ID:** 2018030040  
**Course:** ΠΛΗ513 – Services in Cloud and Fog Computing  
**Institution:** Technical University of Crete

This project is open-source and distributed for educational and academic use only.

---

## Database Recreation Script

This project provides an automated script to **recreate the PostgreSQL database** (schema + data) from the exported SQL dump (`database.sql`).

### 🔧 Script: `recreate_database.sh`

```bash
#!/bin/bash
# recreate_database.sh
# Full PostgreSQL initialization script (creates DB, schema, and inserts data)
# Works even if the database does not exist yet.

DB_NAME="project_db"
DB_USER="postgres"
DB_PASSWORD="xotour"
DB_HOST="localhost"
DB_PORT="5432"
SQL_FILE="database.sql"

# Check if psql exists
if ! command -v psql &> /dev/null
then
    echo "❌ psql command not found. Please install PostgreSQL client tools first."
    exit 1
fi

# Export password for non-interactive authentication
export PGPASSWORD=$DB_PASSWORD

echo "🚀 Starting PostgreSQL database setup..."
echo "---------------------------------------"

# Create database if it doesn't exist
DB_EXISTS=$(psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")
if [ "$DB_EXISTS" != "1" ]; then
    echo "🆕 Creating database '$DB_NAME'..."
    psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "CREATE DATABASE $DB_NAME;"
else
    echo "⚠️ Database '$DB_NAME' already exists. Dropping and recreating..."
    psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "DROP DATABASE $DB_NAME;"
    psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "CREATE DATABASE $DB_NAME;"
fi

# Load schema and data from SQL dump
echo "📥 Importing schema and data from $SQL_FILE ..."
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Database '$DB_NAME' initialized successfully!"
else
    echo "❌ An error occurred during initialization. Check your SQL file."
    exit 1
fi
```

### 🧠 Usage

1. Place this script in your project root **next to** `database.sql`.
2. Make it executable:
   ```bash
   chmod +x recreate_database.sh
   ```
3. Run it:
   ```bash
   ./recreate_database.sh
   ```

### 🧩 What It Does
- Checks for PostgreSQL client (`psql`)
- Drops any existing `project_db`
- Creates a new database from scratch
- Imports **schema and data** from `database.sql`
- Uses password via `PGPASSWORD` (non-interactive mode)

### 💡 Optional
If you want to initialize with a **custom PostgreSQL user** instead of `postgres`, edit these variables at the top of the script:

```bash
DB_USER="your_username"
DB_PASSWORD="your_password"
```
