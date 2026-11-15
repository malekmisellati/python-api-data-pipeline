import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import database

def test_create_table(tmp_path, monkeypatch):

    # Use a temporary database for this test
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_database))

    # Create the database and books table
    database.create_table()

    # Connect to the test database
    connection = database.create_connection()

    cursor = connection.cursor()

    # Check whether the books table exists
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'books'
    """)

    result = cursor.fetchone()

    connection.close()

    assert result is not None
    assert result[0] == "books"

def test_insert_and_retrieve_book(tmp_path, monkeypatch):

    # Use a temporary database
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_database))

    # Create the table
    database.create_table()

    # Create a sample book
    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "authors": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    # Insert the book
    database.insert_book(book)

    # Retrieve stored books
    books = database.get_all_books()

    # Verify the stored record
    assert len(books) == 1
    assert books[0][0] == "/works/OL12345W"
    assert books[0][1] == "The Hobbit"

def test_prevent_duplicate_books(tmp_path, monkeypatch):

    # Use a temporary database
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_database))

    # Create the table
    database.create_table()

    # Sample book
    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "authors": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    # Insert the same book twice
    database.insert_book(book)
    database.insert_book(book)

    # Retrieve stored books
    books = database.get_all_books()

    # Verify duplicate prevention
    assert len(books) == 1

def test_insert_multiple_books(tmp_path, monkeypatch):

    # Use a temporary database
    test_database = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_database))

    # Create the table
    database.create_table()

    # Create sample books
    books_to_insert = [
        {
            "key": "/works/OL12345W",
            "title": "The Hobbit",
            "authors": ["J. R. R. Tolkien"],
            "first_publish_year": 1937,
            "edition_count": 150
        },
        {
            "key": "/works/OL67890W",
            "title": "Dune",
            "authors": ["Frank Herbert"],
            "first_publish_year": 1965,
            "edition_count": 100
        }
    ]

    # Insert both books
    for book in books_to_insert:
        database.insert_book(book)

    # Retrieve stored books
    stored_books = database.get_all_books()

    # Verify both books were stored
    assert len(stored_books) == 2

def test_store_authors_as_json(tmp_path, monkeypatch):

    test_database = tmp_path / "test.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_database))

    database.create_table()

    book = {
        "key": "/works/OL12345W",
        "title": "The Hobbit",
        "authors": ["J. R. R. Tolkien"],
        "first_publish_year": 1937,
        "edition_count": 150
    }

    database.insert_book(book)

    stored_books = database.get_all_books()

    stored_authors = stored_books[0][2]

    assert stored_authors == '["J. R. R. Tolkien"]'