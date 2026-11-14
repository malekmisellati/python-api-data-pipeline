import sys
from pathlib import Path

# Add the src directory to Python's module search path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api_client import search_books


def main():

    books = search_books("The Lord of the Rings", limit=5)

    print(f"\nNumber of books retrieved: {len(books)}")

    for book in books:
        print("\n--------------------")
        print(f"Title: {book.get('title')}")
        print(f"Authors: {book.get('author_name')}")
        print(f"Publication year: {book.get('first_publish_year')}")
        print(f"Book ID: {book.get('key')}")


if __name__ == "__main__":
    main()
