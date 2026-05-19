import duckdb
from prefect import task, get_run_logger

@task(name="validate_marts")
def validate_marts():
    logger = get_run_logger()
    logger.info("Running mart-level sanity checks...")

    duck = duckdb.connect("data/retail.duckdb")

    checks = [
        (
            "fct_orders row count",
            "SELECT COUNT(*) FROM main_marts.fct_orders",
            lambda x: x > 0
        ),
        (
            "fct_orders no null order_ids",
            "SELECT COUNT(*) FROM main_marts.fct_orders WHERE order_id IS NULL",
            lambda x: x == 0
        ),
        (
            "dim_customers row count",
            "SELECT COUNT(*) FROM main_marts.dim_customers",
            lambda x: x > 0
        ),
        (
            "dim_products row count",
            "SELECT COUNT(*) FROM main_marts.dim_products",
            lambda x: x > 0
        ),
        (
            "fct_orders total revenue positive",
            "SELECT SUM(total_payment_value) FROM main_marts.fct_orders",
            lambda x: x > 0
        ),
    ]

    failed_checks = []
    for check_name, query, assertion in checks:
        value = duck.execute(query).fetchone()[0]
        passed = assertion(value)
        status = "✓" if passed else "✗"
        logger.info(f"  {status} {check_name}: {value}")
        if not passed:
            failed_checks.append(check_name)

    duck.close()

    if failed_checks:
        raise ValueError(f"Mart validation failed: {failed_checks}")

    logger.info("All mart checks passed")
    return True
