const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
	const bookTitle = document.getElementById('bookTitle').value;
	const publicationYear = document.getElementById('publicationYear').value;
	const authorName = document.getElementById('authorName').value;
	const bookURL = document.getElementById('bookURL').value;

	// Create a JSON object with book data
	const bookData = {
		title: bookTitle,
		publication_year: publicationYear,
		author_name: authorName,
		book_url: bookURL,
	};

	// Send the book data to the server via POST request
	fetch('/api/add_book', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(bookData),
	})
		.then((response) => response.json())
		.then((data) => {
			// Display a success message or handle errors if needed
			console.log(data.message);

			// Add the new book data to the books array
			books.push(bookData);
			console.log(books);

			// Refresh the book list
			displayBooks();
		})
		.catch((error) => {
			console.error('Error adding book:', error);
		});
}

// Function to display books in the list
function displayBooks() {
	const bookList = document.getElementById('bookList');
	bookList.innerHTML = ''; // Clear existing book list

	books.forEach((book) => {
		const bookElement = document.createElement('div');
		bookElement.innerHTML = `
    <div class="bg-[#d2b48c] flex flex-col items-center w-full p-6 rounded-lg shadow-md space-y-4">
            <h2>Added Successfully :${book.title}</h2>
            <p>Publication Year: ${book.publication_year}</p>
            <p>Author Name: ${book.author_name || ''}</p>
            <img src="${book.book_url || ''}" alt="Book Image">
            </div>
        `;
		bookList.appendChild(bookElement);
	});
}

// Function to fetch and display all books from the server
function showAllBooks() {
	fetch('/api/books')
		.then((response) => response.json())
		.then((data) => {
			const bookList = document.getElementById('allbooks');
			bookList.innerHTML = ''; // Clear existing book list
			console.log(data);
			data.books.forEach((book) => {
				// Access the 'books' key in the JSON response
				const bookElement = document.createElement('div');
				bookElement.innerHTML = `
        <div class="bg-[#d2b48c] flex flex-col items-center w-full p-6 rounded-lg shadow-md space-y-4 h-full">
                    <h2  >${book.title}</h2>
                    <p>Publication Year: ${book.publication_year}</p>
                    <p>Author Name: ${book.author_name || 'No Author'}</p>
                    <img class="hover:scale-105 transition-all duration-300" src="${
											book.book_url || ''
										}" alt="Book Image">
                    </div>
                `;
				bookList.appendChild(bookElement);
			});
		})
		.catch((error) => {
			console.error('Error fetching all books:', error);
		});
}

// Function to search for books
function searchBooks() {
	const query = document.getElementById('searchBox').value;

	if (!query) {
		alert('Please enter a search term!');
		return;
	}

	fetch(`/api/search?q=${encodeURIComponent(query)}`)
		.then((response) => response.json())
		.then((data) => {
			const searchResults = document.getElementById('searchResults');
			searchResults.innerHTML = ''; // Clear previous results

			if (data.results && data.results.length > 0) {
				data.results.forEach((book) => {
					const bookElement = document.createElement('div');
					bookElement.innerHTML = `
                      <div class="bg-[#d2b48c] flex flex-col items-center w-full p-6 rounded-lg shadow-md space-y-4 h-full">
                        <h2>${book.title}</h2>
                        <p>Publication Year: ${book.publication_year}</p>
                        <p>Author Name: ${book.author_name || 'No Author'}</p>
                        <img class="hover:scale-105 transition-all duration-300" src="${
													book.book_url || ''
												}" alt="Book Image">
                      </div>
                    `;
					searchResults.appendChild(bookElement);
				});
			} else {
				searchResults.innerHTML = `<p>No matching books found.</p>`;
			}
		})
		.catch((error) => {
			console.error('Error searching books:', error);
		});
}

function addReview() {
	const bookId = document.getElementById('bookId').value;
	const userName = document.getElementById('userName').value;
	const rating = document.getElementById('rating').value;
	const comment = document.getElementById('comment').value;

	const reviewData = {
		book_id: bookId,
		user: userName,
		rating: rating,
		comment: comment,
	};

	fetch('/api/add_review', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(reviewData),
	})
		.then((response) => response.json())
		.then((data) => {
			console.log(data.message);
			showAllReviews(); // Refresh reviews after adding
		})
		.catch((error) => {
			console.error('Error adding review:', error);
		});
}

// Function to fetch and display all reviews
function showAllReviews() {
	fetch('/api/reviews')
		.then((response) => response.json())
		.then((data) => {
			const reviewList = document.getElementById('reviewList');
			reviewList.innerHTML = ''; // Clear existing reviews

			data.reviews.forEach((review) => {
				const reviewElement = document.createElement('div');
				reviewElement.classList.add('review');
				reviewElement.innerHTML = `
                    <h3>Book ID: ${review.book_id}</h3>
                    <p>User: ${review.user}</p>
                    <p>Rating: ${review.rating}</p>
                    <p>Comment: ${review.comment}</p>
                `;
				reviewList.appendChild(reviewElement);
			});
		})
		.catch((error) => {
			console.error('Error fetching reviews:', error);
		});
}

// Attach search button click
document.addEventListener('DOMContentLoaded', () => {
	const searchButton = document.getElementById('searchButton');
	if (searchButton) {
		searchButton.addEventListener('click', searchBooks);
	}
});
