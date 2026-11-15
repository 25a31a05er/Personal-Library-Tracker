"""Statistics, CSV export and TXT report generation."""

import csv
from datetime import datetime

from book import STATUSES
from storage import DATA_DIR

EXPORT_FILE = DATA_DIR / "library_export.csv"
REPORT_FILE = DATA_DIR / "reading_report.txt"
CSV_HEADERS = ("book_id", "title", "author", "genre", "year", "rating",
               "total_pages", "pages_completed", "completion_percent", "status")


def calculate_statistics(books):
    """Return a dictionary of statistics for the given books."""
    status_counts = {}
    for status in STATUSES:
        status_counts[status] = 0

    genre_counts = {}
    total_pages = 0
    pages_completed = 0
    rating_sum = 0.0
    rated_books = 0

    for book in books:
        status_counts[book.status] += 1
        genre_counts[book.genre] = genre_counts.get(book.genre, 0) + 1
        total_pages += book.total_pages
        pages_completed += book.pages_completed
        if book.rating > 0:
            rating_sum += book.rating
            rated_books += 1

    overall_progress = 0.0
    if total_pages > 0:
        overall_progress = pages_completed / total_pages * 100
    average_rating = 0.0
    if rated_books > 0:
        average_rating = rating_sum / rated_books

    return {
        "total_books": len(books),
        "status_counts": status_counts,
        "genre_counts": genre_counts,
        "total_pages": total_pages,
        "pages_completed": pages_completed,
        "overall_progress": overall_progress,
        "average_rating": average_rating,
    }


def build_statistics_lines(stats):
    """Turn a statistics dictionary into printable lines."""
    counts = stats["status_counts"]
    lines = [
        "READING STATISTICS",
        "------------------",
        f"Total books       : {stats['total_books']}",
        f"Completed         : {counts['Completed']}",
        f"Currently reading : {counts['Reading']}",
        f"Unread            : {counts['Unread']}",
        f"Total pages       : {stats['total_pages']}",
        f"Pages completed   : {stats['pages_completed']}",
        f"Overall progress  : {stats['overall_progress']:.1f}%",
        f"Average rating    : {stats['average_rating']:.2f} (rated books only)",
    ]
    if stats["genre_counts"]:
        lines.append("")
        lines.append("Books by genre:")
        for genre in sorted(stats["genre_counts"]):
            lines.append(f"  - {genre}: {stats['genre_counts'][genre]}")
    return lines


def display_statistics(stats):
    """Print statistics to the terminal."""
    for line in build_statistics_lines(stats):
        print(line)


def export_to_csv(books, file_path=EXPORT_FILE):
    """Export all books to a CSV file. Returns (success, message)."""
    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)
            for book in books:
                writer.writerow([
                    book.book_id, book.title, book.author, book.genre,
                    book.year, book.rating, book.total_pages,
                    book.pages_completed,
                    round(book.completion_percentage(), 1), book.status,
                ])
    except OSError as error:
        return False, f"Could not export CSV: {error}"
    return True, f"Exported {len(books)} book(s) to {file_path}"


def generate_report(books, stats, file_path=REPORT_FILE):
    """Write a readable TXT report. Returns (success, message)."""
    lines = [
        "========================================",
        "        PERSONAL READING REPORT",
        "========================================",
        "Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
    ]
    lines.extend(build_statistics_lines(stats))
    lines.append("")
    lines.append("BOOKS BY STATUS")
    lines.append("------------------")

    for status in STATUSES:
        matching = []
        for book in books:
            if book.status == status:
                matching.append(book)
        lines.append(f"{status} ({len(matching)})")
        for book in matching:
            if book.rating > 0:
                rating_text = f"Rating: {book.rating:.1f}"
            else:
                rating_text = "Not rated"
            lines.append(
                f"  [{book.book_id}] {book.title} by {book.author} - "
                f"{book.pages_completed}/{book.total_pages} pages "
                f"({book.completion_percentage():.1f}%) - {rating_text}"
            )
        lines.append("")

    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")
    except OSError as error:
        return False, f"Could not write report: {error}"
    return True, f"Reading report saved to {file_path}"
