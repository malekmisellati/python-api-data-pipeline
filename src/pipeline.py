import requests
from api_client import search_books
from data_validator import validate_book
from duplicate_checker import remove_duplicates

def process_books(books):

    # Store validation results
    validated_books = []
    invalid_books = []

    # Validate each book
    for book in books:

        result = validate_book(book)

        if result["valid"]:
            validated_books.append(result["cleaned_data"])

        else:
            invalid_books.append(result)

    # Remove duplicate books
    duplicate_results = remove_duplicates(validated_books)

    unique_books = duplicate_results["unique_books"]
    duplicates = duplicate_results["duplicates"]
    invalid_ids = duplicate_results["invalid_books"]

    return {
        "validated_books": validated_books,
        "invalid_books": invalid_books,
        "unique_books": unique_books,
        "duplicates": duplicates,
        "invalid_ids": invalid_ids
    }

def run_pipeline(query, limit=10):

    # Retrieve books from the API
    try:
        books = search_books(query, limit)

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        return

    print(f"Retrieved {len(books)} books from the API.")

    # Process the retrieved books
    results = process_books(books)

    # Print pipeline summary
    print("\n--- Pipeline Summary ---")

    print(f"Books validated: {len(results['validated_books'])}")
    print(f"Books rejected: {len(results['invalid_books'])}")
    print(f"Duplicate books: {len(results['duplicates'])}")
    print(f"Books with invalid IDs: {len(results['invalid_ids'])}")
    print(f"Unique books: {len(results['unique_books'])}")