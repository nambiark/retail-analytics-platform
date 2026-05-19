import subprocess
from prefect import task, get_run_logger
import os

DBT_PROJECT_DIR = os.path.join(os.path.dirname(__file__), "../../dbt")

@task(name="run_dbt_models", retries=1, retry_delay_seconds=30)
def run_dbt_models():
    logger = get_run_logger()
    logger.info("Running dbt models...")

    result = subprocess.run(
        ["dbt", "run", "--project-dir", DBT_PROJECT_DIR],
        capture_output=True,
        text=True
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(f"dbt run failed:\n{result.stderr}")

    logger.info("dbt run complete")
    return result.stdout

@task(name="run_dbt_tests", retries=0)
def run_dbt_tests():
    logger = get_run_logger()
    logger.info("Running dbt tests...")

    result = subprocess.run(
        ["dbt", "test", "--project-dir", DBT_PROJECT_DIR],
        capture_output=True,
        text=True
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(f"dbt tests failed:\n{result.stderr}")

    logger.info("dbt tests complete")
    return result.stdout

@task(name="run_dbt_snapshot")
def run_dbt_snapshot():
    logger = get_run_logger()
    logger.info("Running dbt snapshots...")

    result = subprocess.run(
        ["dbt", "snapshot", "--project-dir", DBT_PROJECT_DIR],
        capture_output=True,
        text=True
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(f"dbt snapshot failed:\n{result.stderr}")

    logger.info("dbt snapshot complete")
    return result.stdout
