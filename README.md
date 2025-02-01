# TrainsService

## Introduction

**TrainsService** is a core microservice of the **Travel-Booking-Framework** that provides a Management system for Trains, like Create - Update - Delete with **Command Pattern**.
This service is developed using **Django**, **PostgreSQL** and **Elasticsearch**. This Project has **Signals** with **Observer Pattern** for Sync PostgreSQL and Elasticsearch.

## Features

- **Trains CUD**: Add, Update and Delete Trains Models with Command Pattern.
- **Trains Simple Queries**: Filter Trains by Simple Queries with Query Object Pattern.
- **Flight Signals**: Sync PostgreSQL with Elasticsearch for TrainsService microservice.

## Prerequisites

- **Python 3.x**
- **Django**
- **Elasticsearch**
- **PostgreSQL**

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Travel-Booking-Framework/TrainsService
   cd TrainsService
   ```

2. **Create and Activate a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup PostgreSQL**: Ensure **PostgreSQL** is installed and running. Update your (`settings.py`) with the correct database credentials.

5. **Setup Elasticsearch**: Ensure that **Elasticsearch** is installed and running on your system. Update the Django settings (`settings.py`) with the correct Elasticsearch configuration.

## Project Structure

- **TrainsService/**: Contains the core settings and configurations for Django.
- **Train/**: Manages Train-related operations and functionalities.
- **Class-Diagram/**: Provides class diagrams for understanding the project architecture.
- **logs/**: Contains logs files.

## Contribution Guidelines

We welcome contributions from the community! To contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Commit** your changes.
4. **Submit a Pull Request**.


## Additional Notes

- **Create a Superuser**: To create an admin account, use the command:
  ```bash
  python manage.py createsuperuser
  ```

- **GraphQL Support**: This project includes GraphQL capabilities, which can be accessed at `/graphql/`.