from api_client import search_books
from data_validator import validate_book
from duplicate_checker import remove_duplicates

def run_pipeline(query, limit=10):

    # Retrieve books from the API
    books = search_books(query, limit)

    print(f"Retrieved {len(books)} books from the API.")

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

        # Print pipeline summary
    print("\n--- Pipeline Summary ---")

    print(f"Books retrieved: {len(books)}")
    print(f"Books validated: {len(validated_books)}")
    print(f"Books rejected: {len(invalid_books)}")
    print(f"Duplicate books: {len(duplicates)}")
    print(f"Books with invalid IDs: {len(invalid_ids)}")
    print(f"Unique books: {len(unique_books)}")