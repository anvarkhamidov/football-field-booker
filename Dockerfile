# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
# RUN python manage.py migrate

# Start the application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
