#!/bin/bash
# Script to activate venv and run Flask app

# Activate the virtual environment
source venv/bin/activate

# Set Flask app variable (adjust if your file is named differently)
export FLASK_APP=backend_server_app.py

# Optional: enable debug mode
export FLASK_ENV=development

# Run Flask
flask run