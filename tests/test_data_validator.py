
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_validator import validate_book


def test_valid_book():

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["errors"] == []
    assert result["cleaned_data"]["title"] == "The Hobbit"


def test_missing_book_id():

    book = {
        "title": "The Hobbit",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937
    }

    result = validate_book(book)

    assert result["valid"] is False
    assert "Missing or invalid book ID" in result["errors"]
    assert result["cleaned_data"]["key"] is None


def test_empty_title():

    book = {
        "key": "/works/OL12345W",
        "title": "",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["cleaned_data"]["title"] is None
    assert "Missing or invalid book title" in result["warnings"]


def test_clean_author_information():

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "author_name": [
            "J. R. R. Tolkien",
            "",
            "   ",
            None,
            "John Smith"
        ],
        "first_publish_year": 1937
    }

    result = validate_book(book)

    assert result["cleaned_data"]["authors"] == [
        "J. R. R. Tolkien",
        "John Smith"
    ]


def test_missing_publication_year():

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "author_name": ["J. R. R. Tolkien"]
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["cleaned_data"]["first_publish_year"] is None
    assert "Missing or invalid publication year" in result["warnings"]


def test_invalid_publication_year():

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": "nineteen thirty-seven"
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["cleaned_data"]["first_publish_year"] is None
    assert "Missing or invalid publication year" in result["warnings"]


def test_missing_edition_count():

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["cleaned_data"]["edition_count"] is None
    assert "Missing or invalid edition count" in result["warnings"]


def test_invalid_edition_count():

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": -5
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["cleaned_data"]["edition_count"] is None
    assert "Missing or invalid edition count" in result["warnings"]


def test_clean_title_formatting():

    book = {
        "key": "/works/OL12345W",
        "title": "   The    Hobbit   ",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    result = validate_book(book)

    assert result["cleaned_data"]["title"] == "The Hobbit"


def test_invalid_book_id_with_otherwise_valid_data():

    book = {
        "title": "   The    Hobbit   ",
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    result = validate_book(book)

    assert result["valid"] is False
    assert result["cleaned_data"]["key"] is None
    assert result["cleaned_data"]["title"] == "The Hobbit"


def test_invalid_title_data_type():

    book = {
        "key": "/works/OL12345W",
        "title": 12345,
        "author_name": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    result = validate_book(book)

    assert result["valid"] is True
    assert result["cleaned_data"]["title"] is None
    assert "Missing or invalid book title" in result["warnings"]
