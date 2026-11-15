"""Main entry point for the Personal Library & Reading Tracker."""

import reports
import storage
import validators
from book import Book, STATUSES
from library import Library

MENU = """
========================================
       PERSONAL LIBRARY MANAGER
========================================

1. Add a New Book
2. View My Library
3. Search for a Book
4. Update Book Details
5. Delete a Book
6. Update Reading Progress
7. Filter Books
8. Reading Statistics
9. Export Library Data
10. Generate Reading Report
0. Exit
"""


def show_status(success, message):
    """Print a clear success or error message."""
    tag = "[SUCCESS]" if success else "[ERROR]"
    print(f"{tag} {message}")


def ask_for_book(library, prompt="Enter Book ID: "):
    """Ask for a book ID and return the matching Book, or None if missing."""
    book_id = validators.get_int(prompt, minimum=1)
    book = library.find_by_id(book_id)
    if book is None:
        show_status(False, f"No book found with ID {book_id}.")
    return book


def add_book_flow(library):
    """Collect details and add a new book."""
    print("\n--- Add a New Book ---")
    suggested_id = library.next_id()
    book_id = validators.get_int(
        f"Book ID (press Enter for {suggested_id}): ",
        minimum=1,
        allow_blank=True,
    )
    if book_id is None:
        book_id = suggested_id
    if library.id_exists(book_id):
        show_status(False, f"A book with ID {book_id} already exists.")
        return

    title = validators.get_title("Title: ")
    author = validators.get_author("Author: ")
    genre = validators.get_genre("Genre: ")
    year = validators.get_year("Publication year: ")
    rating = validators.get_rating("Rating (0-5, use 0 if not rated): ")
    total_pages = validators.get_page_count("Total pages: ")
    pages_completed = validators.get_progress("Pages completed: ", total_pages)

    book = Book(book_id, title, author, genre, year, rating,
                total_pages, pages_completed)
    success, message = library.add_book(book)
    show_status(success, message)


def view_library_flow(library):
    """Display every book in the library."""
    print("\n--- My Library ---")
    library.display_books()
    print(f"\nTotal books: {len(library.books)}")


def search_flow(library):
    """Search by ID, title or author."""
    print("\n--- Search for a Book ---")
    print("1. By ID")
    print("2. By title")
    print("3. By author")
    choice = validators.get_int("Choose a search type: ", 1, 3)

    if choice == 1:
        book = ask_for_book(library, "Enter Book ID to search: ")
        if book is not None:
            library.display_books([book])
        return

    keyword = validators.read_input("Enter search text: ")
    if choice == 2:
        results = library.search_books("title", keyword)
    else:
        results = library.search_books("author", keyword)

    if len(results) == 0:
        show_status(False, f"No books matched '{keyword}'.")
    else:
        library.display_books(results)
        print(f"\n{len(results)} book(s) found.")


def update_details_flow(library):
    """Update one or more details of an existing book."""
    print("\n--- Update Book Details ---")
    book = ask_for_book(library)
    if book is None:
        return

    library.display_books([book])
    print("\nPress Enter to keep the current value.")
    title = validators.get_title(f"Title [{book.title}]: ", allow_blank=True)
    author = validators.get_author(f"Author [{book.author}]: ", allow_blank=True)
    genre = validators.get_genre(f"Genre [{book.genre}]: ", allow_blank=True)
    year = validators.get_year(f"Year [{book.year}]: ", allow_blank=True)
    rating = validators.get_rating(f"Rating [{book.rating}]: ", allow_blank=True)
    total_pages = validators.get_page_count(
        f"Total pages [{book.total_pages}]: ", allow_blank=True
    )

    has_changes = False
    for value in [title, author, genre, year, rating, total_pages]:
        if value is not None:
            has_changes = True

    if not has_changes:
        print("No changes were made.")
        return

    success, message = library.update_book(
        book.book_id, title, author, genre, year, rating, total_pages
    )
    show_status(success, message)


def delete_flow(library):
    """Delete a book after confirmation."""
    print("\n--- Delete a Book ---")
    book = ask_for_book(library)
    if book is None:
        return

    library.display_books([book])
    if validators.get_yes_no("Delete this book? (y/n): "):
        success, message = library.delete_book(book.book_id)
        show_status(success, message)
    else:
        print("Deletion cancelled.")


def update_progress_flow(library):
    """Update pages completed for a book."""
    print("\n--- Update Reading Progress ---")
    book = ask_for_book(library)
    if book is None:
        return

    library.display_books([book])
    pages = validators.get_progress(
        f"Pages completed (0-{book.total_pages}): ", book.total_pages
    )
    success, message = library.update_progress(book.book_id, pages)
    show_status(success, message)


def filter_flow(library):
    """Filter books by genre or reading status."""
    print("\n--- Filter Books ---")
    print("1. By genre")
    print("2. By reading status")
    choice = validators.get_int("Choose a filter: ", 1, 2)

    if choice == 1:
        genres = library.get_genres()
        if len(genres) == 0:
            show_status(False, "Your library is empty.")
            return
        print("Available genres: " + ", ".join(genres))
        genre = validators.read_input("Genre to show: ")
        results = library.filter_by_genre(genre)
        label = f"genre '{genre}'"
    else:
        for number, status in enumerate(STATUSES, start=1):
            print(f"{number}. {status}")
        status_choice = validators.get_int("Choose a status: ", 1, len(STATUSES))
        status = STATUSES[status_choice - 1]
        results = library.filter_by_status(status)
        label = f"status '{status}'"

    if len(results) == 0:
        show_status(False, f"No books found with {label}.")
    else:
        library.display_books(results)
        print(f"\n{len(results)} book(s) found with {label}.")


def statistics_flow(library):
    """Show reading statistics."""
    print()
    stats = library.get_statistics()
    reports.display_statistics(stats)


def export_flow(library):
    """Export library records to CSV."""
    success, message = reports.export_to_csv(library.books)
    show_status(success, message)


def report_flow(library):
    """Generate the TXT reading report."""
    stats = library.get_statistics()
    success, message = reports.generate_report(library.books, stats)
    show_status(success, message)


def run_menu(library):
    """Show the menu repeatedly until the user chooses to exit."""
    actions = {
        "1": add_book_flow,
        "2": view_library_flow,
        "3": search_flow,
        "4": update_details_flow,
        "5": delete_flow,
        "6": update_progress_flow,
        "7": filter_flow,
        "8": statistics_flow,
        "9": export_flow,
        "10": report_flow,
    }

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("\nThank you for using Personal Library Manager. Goodbye!")
            break
        if choice == "":
            show_status(False, "Empty input. Please enter a number from the menu.")
            continue

        action = actions.get(choice)
        if action is None:
            show_status(False, f"Invalid choice '{choice}'. Choose 0-10.")
            continue

        action(library)
        input("\nPress Enter to return to the menu...")


def main():
    """Load saved data and start the application."""
    storage.initialize_storage()
    books, warnings = storage.load_books()
    for warning in warnings:
        print(f"[WARNING] {warning}")

    library = Library(books)
    try:
        run_menu(library)
    except (KeyboardInterrupt, EOFError):
        print("\n\nInput interrupted. Your saved data is safe. Goodbye!")


if __name__ == "__main__":
    main()
