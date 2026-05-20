from prefect import flow, get_run_logger
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from orchestration.tasks.load_data import load_raw_to_duckdb
from orchestration.tasks.validate_data import validate_raw_data
from orchestration.tasks.run_dbt import run_dbt_models, run_dbt_tests, run_dbt_snapshot
from orchestration.tasks.validate_marts import validate_marts
from orchestration.tasks.sync_marts import sync_marts_to_postgres

@flow(
    name="retail-analytics-pipeline",
    description="End-to-end retail pipeline: ingest → validate → transform → test → serve",
    log_prints=True,
)
def retail_pipeline():
    logger = get_run_logger()
    logger.info("Starting retail analytics pipeline...")

    # 1 — load raw data
    tables_loaded = load_raw_to_duckdb()

    # 2 — validate raw (blocks pipeline if data quality fails)
    validation_result = validate_raw_data()

    # 3 — transform
    dbt_result = run_dbt_models()

    # 4 — snapshot (SCD Type 2)
    snapshot_result = run_dbt_snapshot()

    # 5 — test
    test_result = run_dbt_tests()

    # 6 — validate marts
    marts_valid = validate_marts()

    # 7 — sync to postgres for Metabase
    synced = sync_marts_to_postgres()

    logger.info("Pipeline completed successfully")
    return {
        "tables_loaded": tables_loaded,
        "validation": validation_result,
        "marts_valid": marts_valid,
        "synced_to_postgres": synced,
    }

if __name__ == "__main__":
    retail_pipeline()
