"""Main entry point for the Jortt to DuckDB pipeline."""

import os
from dotenv import load_dotenv
from .pipeline import run_pipeline
from .auth import fetch_token

# Load environment variables from .env file
load_dotenv()


def main():
    """Run the Jortt to local DuckDB data pipeline."""
    # Get credentials from environment variables
    jortt_access_token = os.getenv("JORTT_ACCESS_TOKEN")

    # If access token is not provided or is placeholder, fetch it using OAuth
    if not jortt_access_token or jortt_access_token == "your_access_token_here":
        print("No access token found. Fetching token using OAuth client credentials...")
        try:
            jortt_access_token = fetch_token()
            print("✓ Successfully obtained access token")
        except Exception as e:
            raise ValueError(
                f"Failed to fetch access token: {e}\n"
                "Please ensure JORTT_CLIENT_ID and JORTT_CLIENT_SECRET are set in .env"
            )

    # Optional: customize database path
    database_path = os.getenv("DATABASE_PATH", "jortt.duckdb")

    print("\nStarting Jortt to DuckDB pipeline...")
    print(f"Target database: {database_path}")
    print("Schema: raw\n")

    # Run the pipeline
    run_pipeline(
        jortt_access_token=jortt_access_token,
        database_path=database_path,
    )

    print("\nPipeline execution completed!")


if __name__ == "__main__":
    main()
