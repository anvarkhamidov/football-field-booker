# Football Field Booking System

This is a Django-based API for booking football fields. The project uses PostgreSQL as the database and is containerized
using Docker and Docker Compose.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [License](#license)

## Features

- User authentication using tokens.
- Field management for field owners.
- Booking management for users.
- Availability check for fields during requested times.
- Swagger documentation for easy API exploration.

## Technologies Used

- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose
- Nginx

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/football-field-booking-system.git
   cd football-field-booking-system

2. Create a .env file in the root directory and set up the necessary environment variables:

    ```bash
   POSTGRES_DB=mydatabase
   POSTGRES_USER=myuser
   POSTGRES_PASSWORD=mypassword
   POSTGRES_HOST=db
    ```

### Configuration

The project uses a multi-container Docker setup. Make sure to configure the `docker-compose.yml` file as needed.
The Nginx configuration can be found in the nginx directory.

### Running the Application

1. Build and start the containers:

        docker-compose up -d

2. Wait for the containers to start. You can check the logs with:

        docker-compose logs -f

3. Run database migrations:

        docker-compose exec web python manage.py migrate

4. Create a superuser (optional):

        docker-compose exec web python manage.py createsuperuser

5. Access the application at `http://localhost:8010` and the API documentation at `http://localhost:8010/docs/`.
