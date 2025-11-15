#!/bin/bash
# -----------------------------------------------------------------------------
# PostgreSQL Server and Database Setup Script
# Creates user 'nefos' (password: xotour) and database 'project_db'
# Automatically installs PostgreSQL if not present and imports database.sql
# -----------------------------------------------------------------------------

DB_USER="nefos"
DB_PASS="xotour"
DB_NAME="project_db"
SQL_FILE="database.sql"

echo "Starting PostgreSQL setup..."
echo "---------------------------------------"

# Check if PostgreSQL is installed
if ! command -v psql > /dev/null 2>&1; then
  echo "PostgreSQL not found. Installing..."
  sudo apt update -y
  sudo apt install -y postgresql postgresql-contrib
else
  echo "PostgreSQL is already installed."
fi

# Ensure PostgreSQL service is running
echo "Ensuring PostgreSQL service is running..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Switch to postgres user and execute SQL commands
sudo -u postgres psql <<EOF
-- Drop database if exists
DROP DATABASE IF EXISTS ${DB_NAME};
-- Drop role if exists
DROP ROLE IF EXISTS ${DB_USER};

-- Create user and database
CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASS}';
CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOF

echo "Database '${DB_NAME}' and user '${DB_USER}' created successfully."

# Import schema & data from SQL file
if [ -f "$SQL_FILE" ]; then
  echo "Importing schema and data from ${SQL_FILE} ..."
  sudo -u postgres psql -d "${DB_NAME}" -f "${SQL_FILE}" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Database import completed successfully."
  else
    echo "Error occurred during import. Check SQL file for issues."
  fi
else
  echo "SQL file ${SQL_FILE} not found. Skipping import."
fi

# Test connection with created user
echo "Testing connection..."
PGPASSWORD="${DB_PASS}" psql -U "${DB_USER}" -d "${DB_NAME}" -h localhost -c "\dt" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Connection test successful! Setup completed."
else
  echo "Connection test failed. Check credentials or PostgreSQL status."
fi

echo "---------------------------------------"
echo "Setup finished. Database '${DB_NAME}' ready for use."
