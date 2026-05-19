import duckdb
import pandas as pd
from sqlalchemy import create_engine
from prefect import task, get_run_logger
from dotenv import load_dotenv
import os

load_dotenv()

@task(name="load_raw_to_duckdb", retries=2, retry_delay_seconds=30)
def load_raw_to_duckdb():
    logger = get_run_logger()

    pg_engine = create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

    duck = duckdb.connect("data/retail.duckdb")
    duck.execute("CREATE SCHEMA IF NOT EXISTS raw")

    tables = [
        "orders", "customers", "order_items", "payments",
        "reviews", "products", "sellers", "geolocation",
        "category_translation"
    ]

    for table in tables:
        logger.info(f"Loading {table} into DuckDB...")
        df = pd.read_sql(f"SELECT * FROM raw.{table}", pg_engine)
        duck.execute(f"DROP TABLE IF EXISTS raw.{table}")
        duck.execute(f"CREATE TABLE raw.{table} AS SELECT * FROM df")
        count = duck.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        logger.info(f"  ✓ {count} rows loaded into raw.{table}")

    duck.close()
    logger.info("DuckDB load complete")
    return len(tables)
