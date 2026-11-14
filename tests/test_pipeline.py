import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pipeline import process_books, run_pipeline

def test_pipeline_with_mixed_data():

    books = [
        {
            "key": "/works/OL12345W",
            "title": "The Hobbit",
            "author_name": ["J. R. R. Tolkien"],
            "first_publish_year": 1937,
            "edition_count": 150
        },
        {
            "key": "/works/OL67890W",
            "title": "Dune",
            "author_name": ["Frank Herbert"],
            "first_publish_year": 1965,
            "edition_count": 100
        },
        {
            "key": "/works/OL12345W",
            "title": "The Hobbit",
            "author_name": ["J. R. R. Tolkien"],
            "first_publish_year": 1937,
            "edition_count": 150
        },
        {
            "title": "Unknown Book",
            "author_name": ["Unknown Author"],
            "first_publish_year": 2020,
            "edition_count": 1
        },
        {
            "key": "/works/OL99999W",
            "title": "Invalid Year",
            "author_name": ["Test Author"],
            "first_publish_year": "unknown",
            "edition_count": 5
        }
    ]
    results = process_books(books)

    assert len(books) == 5
    assert len(results["validated_books"]) == 4
    assert len(results["invalid_books"]) == 1

    assert len(results["unique_books"]) == 3
    assert len(results["duplicates"]) == 1
    assert len(results["invalid_ids"]) == 0

    assert results["validated_books"][3]["first_publish_year"] is None

def test_pipeline_with_empty_data():

    books = []

    results = process_books(books)

    assert len(books) == 0
    assert len(results["validated_books"]) == 0
    assert len(results["invalid_books"]) == 0
    assert len(results["unique_books"]) == 0
    assert len(results["duplicates"]) == 0
    assert len(results["invalid_ids"]) == 0

def test_run_pipeline_with_mocked_api(monkeypatch, capsys):

    # Simulate the API returning one book
    fake_books = [
        {
            "key": "/works/OL12345W",
            "title": "The Hobbit",
            "author_name": ["J. R. R. Tolkien"],
            "first_publish_year": 1937,
            "edition_count": 150
        }
    ]

    # Replace the real API function with our simulated function
    def mock_search_books(query, limit):
        return fake_books

    monkeypatch.setattr("pipeline.search_books", mock_search_books)

    # Run the pipeline
    run_pipeline("The Hobbit", limit=1)

    # Capture what the pipeline printed
    captured = capsys.readouterr()

    # Verify the output
    assert "Retrieved 1 books from the API." in captured.out
    assert "Books validated: 1" in captured.out
    assert "Unique books: 1" in captured.out

def test_run_pipeline_with_api_error(monkeypatch, capsys):

    # Simulate an API failure
    def mock_search_books(query, limit):
        raise requests.exceptions.HTTPError("500 Server Error")

    # Replace the real API function
    monkeypatch.setattr("pipeline.search_books", mock_search_books)

    # Run the pipeline
    run_pipeline("The Hobbit", limit=1)

    # Capture printed output
    captured = capsys.readouterr()

    # Verify the error message
    assert "API request failed" in captured.out

def test_run_pipeline_with_empty_api_response(monkeypatch, capsys):

    # Simulate a successful API request with no results
    def mock_search_books(query, limit):
        return []

    # Replace the real API function
    monkeypatch.setattr("pipeline.search_books", mock_search_books)

    # Run the pipeline
    run_pipeline("Unknown Book", limit=1)

    # Capture printed output
    captured = capsys.readouterr()

    # Verify the output
    assert "Retrieved 0 books from the API." in captured.out
    assert "Books validated: 0" in captured.out
    assert "Unique books: 0" in captured.out

def test_run_pipeline_with_duplicate_books(monkeypatch, capsys):

    # Simulate API data containing two unique books and one duplicate
    fake_books = [
        {
            "key": "/works/OL12345W",
            "title": "The Hobbit",
            "author_name": ["J. R. R. Tolkien"],
            "first_publish_year": 1937,
            "edition_count": 150
        },
        {
            "key": "/works/OL67890W",
            "title": "Dune",
            "author_name": ["Frank Herbert"],
            "first_publish_year": 1965,
            "edition_count": 100
        },
        {
            "key": "/works/OL12345W",
            "title": "The Hobbit",
            "author_name": ["J. R. R. Tolkien"],
            "first_publish_year": 1937,
            "edition_count": 150
        }
    ]

    # Simulate the API response
    def mock_search_books(query, limit):
        return fake_books

    monkeypatch.setattr("pipeline.search_books", mock_search_books)

    # Run the pipeline
    run_pipeline("Books", limit=3)

    # Capture printed output
    captured = capsys.readouterr()

    # Verify the pipeline results
    assert "Retrieved 3 books from the API." in captured.out
    assert "Books validated: 3" in captured.out
    assert "Books rejected: 0" in captured.out
    assert "Duplicate books: 1" in captured.out
    assert "Unique books: 2" in captured.out