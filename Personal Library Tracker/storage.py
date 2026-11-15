"""JSON persistence for the library."""

import json
import shutil
from pathlib import Path

from book import Book

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LIBRARY_FILE = DATA_DIR / "library.json"
BACKUP_FILE = DATA_DIR / "library_backup.json"


def initialize_storage():
    """Create the data folder and an empty library file if missing."""
    try:
        DATA_DIR.mkdir(exist_ok=True)
        if not LIBRARY_FILE.exists():
            LIBRARY_FILE.write_text("[]", encoding="utf-8")
    except OSError as error:
        print(f"[WARNING] Could not initialize storage: {error}")


def dict_to_book(record):
    """Convert one dictionary into a Book (raises on bad data)."""
    return Book(
        book_id=int(record["book_id"]),
        title=str(record["title"]),
        author=str(record["author"]),
        genre=str(record["genre"]),
        year=int(record["year"]),
        rating=float(record["rating"]),
        total_pages=int(record["total_pages"]),
        pages_completed=int(record["pages_completed"]),
    )


def backup_library_file():
    """Copy the original file so bad data is never silently lost."""
    try:
        shutil.copy2(LIBRARY_FILE, BACKUP_FILE)
        return f"The original file was copied to {BACKUP_FILE.name}."
    except OSError:
        return "A backup copy of the original file could not be created."


def load_books():
    """Load books from JSON. Returns (books, list_of_warnings)."""
    books = []
    warnings = []

    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
    except OSError as error:
        warnings.append(f"Could not read library file: {error}")
        return books, warnings

    if content == "":
        return books, warnings  # empty file = empty library

    try:
        records = json.loads(content)
    except json.JSONDecodeError:
        warnings.append("library.json is malformed. Starting with an empty "
                        "library. " + backup_library_file())
        return books, warnings

    if not isinstance(records, list):
        warnings.append("library.json has an unexpected format. Starting with "
                        "an empty library. " + backup_library_file())
        return books, warnings

    seen_ids = set()
    skipped = 0
    for position, record in enumerate(records, start=1):
        try:
            book = dict_to_book(record)
        except (KeyError, ValueError, TypeError):
            warnings.append(f"Skipped record #{position}: invalid data.")
            skipped += 1
            continue
        if book.book_id in seen_ids:
            warnings.append(f"Skipped record #{position}: duplicate ID {book.book_id}.")
            skipped += 1
            continue
        seen_ids.add(book.book_id)
        books.append(book)

    if skipped > 0:
        warnings.append(backup_library_file())
    return books, warnings


def save_books(books):
    """Save books to JSON safely. Returns True on success.

    Data is written to a temporary file first and then swapped in, so a
    failed write can never corrupt the existing library.json.
    """
    records = []
    for book in books:
        records.append(book.to_dict())

    temp_file = LIBRARY_FILE.with_suffix(".tmp")
    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
        temp_file.replace(LIBRARY_FILE)
        return True
    except (OSError, TypeError, ValueError) as error:
        print(f"[WARNING] Could not save library: {error}")
        return False
