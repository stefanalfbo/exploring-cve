SHELL := /bin/bash

# Determine the absolute directory of the Makefile
MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

# Export the AIRFLOW_HOME environment variable, it has to be an absolute path
export AIRFLOW_HOME := $(MAKEFILE_DIR)

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

airflow-standalone: ## The airflow standalone command initializes the database, creates a user, and starts all components
	uv run airflow standalone

airflow-migrate: ## Initialize the database tables
	uv run airflow db migrate

airflow-webserver: ## Start the Airflow webserver
	uv run airflow webserver -p 8080

airflow-create-user: ## Create a new user
	uv run airflow users create -r Admin -u admin -p password -e admin@example.com -f admin -l user

airflow-scheduler: ## Start the Airflow scheduler
	uv run airflow scheduler