def validate_book(book):

    errors = []
    warnings = []

    # Check whether the book has a valid ID
    book_id = book.get("key")

    if not isinstance(book_id, str) or not book_id.strip():
        errors.append("Missing or invalid book ID")

    # Check the book title
    
    title = book.get("title")

    if not isinstance(title, str):
        warnings.append("Missing or invalid book title")
        title = None

    else:
        title = " ".join(title.split())

    if not title:
        warnings.append("Missing or invalid book title")
        title = None

    # Check author information
    
    authors = book.get("author_name")

    if isinstance(authors, list):

        cleaned_authors = [
            author.strip()
            for author in authors
            if isinstance(author, str) and author.strip()
        ]

    else:
        cleaned_authors = []

    if not cleaned_authors:
        warnings.append("Missing author information")

    # Check publication year
    
    publication_year = book.get("first_publish_year")

    if (
        not isinstance(publication_year, int)
        or isinstance(publication_year, bool)
        or publication_year <= 0
    ):
        warnings.append("Missing or invalid publication year")
        publication_year = None
       
    
    # Check edition count
    
    edition_count = book.get("edition_count")

    if (
        not isinstance(edition_count, int)
        or isinstance(edition_count, bool)
        or edition_count <= 0
    ):
        warnings.append("Missing or invalid edition count")
        edition_count = None
        
    
    # Build a cleaned book record
    
    cleaned_data = {
        "key": book_id.strip() if isinstance(book_id, str) else None,
        "title": title,
        "authors": cleaned_authors,
        "first_publish_year": publication_year,
        "edition_count": edition_count
    }

    # Return validation results and cleaned book data
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "cleaned_data": cleaned_data
    }
