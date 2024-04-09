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
    uvicorn app.main:app --host ${HOST} --port ${PORT} --reload
    ```

> **_NOTE:_**  Don't forget to create an .env file and add  the HOST and PORT variables to  it. For local startup you can set HOST='127.0.0.1', PORT='8000'.

## Running Tests
1. To run tests for the FastAPI application, use the following command:

    ```bash
    python -m pytest tests/
    ```
    
This command executes all test modules (test_*.py) within the tests directory using pytest. The tests are configured to use fixtures defined in conftest.py for setting up the test environment.