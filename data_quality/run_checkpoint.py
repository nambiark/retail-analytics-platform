import great_expectations as gx
from dotenv import load_dotenv

load_dotenv()

context = gx.get_context(mode="file", project_root_dir="data_quality")

datasource = context.data_sources.get("retail_postgres")

validations = [
    gx.ValidationDefinition(
        name="validate_orders",
        data=datasource.get_asset("orders").get_batch_definition("orders_full"),
        suite=context.suites.get("orders.raw"),
    ),
    gx.ValidationDefinition(
        name="validate_payments",
        data=datasource.get_asset("payments").get_batch_definition("payments_full"),
        suite=context.suites.get("payments.raw"),
    ),
    gx.ValidationDefinition(
        name="validate_products",
        data=datasource.get_asset("products").get_batch_definition("products_full"),
        suite=context.suites.get("products.raw"),
    ),
]

for vd in validations:
    try:
        context.validation_definitions.add(vd)
    except Exception:
        context.validation_definitions.delete(vd.name)
        context.validation_definitions.add(vd)

checkpoint = gx.Checkpoint(
    name="raw_tables_checkpoint",
    validation_definitions=validations,
    actions=[gx.checkpoint.UpdateDataDocsAction(name="update_data_docs")],
)

try:
    context.checkpoints.add(checkpoint)
except Exception:
    context.checkpoints.delete("raw_tables_checkpoint")
    context.checkpoints.add(checkpoint)

result = context.checkpoints.get("raw_tables_checkpoint").run()

print(f"\nOverall success: {result.success}")
for identifier, vr in result.run_results.items():
    suite_name = vr["suite_name"]
    stats = vr["statistics"]
    print(f"  {suite_name}: {stats['successful_expectations']}/{stats['evaluated_expectations']} passed")

context.open_data_docs()
