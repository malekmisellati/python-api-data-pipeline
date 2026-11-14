
import requests

API_URL = "https://openlibrary.org/search.json"


def search_books(query, limit=5):

    params = {
        "q": query,
        "fields": "title,author_name,first_publish_year,key,edition_count",
        "limit": limit
    }

    response = requests.get(API_URL, params=params, timeout=10)

    response.raise_for_status()

    data = response.json()

    books = data.get("docs", [])

    return books
