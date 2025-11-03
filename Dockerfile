FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y netcat-traditional && \
    pip install --no-cache-dir flask psycopg2-binary && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]