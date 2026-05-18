import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

csv_files = {
    "orders":       "data/raw/olist_orders_dataset.csv",
    "customers":    "data/raw/olist_customers_dataset.csv",
    "order_items":  "data/raw/olist_order_items_dataset.csv",
    "payments":     "data/raw/olist_order_payments_dataset.csv",
    "reviews":      "data/raw/olist_order_reviews_dataset.csv",
    "products":     "data/raw/olist_products_dataset.csv",
    "sellers":      "data/raw/olist_sellers_dataset.csv",
    "geolocation":  "data/raw/olist_geolocation_dataset.csv",
    "category_translation": "data/raw/product_category_name_translation.csv",
}

for table_name, filepath in csv_files.items():
    print(f"Loading {table_name}...")
    df = pd.read_csv(filepath)
    df.to_sql(table_name, engine, schema="raw", if_exists="replace",
              index=False)
    print(f"  ✓ {len(df)} rows loaded into raw.{table_name}")

print("\nAll tables loaded successfully.")
