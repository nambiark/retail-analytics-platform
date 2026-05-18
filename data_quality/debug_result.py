import great_expectations as gx
from dotenv import load_dotenv

load_dotenv()

context = gx.get_context(mode="file", project_root_dir="data_quality")

result = context.checkpoints.get("raw_tables_checkpoint").run()

print(f"\nOverall success: {result.success}")
print("\n--- Inspecting result structure ---")
for identifier, validation_result in result.run_results.items():
    print(f"\nIdentifier type: {type(identifier)}")
    print(f"Identifier attrs: {[a for a in dir(identifier) if not a.startswith('_')]}")
    print(f"Validation result keys: {validation_result.keys()}")
    break  # just inspect first one
