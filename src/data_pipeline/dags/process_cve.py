from airflow.decorators import dag, task
from datetime import datetime
import requests
from pathlib import Path

def github_release():
    GITHUB_OWNER = "CVEProject"
    GITHUB_REPO = "cvelistV5"
    RELEASE_TAG = "cve_2025-02-14_1800Z"
    ASSET_NAME = "2025-02-14_all_CVEs_at_midnight.zip.zip"

    release_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/tags/{RELEASE_TAG}"

    headers = {
        "Accept": "application/vnd.github.raw"
    }

    response = requests.get(release_url, headers=headers)
    response.raise_for_status() 

    release_data = response.json()

    assets = release_data.get("assets", [])
    asset = next((a for a in assets if a["name"] == ASSET_NAME), None)
    if not asset:
        raise ValueError(f"Asset '{ASSET_NAME}' not found in release {RELEASE_TAG}.")

    download_url = asset["browser_download_url"]

    print(f"Downloading {ASSET_NAME} from {download_url}...")
    zip_response = requests.get(download_url, headers=headers, stream=True)

    print(f"Response status code: {zip_response.status_code}")
    zip_response.raise_for_status()

    file_path = Path("data") / ASSET_NAME
    with open(file_path, "wb") as file:
        for chunk in zip_response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Download complete: {ASSET_NAME}")

    return str(file_path)

@dag(
    start_date=datetime(year=2023, month=1, day=1, hour=9, minute=0),
    schedule="@daily",
    catchup=True,
    max_active_runs=1
)
def ProcessCVE():
    @task()
    def extract():
        # Download from GitHub the latest release
        return github_release()

    @task()
    def transform(file):
        # Transform response to a list
        print(f"Transforming file: {file}")
        return file

    @task()
    def load(file):
        print(f"Loading file: {file}")

    # Set dependencies using function calls
    file = extract()
    transformed_files = transform(file)
    load(transformed_files)


# Allow the DAG to be run
dag = ProcessCVE()

