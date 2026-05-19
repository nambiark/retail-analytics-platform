from prefect import task, get_run_logger
import great_expectations as gx
from dotenv import load_dotenv

load_dotenv()

@task(name="validate_raw_data", retries=1, retry_delay_seconds=10)
def validate_raw_data():
    logger = get_run_logger()
    logger.info("Running Great Expectations validation...")

    context = gx.get_context(mode="file", project_root_dir="data_quality")
    result = context.checkpoints.get("raw_tables_checkpoint").run()

    passed = 0
    failed = 0
    for identifier, vr in result.run_results.items():
        suite_name = vr["suite_name"]
        stats = vr["statistics"]
        suite_passed = stats["successful_expectations"]
        suite_total = stats["evaluated_expectations"]
        passed += suite_passed
        failed += suite_total - suite_passed
        logger.info(f"  {suite_name}: {suite_passed}/{suite_total} passed")

    logger.info(f"Validation complete — {passed} passed, {failed} failed")

    if not result.success:
        raise ValueError(
            f"Data validation failed — {failed} expectations did not pass. "
            f"Check GE data docs for details."
        )

    return {"passed": passed, "failed": failed}
