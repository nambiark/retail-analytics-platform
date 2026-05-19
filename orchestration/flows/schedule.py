from prefect import serve
from retail_pipeline import retail_pipeline
from datetime import timedelta

if __name__ == "__main__":
    # runs every day at 6am
    retail_pipeline.serve(
        name="retail-daily",
        cron="0 6 * * *",
        description="Daily retail pipeline — ingest, validate, transform",
    )
