import pandas as pd
import sqlite3
import os

PROCESSED_DATA_PATH = "data/processed/flipkart_smartphones_cleaned.csv"
DB_PATH = "data/flipkart_smartphones.db"


def create_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to database: {DB_PATH}")
    return conn


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name  TEXT NOT NULL UNIQUE,
            brand         TEXT,
            price_segment TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name   TEXT NOT NULL,
            brand          TEXT,
            current_price  INTEGER,
            original_mrp   REAL,
            discount_pct   REAL,
            rating         REAL,
            ratings_count  INTEGER,
            review_count   INTEGER,
            scraped_at     TEXT,
            scraped_date   TEXT,
            page_number    INTEGER
        )
    """)
    conn.commit()
    print("Tables created: products, price_history")


def load_data(conn):
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Cleaned CSV not found at {PROCESSED_DATA_PATH}")
        print("Run 01_data_cleaning.ipynb first.")
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    print(f"Loaded {len(df)} rows from cleaned CSV")

    # Load all rows into price_history
    df.to_sql("price_history", conn, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into price_history table")

    # Load unique products into products table
    products_df = (
        df[["product_name", "brand"]]
        .drop_duplicates(subset=["product_name"])
        .reset_index(drop=True)
    )
    products_df.to_sql("products", conn, if_exists="replace", index=False)
    print(f"Loaded {len(products_df)} unique products into products table")

    conn.commit()


def verify_load(conn):
    cursor = conn.cursor()
    print("\n── Verification ───────────────────────────────")

    cursor.execute("SELECT COUNT(*) FROM price_history")
    print(f"Total rows in price_history : {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM products")
    print(f"Total unique products       : {cursor.fetchone()[0]}")

    cursor.execute("""
        SELECT scraped_date, COUNT(*) 
        FROM price_history 
        GROUP BY scraped_date 
        ORDER BY scraped_date
    """)
    print(f"\nRows per day:")
    for row in cursor.fetchall():
        print(f"  {row[0]} → {row[1]} rows")

    cursor.execute("""
        SELECT brand, COUNT(DISTINCT product_name) 
        FROM price_history 
        GROUP BY brand 
        ORDER BY COUNT(DISTINCT product_name) DESC
    """)
    print(f"\nProducts per brand:")
    for row in cursor.fetchall():
        print(f"  {row[0]:<12} {row[1]}")


if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
    load_data(conn)
    verify_load(conn)
    conn.close()
    print("\nDatabase ready. Run SQL queries now!")