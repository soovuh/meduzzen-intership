# Meduzzen Internship Project

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/soovuh/meduzzen-internship.git
   cd meduzzen-internship
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. To start the FastAPI application, use the following command:

    ```bash
    python -m app.main
    ```

> **_NOTE:_**  Don't forget to create an .env file and add  the HOST and PORT variables to  it. For local startup you can set HOST='127.0.0.1', PORT='8000'.

## Runing the Application via Docker
1. To start the FastAPI application via Dockerfile, use the following commands:

    ```bash
    docker build -t myapp .
    docker run -d -p 8080:8080 --name myapp-container fastapi-app
    ```

2. To start the FastAPI application via docker-compose, use the following commands:

    ```bash
    docker-compose build
    docker-compose up -d
    ```
> **_NOTE:_**  The -d option will run the container in the background, this option can be removed if desired

### To access the application from a local machine, use http://localhost:8080/

## Migrations with Alembic
1. To generate migrations with alembic run the following command:

    ```bash
    docker-compose run server /bin/sh -c "alembic revision --autogenerate -m "<migration_name>""
    ```
2. To apply migrations for a database in the docker, run the following command:

    ```bash
    docker-compose run server /bin/sh -c "alembic upgrade head"
    ```

## Running Tests via Docker
1. Firstly, need to build docker test containers:

    ```bash
    docker-compose -f docker-compose-test.yaml -p run-tests build
    ```
2. To apply migrations for a database in the docker for tests, run the following command:

    ```bash
    docker-compose -f docker-compose-test.yaml -p run-tests run server /bin/sh -c "alembic upgrade head"
    ```
3. To run tests for the FastAPI application, use the following commands:

    ```bash
    docker-compose -f docker-compose-test.yaml -p run-tests up --build
    ```
This command executes all test modules (test_*.py) within the tests directory using pytest via Docker. The tests are configured to use fixtures defined in conftest.py for setting up the test environment.
