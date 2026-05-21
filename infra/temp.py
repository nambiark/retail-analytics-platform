import duckdb

duck = duckdb.connect("data/retail.duckdb")

print("=== Pipeline Stats ===")

orders = duck.execute("SELECT COUNT(*) FROM main_marts.fct_orders").fetchone()[0]
customers = duck.execute("SELECT COUNT(*) FROM main_marts.dim_customers").fetchone()[0]
products = duck.execute("SELECT COUNT(*) FROM main_marts.dim_products").fetchone()[0]
revenue = duck.execute("SELECT SUM(total_payment_value) FROM main_marts.fct_orders").fetchone()[0]
states = duck.execute("SELECT COUNT(DISTINCT customer_state) FROM main_marts.fct_orders").fetchone()[0]
categories = duck.execute("SELECT COUNT(DISTINCT category_name_en) FROM main_marts.dim_products").fetchone()[0]

print(f"Total orders:     {orders:,}")
print(f"Total customers:  {customers:,}")
print(f"Total products:   {products:,}")
print(f"Total revenue:    R$ {revenue:,.2f}")
print(f"States covered:   {states}")
print(f"Product categories: {categories}")

duck.close()