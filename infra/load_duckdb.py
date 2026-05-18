import duckdb
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to both
pg_engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

os.makedirs("data", exist_ok=True)
duck = duckdb.connect("data/retail.duckdb")
duck.execute("CREATE SCHEMA IF NOT EXISTS raw")

tables = [
    "orders", "customers", "order_items", "payments",
    "reviews", "products", "sellers", "geolocation",
    "category_translation"
]

for table in tables:
    print(f"Copying {table}...")
    df = pd.read_sql(f"SELECT * FROM raw.{table}", pg_engine)
    duck.execute(f"DROP TABLE IF EXISTS raw.{table}")
    duck.execute(f"CREATE TABLE raw.{table} AS SELECT * FROM df")
    count = duck.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
    print(f"  ✓ {count} rows loaded into raw.{table}")

duck.close()
print("\nDuckDB loaded successfully.")
