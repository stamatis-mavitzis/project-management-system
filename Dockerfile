FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install required system tools and Python dependencies
RUN apt-get update && apt-get install -y netcat-traditional && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
