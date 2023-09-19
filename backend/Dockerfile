# Use an official Python runtime as a parent image
FROM python:3.11.5-bookworm

# Set environment variables for Python to not write .pyc files and to disable buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory contents into /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
