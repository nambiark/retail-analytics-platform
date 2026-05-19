from prefect import flow, get_run_logger
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from orchestration.tasks.load_data import load_raw_to_duckdb
from orchestration.tasks.validate_data import validate_raw_data
from orchestration.tasks.run_dbt import run_dbt_models, run_dbt_tests, run_dbt_snapshot
from orchestration.tasks.validate_marts import validate_marts

@flow(
    name="retail-analytics-pipeline",
    description="End-to-end retail data pipeline: ingest → validate → transform → test",
    log_prints=True,
)
def retail_pipeline(full_refresh: bool = False):
    logger = get_run_logger()
    logger.info("Starting retail analytics pipeline...")

    tables_loaded = load_raw_to_duckdb()
    logger.info(f"Loaded {tables_loaded} tables")

    validation_result = validate_raw_data()
    logger.info(f"Validation passed: {validation_result}")

    dbt_result = run_dbt_models()
    snapshot_result = run_dbt_snapshot()
    test_result = run_dbt_tests()

    marts_valid = validate_marts()

    logger.info("Pipeline completed successfully")
    return {
        "tables_loaded": tables_loaded,
        "validation": validation_result,
        "marts_valid": marts_valid,
    }

if __name__ == "__main__":
    retail_pipeline()
