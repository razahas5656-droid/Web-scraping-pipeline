import re
import sqlite3
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraping project)"}

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(page_num: int) -> str:
    """Download raw HTML for a single catalogue page."""
    url = BASE_URL.format(page_num)
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


def clean_text(raw: str) -> str:
    """Strip whitespace artifacts (newlines, tabs, double spaces, currency junk)."""
    if raw is None:
        return ""
    text = raw.replace("\n", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_price(raw_price: str) -> float:
    """Pull a clean float out of a messy price string like '£53.74'."""
    cleaned = re.sub(r"[^\d.]", "", raw_price)
    return float(cleaned) if cleaned else 0.0


def parse_page(html: str) -> list[dict]:
    """Extract target parameters (title, price, rating, availability) from one page."""
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for article in soup.select("article.product_pod"):
        title_raw = article.h3.a["title"]
        price_raw = article.select_one(".price_color").get_text()
        availability_raw = article.select_one(".availability").get_text()
        rating_class = article.select_one("p.star-rating")["class"]
        rating_word = next((c for c in rating_class if c in RATING_WORDS), "Zero")

        record = {
            "title": clean_text(title_raw),
            "price_gbp": extract_price(price_raw),
            "availability": clean_text(availability_raw),
            "rating": RATING_WORDS.get(rating_word, 0),
        }
        records.append(record)

    return records


def scrape_all(num_pages: int = 5) -> list[dict]:
    """Loop over multiple pages to build the full dataset (polite delay included)."""
    all_records = []
    for page_num in range(1, num_pages + 1):
        print(f"Scraping page {page_num}/{num_pages} ...")
        html = fetch_page(page_num)
        all_records.extend(parse_page(html))
        time.sleep(0.5)  # be polite to the server
    return all_records


def save_to_csv(records: list[dict], path: str) -> None:
    import csv

    if not records:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} records to {path}")


def save_to_sqlite(records: list[dict], path: str) -> None:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price_gbp REAL,
            availability TEXT,
            rating INTEGER
        )
        """
    )
    cur.execute("DELETE FROM books")  # keep the table fresh on re-run
    cur.executemany(
        "INSERT INTO books (title, price_gbp, availability, rating) VALUES "
        "(:title, :price_gbp, :availability, :rating)",
        records,
    )
    conn.commit()
    conn.close()
    print(f"Saved {len(records)} records to {path}")


def main():
    output_dir = Path(__file__).parent
    data = scrape_all(num_pages=5)  # ~100 book records
    save_to_csv(data, output_dir / "books_data.csv")
    save_to_sqlite(data, output_dir / "books_data.db")
    print("\nSample record:", data[0] if data else "No data scraped.")


if __name__ == "__main__":
    main()
