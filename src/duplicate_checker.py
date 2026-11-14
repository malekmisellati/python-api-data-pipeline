def remove_duplicates(books):

    seen_ids = set()
    unique_books = []
    duplicates = []
    invalid_books = []

    for book in books:

        book_id = book.get("key")

        # Check whether the book has a valid ID
        if not isinstance(book_id, str) or not book_id.strip():
            invalid_books.append(book)
            continue

        # Remove surrounding whitespace from the ID
        book_id = book_id.strip()

        # Check whether the ID has already appeared
        if book_id in seen_ids:
            duplicates.append(book)
            continue

        # Record the new ID and keep the book
        seen_ids.add(book_id)
        unique_books.append(book)

    return {
        "unique_books": unique_books,
        "duplicates": duplicates,
        "invalid_books": invalid_books
    }