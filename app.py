from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'db/books.db'

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT b.book_id,
                   b.title,
                   b.publication_year,
                   b.book_url,
                   COALESCE(GROUP_CONCAT(a.name, ', '), '') AS author_name
            FROM Books b
            LEFT JOIN book_author ba ON ba.book_id = b.book_id
            LEFT JOIN Authors a ON a.author_id = ba.author_id
            GROUP BY b.book_id, b.title, b.publication_year, b.book_url
            ORDER BY b.book_id
            """
        )
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2],
                'book_url': book[3],
                'author_name': book[4]
                # Add other attributes here as needed
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)})


# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')
        author_name = (data.get('author_name') or '').strip() if isinstance(data, dict) else ''
        book_url = data.get('book_url')

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Insert the book into the database
        cursor.execute("INSERT INTO Books (title, publication_year, book_url) VALUES (?, ?, ?)", (title, publication_year, book_url))
        book_id = cursor.lastrowid

        # If an author name is provided, find or create the author and link it
        if author_name:
            cursor.execute("SELECT author_id FROM Authors WHERE LOWER(name) = LOWER(?) LIMIT 1", (author_name,))
            row = cursor.fetchone()
            if row:
                author_id = row[0]
            else:
                cursor.execute("INSERT INTO Authors (name) VALUES (?)", (author_name,))
                author_id = cursor.lastrowid

            # Link book and author (ignore if already linked)
            cursor.execute(
                "INSERT OR IGNORE INTO book_author (book_id, author_id) VALUES (?, ?)",
                (book_id, author_id)
            )

        conn.commit()
        conn.close()

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# API to search for books by title or author
@app.route('/api/search', methods=['GET'])
def search_books():
    try:
        query = request.args.get('q', '')

        if not query:
            return jsonify({'error': 'No search query provided'}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Use LIKE for case-insensitive partial matching on title or author
        cursor.execute(
            """
            SELECT b.title,
                   b.publication_year,
                   b.book_url,
                   COALESCE(GROUP_CONCAT(a.name, ', '), '') AS author_name
            FROM Books b
            LEFT JOIN book_author ba ON ba.book_id = b.book_id
            LEFT JOIN Authors a ON a.author_id = ba.author_id
            WHERE LOWER(b.title) LIKE ?
               OR LOWER(a.name) LIKE ?
            GROUP BY b.book_id, b.title, b.publication_year, b.book_url
            ORDER BY b.book_id
            """,
            ('%' + query.lower() + '%', '%' + query.lower() + '%')
        )
        results = cursor.fetchall()
        conn.close()

        # Format results as JSON
        books = [{'title': row[0], 'publication_year': row[1], 'author_name': row[3], 'book_url': row[2]} for row in results]

        return jsonify({'results': books})
    except Exception as e:
        return jsonify({'error': str(e)})


# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
