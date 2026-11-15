# Personal Library & Reading Tracker

A terminal-based Python app to manage a personal book collection, track
reading progress, search and filter books, and generate reports.
Built with Python 3 and built-in libraries only.

## Features
- Add, view, search (ID / title / author), update and delete books
- Page-based progress with automatic status: Unread, Reading, Completed
- Filter by genre or reading status
- Reading statistics (totals, overall progress, average rating)
- Export to CSV and generate a TXT reading report
- Automatic JSON saving after every successful change
- Safe handling of invalid input and missing, empty or malformed JSON

## Project Structure
```
Personal-Library-Tracker/
├── main.py         # Menu loop, coordinates all modules
├── book.py         # Book class + fixed STATUSES tuple
├── library.py      # Library class (collection operations)
├── storage.py      # JSON load/save
├── reports.py      # Statistics, CSV export, TXT report
├── validators.py   # Input validation functions
├── data/
│   ├── library.json
│   ├── library_export.csv
│   └── reading_report.txt
└── README.md
```

Import flow (no circular imports):
`main -> library -> reports -> storage -> book`

## How to Run
```
python main.py
```
Requires Python 3.6 or newer. No installation or internet needed.

## Example Usage
```
Enter your choice: 1
Book ID (press Enter for 4):
Title: Clean Code
Author: Robert Martin
Genre: technology
Publication year: 2008
Rating (0-5, use 0 if not rated): 4.5
Total pages: 464
Pages completed: 0
[SUCCESS] Book 'Clean Code' added successfully.

Enter your choice: 6
Enter Book ID: 4
Pages completed (0-464): 100
[SUCCESS] Progress updated: 100/464 pages (21.6%) - status: Reading.
```

## Notes
- A rating of 0 means "not rated" and is excluded from the average rating.
- If `library.json` is malformed, the original is copied to
  `data/library_backup.json` and the app starts with an empty library.
- `library_export.csv` and `reading_report.txt` are regenerated
  by menu options 9 and 10.
