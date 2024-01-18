from authenticate import client
from variables import FUNCTION_NAME, FUNCTION_EXTERNAL_ID


if __name__ == "__main__":

    functions = client.functions.list(limit=-1).to_pandas()
    if not functions.empty and FUNCTION_EXTERNAL_ID in functions.external_id.values.tolist():
        client.functions.delete(external_id=FUNCTION_EXTERNAL_ID)
        print(f"Deleted function with external_id: {FUNCTION_EXTERNAL_ID}")
        
    func = client.functions.create(
        name=FUNCTION_NAME,
        external_id=FUNCTION_EXTERNAL_ID,
        folder=".",
        description="Scrape finn realestate data",
        runtime="py311",
        )
    print(f"Created function with external_id: {FUNCTION_EXTERNAL_ID}")
    
    schedule = client.functions.schedules.create(
        name="run-every-day",
        cron_expression="0 0 * * *",
        function_id=func.id,
        )
    print(f"Created schedule for function with external_id: {FUNCTION_EXTERNAL_ID}")