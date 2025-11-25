import pytest
from app import app
from uuid import uuid4

def test_add_book_increases_count():
    client = app.test_client()

    # Get number of books before adding
    response = client.get("/api/books")
    assert response.status_code == 200
    before_count = len(response.get_json()["books"])

    # Add a new book
    response = client.post("/api/add_book", json={
        "title": "Clean Architecture",
        "publication_year": "2025"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Book added successfully"

    # Get number of books after adding
    response = client.get("/api/books")
    assert response.status_code == 200
    after_count = len(response.get_json()["books"])

    # Assert count increased by 1
    assert after_count == before_count + 1


def test_add_book_stores_title_author_and_image_url():
    client = app.test_client()

    unique = str(uuid4())[:8]
    title = f"Test Book {unique}"
    author = f"Author {unique}"
    image_url = f"https://example.com/{unique}.jpg"

    # Add a new book with author and image URL
    response = client.post(
        "/api/add_book",
        json={
            "title": title,
            "publication_year": "2024",
            "author_name": author,
            "book_url": image_url,
        },
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Book added successfully"

    # Fetch all books and verify fields are stored
    response = client.get("/api/books")
    assert response.status_code == 200
    books = response.get_json()["books"]
    # Find the book by title
    stored = next((b for b in books if b["title"] == title), None)
    assert stored is not None, "Added book not found in /api/books"
    assert stored["book_url"] == image_url
    assert author.lower() in (stored.get("author_name") or "").lower()


def test_search_by_title_returns_correct_results():
    client = app.test_client()

    unique = str(uuid4())[:8]
    title = f"Search Title {unique}"
    author = f"Some Author {unique}"
    image_url = f"https://example.com/{unique}.png"

    # Ensure a known book exists
    response = client.post(
        "/api/add_book",
        json={
            "title": title,
            "publication_year": "2023",
            "author_name": author,
            "book_url": image_url,
        },
    )
    assert response.status_code == 200

    # Search by full title
    response = client.get(f"/api/search?q={title}")
    assert response.status_code == 200
    results = response.get_json()["results"]
    match = next((r for r in results if r["title"] == title), None)
    assert match is not None
    assert author.lower() in (match.get("author_name") or "").lower()
    assert match.get("book_url") == image_url


def test_search_nonexistent_returns_empty_results():
    client = app.test_client()

    query = "no-way-this-exists-" + str(uuid4())
    response = client.get(f"/api/search?q={query}")
    assert response.status_code == 200
    data = response.get_json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 0
