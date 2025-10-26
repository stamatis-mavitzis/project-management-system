# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY app/ /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=homepage.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run Flask
CMD ["flask", "run"]
