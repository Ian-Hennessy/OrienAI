# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /OrienAI

# Copy requirements.txt first (to leverage Docker cache)
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application code to the container
COPY . /app/

# Expose the port your app runs on (Flask default is 5000)
EXPOSE 5000

# Set necessary environment variables for Flask
ENV FLASK_APP=OrienAI.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the Flask app
CMD ["flask", "run"]
