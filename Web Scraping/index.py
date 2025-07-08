import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = ["Title", "Price (₹)", "Rating"]

def get_rating_value(rating_str):
    values = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return values.get(rating_str, 0)

def scrape_books(pages=5):
    all_books = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select(".product_pod")

        for book in books:
            title = book.h3.a["title"]

            # Fix encoding issue and clean price
            raw_price = book.select_one(".price_color").text.strip()
            price_text = raw_price.encode("latin1").decode("utf-8").replace("£", "").strip()
            price = float(price_text)

            rating_class = book.select_one(".star-rating")["class"][1]
            rating_value = get_rating_value(rating_class)

            all_books.append({
                "Title": title,
                "Price (₹)": price,
                "Rating": rating_value
            })

    # Sort by rating (descending), then by price (ascending)
    all_books.sort(key=lambda x: (-x["Rating"], x["Price (₹)"]))
    return all_books

def save_to_csv(data, filename="books.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for book in data:
            writer.writerow({
                "Title": book["Title"],
                "Price (₹)": f"{book['Price (₹)']:.2f}",
                "Rating": book["Rating"]
            })

if __name__ == "__main__":
    print("🔍 Scraping book data...")
    books = scrape_books(pages=5)
    save_to_csv(books)
    print(f"✅ Done! {len(books)} books saved to books.csv")