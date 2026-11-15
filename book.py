"""Book model for the Personal Library & Reading Tracker."""

# Fixed reading statuses, defined once and imported where needed.
STATUSES = ("Unread", "Reading", "Completed")


def check_book_values(rating, total_pages, pages_completed):
    """Raise ValueError if rating or page values are not valid."""
    if not 0 <= rating <= 5:
        raise ValueError("Rating must be between 0 and 5.")
    if total_pages < 1:
        raise ValueError("Total pages must be at least 1.")
    if pages_completed < 0:
        raise ValueError("Pages completed cannot be negative.")
    if pages_completed > total_pages:
        raise ValueError(
            f"Pages completed ({pages_completed}) cannot exceed "
            f"total pages ({total_pages})."
        )


class Book:
    """A single book with details and reading progress."""

    def __init__(self, book_id, title, author, genre, year, rating,
                 total_pages, pages_completed=0):
        check_book_values(rating, total_pages, pages_completed)
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.rating = rating
        self.total_pages = total_pages
        self.pages_completed = pages_completed
        self.status = STATUSES[0]
        self._refresh_status()

    def _refresh_status(self):
        """Set the status automatically from the page progress."""
        if self.pages_completed == 0:
            self.status = STATUSES[0]      # Unread
        elif self.pages_completed == self.total_pages:
            self.status = STATUSES[2]      # Completed
        else:
            self.status = STATUSES[1]      # Reading

    def completion_percentage(self):
        """Return reading completion as a percentage (0-100)."""
        return self.pages_completed / self.total_pages * 100

    def update_progress(self, pages_completed):
        """Set pages completed and update the status automatically."""
        check_book_values(self.rating, self.total_pages, pages_completed)
        self.pages_completed = pages_completed
        self._refresh_status()

    def update_details(self, title=None, author=None, genre=None, year=None,
                       rating=None, total_pages=None):
        """Update any provided details. Arguments left as None are kept."""
        new_rating = self.rating if rating is None else rating
        new_total = self.total_pages if total_pages is None else total_pages
        # Validate first so nothing is changed if a value is invalid.
        check_book_values(new_rating, new_total, self.pages_completed)

        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if genre is not None:
            self.genre = genre
        if year is not None:
            self.year = year
        self.rating = new_rating
        self.total_pages = new_total
        self._refresh_status()

    def to_dict(self):
        """Convert the book into a dictionary for JSON/CSV storage."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating,
            "total_pages": self.total_pages,
            "pages_completed": self.pages_completed,
            "status": self.status,
        }
