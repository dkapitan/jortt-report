# Project Summary: Jortt to DuckDB Pipeline

## What Was Built

A complete Python data pipeline that:
1. Authenticates with the Jortt API using OAuth 2.0 Client Credentials
2. Extracts project data from the Jortt API with automatic pagination
3. Loads the data into DuckDB using dlt

## Key Features

### ✓ OAuth 2.0 Authentication
- Automatic token fetching using client credentials
- Standalone auth script for testing (`python -m jortt_duck.auth`)
- Supports all Jortt API scopes

### ✓ Data Extraction
- RESTful API client with pagination support
- Handles Jortt API response structures
- Error handling and retry logic

### ✓ Data Loading
- Loads data to DuckDB using dlt
- Automatic database and schema creation
- Maintains data lineage with dlt metadata tables
- Replace write disposition for full refreshes

## Project Structure

```
jortt-duck/
├── src/jortt_duck/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # CLI entry point
│   ├── auth.py              # OAuth 2.0 authentication
│   └── pipeline.py          # dlt pipeline definition
├── .env                     # Credentials (not in git)
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Project configuration
└── README.md               # Full documentation
```

## Successfully Tested

✅ OAuth token generation (2-hour expiry tokens)
✅ API connection to Jortt
✅ MotherDuck connection and database creation
✅ Data extraction from `/projects` endpoint
✅ Data loading to MotherDuck
✅ 3 project records successfully ingested

## Data Location

- **Database**: `jortt` (or custom via `DATABASE_NAME` env var)
- **Schema**: `jortt_raw`
- **Main Table**: `my_db.jortt_raw.projects_resource`
- **Access**: Via MotherDuck web UI or SQL client

## Quick Start

1. Set credentials in `.env`:
   ```bash
   JORTT_CLIENT_ID=your_id
   JORTT_CLIENT_SECRET=your_secret
   ```

2. Run pipeline:
   ```bash
   uv run python -m jortt_duck
   ```

## Next Steps / Extensibility

The pipeline can be easily extended to ingest other Jortt API resources:

- **Invoices**: `/invoices` endpoint
- **Customers**: `/customers` endpoint
- **Invoice line items**: `/projects/{id}/line_items`
- **Organizations**: `/organizations` endpoint
- **Reports**: Various reporting endpoints

Simply add new methods to `jortt_api.py` and new resources to `pipeline.py` following the existing patterns.

## Technologies Used

- **Python 3.13**
- **dlt**: Data loading framework
- **DuckDB**: Embedded analytics database
- **uv**: Fast Python package manager
- **requests**: HTTP client
- **python-dotenv**: Environment management

## Notes

- Access tokens expire after 2 hours (7200 seconds)
- The pipeline automatically fetches new tokens when needed
- Data is loaded with "replace" disposition (full refresh each run)
- Pagination automatically handles large datasets
