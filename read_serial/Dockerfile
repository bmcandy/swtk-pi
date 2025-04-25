# Use the official Python 3.13 image as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir mysql-connector-python

# Install pyserial for serial communication
RUN pip install --no-cache-dir pyserial

# Set the command to run the Python script
CMD ["python", "read_serial3.py"]