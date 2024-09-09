# Use Python slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install SQLite client and dependencies
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev gcc

# Install Python packages
RUN pip install --no-cache-dir pysqlite3 pyyaml requests

# Copy the Python script into the container
COPY exporter.py .

# Run the Python script
CMD ["python", "-u", "./exporter.py"]
