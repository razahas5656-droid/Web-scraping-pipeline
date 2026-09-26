# Automated Web Scraping & Data Extraction Pipeline

**Progree Data Science Internship — Task 2**

An automated Python pipeline that scrapes book listings from a public
practice site, cleans the extracted text, and stores the results in both
CSV and SQLite formats.

## Objective

Build an automated system pipeline that harvests data records from a
remote web environment, extracts target parameters using text-filtering
logic, cleans whitespace artifacts, and writes the final output to a
structured file.

## Source

[books.toscrape.com](https://books.toscrape.com) — a public website
built specifically for scraping practice, so the pipeline can run
without any legal/permission concerns.

## What it does

1. **Fetch** — downloads HTML for multiple catalogue pages using `requests`.
2. **Parse** — uses `BeautifulSoup` to locate each book listing and pull out:
   - Title
   - Price (GBP)
   - Availability
   - Star rating (converted from word to number)
3. **Clean** — strips newlines, tabs, and extra whitespace; converts
   messy price strings (e.g. `£53.74`) into clean floats.
4. **Store** — writes the final structured records to:
   - `books_data.csv`
   - `books_data.db` (SQLite, table `books`)

## Project structure

```
web-scraping-pipeline/
├── scraper.py          # main pipeline script
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## Setup & usage

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/web-scraping-pipeline.git
cd web-scraping-pipeline

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline
python scraper.py
```

This scrapes 5 pages (~100 books) by default and produces
`books_data.csv` and `books_data.db` in the project directory. To
scrape more pages, change `num_pages` in the `scrape_all()` call
inside `scraper.py`.

## Sample output

| title | price_gbp | availability | rating |
|---|---|---|---|
| A Light in the Attic | 51.77 | In stock | 3 |
| Tipping the Velvet | 53.74 | In stock | 1 |

## Tech stack

- Python 3
- `requests` — HTTP fetching
- `BeautifulSoup4` — HTML parsing
- `sqlite3` (standard library) — structured storage

## Author

Hasnain Raza — Progree Data Science Internship
