import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import os
import re

BASE_URL = "https://www.flipkart.com/search?q=smartphones&page={page}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def get_page(url):
    """Fetching a Flipkart listing page and returning BeautifulSoup object."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"  Error fetching {url}: {e}")
        return None


def extract_brand(product_name):
    """Extracting brand from product name (first word)."""
    brands = [
        "Samsung", "Apple", "OnePlus", "Realme", "Redmi",
        "Xiaomi", "Vivo", "OPPO", "Motorola", "Nokia", "iQOO"
    ]
    for brand in brands:
        if brand.lower() in product_name.lower():
            return brand
    return product_name.split()[0]


def clean_price(price_str):
    """Converting '₹18,999' to integer 18999."""
    if not price_str:
        return None
    cleaned = price_str.replace("₹", "").replace(",", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        return None


def parse_products(soup):
    """Extracting product data from a Flipkart listing page."""
    products = []


    product_cards = soup.find_all("div", class_="jIjQ8S")

    for card in product_cards:
        try:
            # Product name
            name_tag = card.find("div", class_="RG5Slk")
            if not name_tag:
                continue
            name = name_tag.get_text(strip=True)
            if len(name) < 5:
                continue

            # Current price
            price_tag = card.find("div", class_="hZ3P6w")
            current_price = clean_price(
                price_tag.get_text() if price_tag else None
            )

            # Original MRP
            mrp_tag = card.find("div", class_="kRYCnD")
            original_mrp = clean_price(
                mrp_tag.get_text() if mrp_tag else None
            )

            # Discount percentage
            discount_tag = card.find("div", class_="HQe8jr")
            discount_pct = None
            if discount_tag:
                disc_text = discount_tag.get_text(strip=True)
                disc_text = disc_text.replace("%", "").replace("off", "").strip()
                try:
                    discount_pct = float(disc_text)
                except ValueError:
                    pass

            # Rating badge
            rating_tag = card.find("div", class_="MKiFS6")
            rating = None
            if rating_tag:
                rating_text = rating_tag.get_text(strip=True)
                rating_text = rating_text.replace("★", "").strip()
                try:
                    rating = float(rating_text)
                except ValueError:
                    pass

            # Ratings & Reviews
            review_count = None
            ratings_count = None
            review_span = card.find("span", class_="PvbNMB")
            if review_span:
                text = review_span.get_text(separator=" ", strip=True)
                numbers = re.findall(r"[\d,]+", text)
                if len(numbers) >= 1:
                    ratings_count = int(numbers[0].replace(",", ""))
                if len(numbers) >= 2:
                    review_count = int(numbers[1].replace(",", ""))

            if current_price:  # only save if we got a price
                products.append({
                    "product_name": name,
                    "brand": extract_brand(name),
                    "current_price": current_price,
                    "original_mrp": original_mrp,
                    "discount_pct": discount_pct,
                    "rating": rating,
                    "ratings_count": ratings_count,
                    "review_count": review_count,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })

        except Exception as e:
            print(f"  Skipping a card due to error: {e}")
            continue

    return products


def scrape_flipkart(num_pages=8):
    """Scraping num_pages of Flipkart smartphone listings."""
    all_products = []
    print(f"Starting scrape: {num_pages} pages...")

    for page in range(1, num_pages + 1):
        url = BASE_URL.format(page=page)
        print(f"  Scraping page {page}...")

        soup = get_page(url)
        if soup:
            products = parse_products(soup)
            for p in products:
                p["page_number"] = page
            all_products.extend(products)
            print(f"  Found {len(products)} products on page {page}")

        # waiting 2-4 seconds between requests
        time.sleep(random.uniform(2, 4))

    return all_products


def save_to_csv(products):
    """Saving scraped products to a date-stamped CSV file."""
    if not products:
        print("No products to save.")
        return None

    # Ensuring the data/raw folder exists before trying to save
    os.makedirs("data/raw", exist_ok=True)

    df = pd.DataFrame(products)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/raw/flipkart_smartphones_{date_str}.csv"

    # Appending to existing file if it already exists today
    if os.path.exists(filename):
        existing = pd.read_csv(filename)
        df = pd.concat([existing, df], ignore_index=True)
        df = df.drop_duplicates(
            subset=["product_name", "scraped_at"]
        )

    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} rows to {filename}")
    return filename


if __name__ == "__main__":
    products = scrape_flipkart(num_pages=8)
    print(f"\nTotal products scraped: {len(products)}")
    save_to_csv(products)
    print("Done!")