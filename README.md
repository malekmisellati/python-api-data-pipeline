# Python API Data Pipeline

## Overview

A Python application that retrieves data from external REST APIs, processes JSON responses, validates records, and stores information in an SQLite database.

## Objectives

- Integrate with external REST APIs.
- Process and validate JSON data.
- Detect duplicate records.
- Store structured data using SQLite.
- Handle API errors and failed requests.
- Implement automated tests.

## Technologies

- Python
- Requests (HTTP API integration)
- REST APIs
- JSON
- SQLite
- Pytest
- Git and GitHub
- Python Logging

## Installation

1. Clone the repository:

   ```bash
   git clone <your-github-repository-url>
   ```

2. Navigate into the project directory:

   ```bash
   cd python-api-data-pipeline
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment (Windows PowerShell):

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install requests pytest
   ```

## Project Structure

- `src/`: Application source code
- `tests/`: Automated tests
- `data/`: Local database and sample data
- `docs/`: Technical documentation

## Usage

Run the application from the project root directory:

bash
python main.py


The application will:

1. Retrieve book data from the Open Library Search API.
2. Validate and clean the retrieved records.
3. Identify duplicate and invalid records.
4. Store unique books in the SQLite database.
5. Log pipeline activity and errors.
6. Display a summary of the pipeline results.

The SQLite database is stored locally at `data/books.db`.

## Running Tests

Run the automated test suite from the project root directory:

bash
python -m pytest -v


The tests cover:

- Data validation and cleaning.
- Duplicate detection.
- Pipeline processing and error handling.
- SQLite database creation and storage.
