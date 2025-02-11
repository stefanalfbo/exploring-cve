from airflow.decorators import dag, task
from datetime import datetime


@dag(
    start_date=datetime(year=2023, month=1, day=1, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1
)
def ProcessCVE():
    @task()
    def extract():
        # Print message, return a response
        print("Extracting data CVE API")
        return {
            "date": "2023-01-01",
            "location": "NYC",
            "weather": {
                "temp": 33,
                "conditions": "Light snow and wind"
            }
        }

    @task()
    def transform(raw_data):
        # Transform response to a list
        transformed_data = [
            [
                raw_data.get("date"),
                raw_data.get("location"),
                raw_data.get("weather").get("temp"),
                raw_data.get("weather").get("conditions")
            ]
        ]
        return transformed_data

    @task()
    def load(transformed_data):
        print(transformed_data)

    # Set dependencies using function calls
    raw_dataset = extract()
    transformed_dataset = transform(raw_dataset)
    load(transformed_dataset)


# Allow the DAG to be run
dag = ProcessCVE()
