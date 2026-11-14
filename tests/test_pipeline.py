import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pipeline import process_books

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