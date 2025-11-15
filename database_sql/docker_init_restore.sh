#!/bin/bash
set -e

echo "Running docker_init_restore.sh — restoring PostgreSQL database..."

# Wait for PostgreSQL to be ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
    echo "Waiting for Postgres to be ready..."
    sleep 1
done

echo "Postgres is ready! Importing SQL dump..."

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/database.sql

echo "Docker database initialization completed successfully!"
