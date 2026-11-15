"""Library class: manages the collection of Book objects."""

import reports
import storage

ROW_FORMAT = "{:<4}{:<20}{:<15}{:<11}{:<6}{:<7}{:<9}{}"


def shorten(text, width):
    """Cut long text so table columns stay aligned."""
    if len(text) > width:
        return text[:width - 3] + "..."
    return text


class Library:
    """A collection of books with search, filter and update operations."""

    def __init__(self, books=None):
        self.books = books if books is not None else []

    # ---------- helpers ----------
    def _save_result(self, success_message):
        """Save to disk and return (success, message)."""
        if storage.save_books(self.books):
            return True, success_message
        return False, "The change was made in memory but could not be saved to disk."

    def find_by_id(self, book_id):
        """Return the Book with this ID, or None."""
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def id_exists(self, book_id):
        """Return True if the ID is already used."""
        return self.find_by_id(book_id) is not None

    def next_id(self):
        """Suggest the next free book ID."""
        highest = 0
        for book in self.books:
            if book.book_id > highest:
                highest = book.book_id
        return highest + 1

    # ---------- operations ----------
    def add_book(self, book):
        """Add a book unless its ID already exists."""
        if self.id_exists(book.book_id):
            return False, f"A book with ID {book.book_id} already exists."
        self.books.append(book)
        return self._save_result(f"Book '{book.title}' added successfully.")

    def display_books(self, books=None):
        """Print books in a table. Shows the whole library by default."""
        if books is None:
            books = self.books
        if len(books) == 0:
            print("No books to display.")
            return

        print(ROW_FORMAT.format("ID", "Title", "Author", "Genre", "Year",
                                "Rating", "Progress", "Status"))
        print("-" * 80)
        for book in books:
            print(ROW_FORMAT.format(
                book.book_id,
                shorten(book.title, 18),
                shorten(book.author, 13),
                shorten(book.genre, 9),
                book.year,
                f"{book.rating:.1f}",
                f"{book.completion_percentage():.1f}%",
                book.status,
            ))

    def search_books(self, field, keyword):
        """Case-insensitive search by 'title' or 'author'."""
        keyword = keyword.lower()
        results = []
        for book in self.books:
            if field == "title":
                text = book.title
            else:
                text = book.author
            if keyword in text.lower():
                results.append(book)
        return results

    def update_book(self, book_id, title=None, author=None, genre=None,
                    year=None, rating=None, total_pages=None):
        """Update details of an existing book."""
        book = self.find_by_id(book_id)
        if book is None:
            return False, f"No book found with ID {book_id}."
        try:
            book.update_details(title, author, genre, year, rating, total_pages)
        except ValueError as error:
            return False, str(error)
        return self._save_result(f"Book {book_id} updated successfully.")

    def delete_book(self, book_id):
        """Delete a book by ID."""
        book = self.find_by_id(book_id)
        if book is None:
            return False, f"No book found with ID {book_id}."
        self.books.remove(book)
        return self._save_result(f"Book '{book.title}' deleted.")

    def update_progress(self, book_id, pages_completed):
        """Update pages completed; status updates automatically."""
        book = self.find_by_id(book_id)
        if book is None:
            return False, f"No book found with ID {book_id}."
        try:
            book.update_progress(pages_completed)
        except ValueError as error:
            return False, str(error)
        return self._save_result(
            f"Progress updated: {book.pages_completed}/{book.total_pages} pages "
            f"({book.completion_percentage():.1f}%) - status: {book.status}."
        )

    def filter_by_genre(self, genre):
        """Return books whose genre matches (case-insensitive)."""
        results = []
        for book in self.books:
            if book.genre.lower() == genre.strip().lower():
                results.append(book)
        return results

    def filter_by_status(self, status):
        """Return books with the given reading status."""
        results = []
        for book in self.books:
            if book.status == status:
                results.append(book)
        return results

    def get_genres(self):
        """Return a sorted list of unique genres (uses a set)."""
        genres = set()
        for book in self.books:
            genres.add(book.genre)
        return sorted(genres)

    def get_statistics(self):
        """Return collection statistics as a dictionary."""
        return reports.calculate_statistics(self.books)
