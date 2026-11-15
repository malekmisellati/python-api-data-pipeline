import sqlite3
import json

DATABASE_PATH = "data/books.db"


def create_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    return connection

def create_table():

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            key TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            first_publish_year INTEGER,
            edition_count INTEGER
        )
    """)

    connection.commit()

    connection.close()
def insert_book(book):

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO books (
            key,
            title,
            authors,
            first_publish_year,
            edition_count
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        book["key"],
        book["title"],
        json.dumps(book["authors"]),
        book["first_publish_year"],
        book["edition_count"]
    ))

    connection.commit()

    connection.close()

def get_all_books():

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()

    return books