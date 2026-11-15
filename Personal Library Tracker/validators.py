"""Reusable input validation functions.

Every get_* function keeps asking until the input is valid, so bad input
never crashes the program. With allow_blank=True, pressing Enter returns
None (used for "keep the current value").
"""

import math
from datetime import date

MIN_YEAR = 1000
MAX_PAGES = 10000
MAX_RATING = 5
NAME_SYMBOLS = (" ", ".", "'", "-")


def read_input(prompt, allow_blank=False):
    """Read a stripped line; reject empty input unless allow_blank."""
    while True:
        value = input(prompt).strip()
        if value != "" or allow_blank:
            return value
        print("Input cannot be empty. Please try again.")


def get_int(prompt, minimum=None, maximum=None, allow_blank=False):
    """Read a whole number within optional limits."""
    while True:
        text = read_input(prompt, allow_blank)
        if text == "":
            return None
        try:
            number = int(text)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue
        if minimum is not None and number < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        if maximum is not None and number > maximum:
            print(f"Value must be at most {maximum}.")
            continue
        return number


def get_float(prompt, minimum=None, maximum=None, allow_blank=False):
    """Read a decimal number within optional limits."""
    while True:
        text = read_input(prompt, allow_blank)
        if text == "":
            return None
        try:
            number = float(text)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if not math.isfinite(number):
            print("Please enter a normal number.")
            continue
        if minimum is not None and number < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        if maximum is not None and number > maximum:
            print(f"Value must be at most {maximum}.")
            continue
        return number


def get_title(prompt, allow_blank=False):
    """Read a book title (1-100 chars, with a letter or digit)."""
    while True:
        text = read_input(prompt, allow_blank)
        if text == "":
            return None
        if len(text) > 100:
            print("Title is too long (maximum 100 characters).")
            continue
        for character in text:
            if character.isalnum():
                return text
        print("Title must contain at least one letter or digit.")


def get_author(prompt, allow_blank=False):
    """Read an author name (letters, spaces, . ' - only)."""
    while True:
        text = read_input(prompt, allow_blank)
        if text == "":
            return None
        if len(text) > 60:
            print("Name is too long (maximum 60 characters).")
            continue
        has_letter = False
        valid = True
        for character in text:
            if character.isalpha():
                has_letter = True
            elif character not in NAME_SYMBOLS:
                valid = False
                break
        if valid and has_letter:
            return text
        print("Names may contain only letters, spaces, periods, "
              "apostrophes and hyphens.")


def get_genre(prompt, allow_blank=False):
    """Read a genre (letters required) and return it in Title Case."""
    while True:
        text = read_input(prompt, allow_blank)
        if text == "":
            return None
        if len(text) > 40:
            print("Genre is too long (maximum 40 characters).")
            continue
        for character in text:
            if character.isalpha():
                return text.title()
        print("Genre must contain at least one letter.")


def get_year(prompt, allow_blank=False):
    """Read a publication year (1000 up to the current year)."""
    return get_int(prompt, MIN_YEAR, date.today().year, allow_blank)


def get_rating(prompt, allow_blank=False):
    """Read a rating between 0 and 5 (rounded to 1 decimal)."""
    rating = get_float(prompt, 0, MAX_RATING, allow_blank)
    if rating is None:
        return None
    return round(rating, 1)


def get_page_count(prompt, allow_blank=False):
    """Read a total page count (1 to 10000)."""
    return get_int(prompt, 1, MAX_PAGES, allow_blank)


def get_progress(prompt, total_pages, allow_blank=False):
    """Read pages completed (0 up to total_pages)."""
    return get_int(prompt, 0, total_pages, allow_blank)


def get_yes_no(prompt):
    """Return True for yes, False for no."""
    while True:
        answer = read_input(prompt).lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")
