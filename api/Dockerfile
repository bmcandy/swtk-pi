FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask mysqlclient python-dotenv

# Copy the application code
COPY ./api3.py /app
COPY ./templates /app/templates

# Command to run the application
CMD ["python3", "api3.py"]
