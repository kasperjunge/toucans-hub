# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependency files
COPY pyproject.toml poetry.lock* ./

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]