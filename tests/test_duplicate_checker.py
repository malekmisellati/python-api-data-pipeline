
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from duplicate_checker import remove_duplicates


def test_no_duplicates():

    books = [
        {"key": "/works/OL12345W", "title": "The Hobbit"},
        {"key": "/works/OL67890W", "title": "The Lord of the Rings"},
        {"key": "/works/OL11111W", "title": "Dune"}
    ]

    result = remove_duplicates(books)

    assert len(result["unique_books"]) == 3
    assert len(result["duplicates"]) == 0


def test_duplicate_books():

    books = [
        {"key": "/works/OL12345W", "title": "The Hobbit"},
        {"key": "/works/OL67890W", "title": "Dune"},
        {"key": "/works/OL12345W", "title": "The Hobbit"}
    ]

    result = remove_duplicates(books)

    assert len(result["unique_books"]) == 2
    assert len(result["duplicates"]) == 1


def test_multiple_duplicates():

    books = [
        {"key": "/works/OL12345W", "title": "The Hobbit"},
        {"key": "/works/OL12345W", "title": "The Hobbit"},
        {"key": "/works/OL67890W", "title": "Dune"},
        {"key": "/works/OL67890W", "title": "Dune"}
    ]

    result = remove_duplicates(books)

    assert len(result["unique_books"]) == 2
    assert len(result["duplicates"]) == 2


def test_empty_book_list():

    books = []

    result = remove_duplicates(books)

    assert result["unique_books"] == []
    assert result["duplicates"] == []
def test_missing_book_id():

    books = [
        {"key": "/works/OL12345W", "title": "The Hobbit"},
        {"title": "Unknown Book"}
    ]

    result = remove_duplicates(books)

    assert len(result["unique_books"]) == 1
    assert len(result["duplicates"]) == 0
    assert len(result["invalid_books"]) == 1


def test_empty_book_id():

    books = [
        {"key": "", "title": "Unknown Book"}
    ]

    result = remove_duplicates(books)

    assert len(result["unique_books"]) == 0
    assert len(result["duplicates"]) == 0
    assert len(result["invalid_books"]) == 1


def test_whitespace_book_id():

    books = [
        {"key": "   ", "title": "Unknown Book"}
    ]

    result = remove_duplicates(books)

    assert len(result["unique_books"]) == 0
    assert len(result["duplicates"]) == 0
    assert len(result["invalid_books"]) == 1