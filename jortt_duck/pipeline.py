"""DLT pipeline for ingesting Jortt API data into local DuckDB."""

import dlt
from dlt.sources.rest_api import rest_api_source


def get_jortt_config(access_token: str) -> dict:
    """Get the declarative REST API configuration for Jortt API.

    Args:
        access_token: OAuth access token for Jortt API

    Returns:
        Configuration dictionary for dlt rest_api_source
    """
    return {
        "client": {
            "base_url": "https://api.jortt.nl",
            "auth": {
                "type": "bearer",
                "token": access_token,
            },
            "paginator": {
                "type": "json_link",
                "next_url_path": "_links.next.href",
            },
        },
        "resource_defaults": {
            "write_disposition": "replace",
            "primary_key": "aggregate_id",
        },
        "resources": [
            {
                "name": "projects",
                "endpoint": {
                    "path": "projects",
                    "params": {
                        "per_page": 100,
                    },
                    "data_selector": "data",
                },
            },
            {
                "name": "project_line_items",
                "write_disposition": "replace",
                "primary_key": None,
                "endpoint": {
                    "path": "projects/{aggregate_id}/line_items",
                    "params": {
                        "aggregate_id": {
                            "type": "resolve",
                            "resource": "projects",
                            "field": "aggregate_id",
                        },
                    },
                    "data_selector": "data",
                },
            },
        ],
    }


def run_pipeline(
    jortt_access_token: str = None,
    database_path: str = "jortt.duckdb",
) -> None:
    """Run the Jortt to local DuckDB pipeline.

    Args:
        jortt_access_token: Jortt API access token
        database_path: Path to local DuckDB database file (default: jortt.duckdb)
    """
    # Get the REST API configuration
    config = get_jortt_config(jortt_access_token)

    # Create the REST API source
    source = rest_api_source(config)

    # Create the pipeline with local DuckDB destination
    pipeline = dlt.pipeline(
        pipeline_name="jortt_to_duckdb",
        destination=dlt.destinations.duckdb(database_path),
        dataset_name="raw",  # Schema name within the database
    )

    # Run the pipeline
    load_info = pipeline.run(source)

    # Print the load info
    print("\n✓ Pipeline completed successfully!")
    print(f"Database: {database_path}")
    print("Schema: raw")
    print(f"Loaded {len(load_info.loads_ids)} load(s)")
    print("\nLoad details:")
    print(load_info)
