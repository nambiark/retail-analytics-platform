from prefect import task, get_run_logger
import subprocess
import os

@task(name="sync_marts_to_postgres", retries=1, retry_delay_seconds=15)
def sync_marts_to_postgres():
    logger = get_run_logger()
    logger.info("Syncing marts to Postgres for Metabase...")

    result = subprocess.run(
        ["python", "infra/sync_marts_to_postgres.py"],
        capture_output=True,
        text=True
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError(f"Mart sync failed:\n{result.stderr}")

    logger.info("Sync complete")
    return True
