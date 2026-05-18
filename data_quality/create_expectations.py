import great_expectations as gx
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize context (stored in data_quality/gx/)
context = gx.get_context(mode="file", project_root_dir="data_quality")

# ── Connect to Postgres ─────────────────────────────────────
connection_string = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

datasource = context.data_sources.add_or_update_postgres(
    name="retail_postgres",
    connection_string=connection_string,
)

# ── Orders ──────────────────────────────────────────────────
orders_asset = datasource.add_table_asset(name="orders", table_name="orders", schema_name="raw")
orders_batch = orders_asset.add_batch_definition_whole_table("orders_full")

orders_suite = context.suites.add(gx.ExpectationSuite(name="orders.raw"))
orders_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
orders_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
orders_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id"))
orders_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="order_status",
    value_set=["delivered","shipped","canceled","unavailable","invoiced","processing","created","approved"]
))
orders_suite.add_expectation(gx.expectations.ExpectTableRowCountToBeBetween(min_value=90000, max_value=110000))
orders_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_purchase_timestamp"))
print("✓ orders.raw suite created")

# ── Payments ────────────────────────────────────────────────
payments_asset = datasource.add_table_asset(name="payments", table_name="payments", schema_name="raw")
payments_batch = payments_asset.add_batch_definition_whole_table("payments_full")

payments_suite = context.suites.add(gx.ExpectationSuite(name="payments.raw"))
payments_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
payments_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="payment_value"))
payments_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="payment_value", min_value=0
))
payments_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
    column="payment_type",
    value_set=["credit_card","boleto","voucher","debit_card","not_defined"]
))
payments_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="payment_installments", min_value=1, max_value=24,
    mostly=0.99
))
print("✓ payments.raw suite created")

# ── Products ────────────────────────────────────────────────
products_asset = datasource.add_table_asset(name="products", table_name="products", schema_name="raw")
products_batch = products_asset.add_batch_definition_whole_table("products_full")

products_suite = context.suites.add(gx.ExpectationSuite(name="products.raw"))
products_suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="product_id"))
products_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="product_id"))
products_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="product_weight_g", min_value=0, mostly=0.95
))
products_suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
    column="product_length_cm", min_value=0, mostly=0.95
))
print("✓ products.raw suite created")

print("\nAll suites created successfully.")
