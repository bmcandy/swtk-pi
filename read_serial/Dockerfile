# Use the official Python 3.13 image as the base image
FROM python:3.13-slim

# Install mysql connector for Python
RUN pip install --no-cache-dir mysql-connector-python

# Install pyserial for serial communication
RUN pip install --no-cache-dir pyserial

# Install python-dotenv for environment variable management
RUN pip install --no-cache-dir python-dotenv

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Set the command to run the Python script
CMD ["python3", "read_serial3.py"]