import duckdb
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

pg_engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

duck = duckdb.connect("data/retail.duckdb")

# create marts schema in postgres
with pg_engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS marts"))
    conn.commit()

marts = {
    "fct_orders":    "SELECT * FROM main_marts.fct_orders",
    "dim_customers": "SELECT * FROM main_marts.dim_customers",
    "dim_products":  "SELECT * FROM main_marts.dim_products",
}

for table_name, query in marts.items():
    print(f"Syncing {table_name}...")
    df = duck.execute(query).df()

    # convert boolean columns — postgres handles them differently
    bool_cols = df.select_dtypes(include='bool').columns
    for col in bool_cols:
        df[col] = df[col].astype(str)

    df.to_sql(
        table_name,
        pg_engine,
        schema="marts",
        if_exists="replace",
        index=False
    )
    print(f"  ✓ {len(df)} rows synced to marts.{table_name}")

duck.close()
print("\nSync complete.")
