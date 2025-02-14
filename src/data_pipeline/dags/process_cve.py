from airflow.decorators import dag, task
from datetime import datetime
import os
import requests


@dag(
    start_date=datetime(year=2023, month=1, day=1, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1
)
def ProcessCVE():
    @task()
    def extract():
        year = 2024
        folder = f"data/{year}"
        os.makedirs(folder, exist_ok=True)
        cve_files = []

        for i in range(1, 10000):
            file_name = f"CVE-{year}-{i:04d}.json"
            url = f"https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{year}/0xxx/{file_name}"
            response = requests.get(url)
            if response.status_code == 404:
                break
            if response.status_code == 200:
                file = os.path.join(folder, file_name)
                with open(file, "w") as f:
                    f.write(response.text)
                cve_files.append(file)

        return cve_files

    @task()
    def transform(files):
        # Transform response to a list
        return files

    @task()
    def load(files):
        for file in files:
            print(f"Loading file: {file}")

    # Set dependencies using function calls
    files = extract()
    transformed_files = transform(files)
    load(transformed_files)


# Allow the DAG to be run
dag = ProcessCVE()
