# Jortt to DuckDB Data Pipeline

A Python project that ingests data from the [Jortt API](https://developer.jortt.nl/) into a local DuckDB database using [dlt (data load tool)](https://dlthub.com/) with declarative REST API configuration.

## Features

- **Declarative REST API Configuration**: Uses dlt's built-in REST API source with minimal custom code
- **OAuth 2.0 Authentication**: Secure authentication with the Jortt API using access tokens
- **Multiple Resources**: Ingests projects and project line items from Jortt API
- **Local DuckDB Storage**: Stores data in a local DuckDB database file
- **Automatic Pagination**: Built-in pagination handling by dlt
- **Type-Safe**: Built with modern Python practices

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Jortt API credentials (OAuth client ID and secret)

## Setup

### 1. Clone or navigate to the project directory

```bash
cd jortt-duck
```

### 2. Install dependencies

The project uses `uv` for dependency management:

```bash
uv sync
```

### 3. Configure environment variables

Edit your [.env](.env) file and add your credentials:

```env
# Jortt API Configuration (OAuth Client Credentials)
JORTT_CLIENT_ID=your_client_id_here
JORTT_CLIENT_SECRET=your_client_secret_here
JORTT_SCOPES=invoices:read invoices:write

# Optional: manually provide access token (will be fetched automatically if not provided)
# JORTT_ACCESS_TOKEN=your_access_token_here

# Optional: customize database path (default: jortt.duckdb)
DATABASE_PATH=jortt.duckdb
```

#### Getting Jortt API Credentials

1. Visit the [Jortt Developer Portal](https://developer.jortt.nl/)
2. Register your application to get your **Client ID** and **Client Secret**
3. Add them to your `.env` file
4. The pipeline will automatically fetch access tokens using the **Client Credentials Grant** flow
5. Common scopes: `invoices:read`, `invoices:write`, `customers:read`, `customers:write`

## Usage

### Get an Access Token (Optional)

If you want to manually fetch an access token to test your credentials:

```bash
uv run python -m jortt_duck.auth
```

This will display your access token and token details. However, the pipeline will automatically fetch tokens when needed.

### Run the pipeline

```bash
uv run python -m jortt_duck
```

The pipeline will:
1. Automatically fetch an access token using your client credentials if needed
2. Extract projects and project line items from the Jortt API with automatic pagination
3. Load the data into a local DuckDB database file (`jortt.duckdb` by default)
4. Store tables in the `raw` schema

### Query the data

After running the pipeline, you can query the data using DuckDB:

```bash
# Open the DuckDB CLI
duckdb jortt.duckdb

# Or use Python
python
>>> import duckdb
>>> conn = duckdb.connect('jortt.duckdb')
>>> conn.execute("SELECT * FROM raw.projects LIMIT 5").fetchdf()
>>> conn.execute("SELECT * FROM raw.project_line_items LIMIT 5").fetchdf()
```

### Project Structure

```
jortt-duck/
├── src/
│   └── jortt_duck/
│       ├── __init__.py
│       ├── __main__.py       # Main entry point
│       ├── auth.py           # OAuth authentication helper
│       └── pipeline.py       # DLT pipeline with REST API config
├── .env                      # Environment variables
├── .gitignore
├── pyproject.toml            # Project configuration
└── README.md
```

## How It Works

1. **OAuth Authentication**: The pipeline uses your Client ID and Secret to obtain an access token via OAuth 2.0 Client Credentials Grant
2. **Declarative Configuration**: The REST API source is configured using a simple dictionary structure with endpoints, authentication, and pagination settings
3. **Data Extraction**: dlt's built-in REST API source handles all API calls and pagination automatically
4. **Data Loading**: DLT loads the data into a local DuckDB file using the `replace` write disposition
5. **Result**: Your Jortt data is now available in DuckDB for analysis

### Authentication Flow

The project supports two authentication methods:

1. **Automatic (Recommended)**: Provide `JORTT_CLIENT_ID` and `JORTT_CLIENT_SECRET` in your `.env` file. The pipeline will automatically fetch access tokens as needed.

2. **Manual**: Fetch an access token manually and provide it as `JORTT_ACCESS_TOKEN` in your `.env` file.

## Data Model

The pipeline creates the following tables in the local DuckDB file (in the `raw` schema):

- **projects**: Main table containing project data from the Jortt API
- **project_line_items**: Table containing project line item data
- **_dlt_loads**: DLT metadata table tracking load operations
- **_dlt_pipeline_state**: DLT state management table
- **_dlt_version**: DLT version information

Additional nested tables may be created automatically by dlt for nested JSON structures (e.g., `projects__customer_record__cc_emails`).

Tables are accessible as `raw.projects` and `raw.project_line_items` within the DuckDB database.

## Extending the Pipeline

To add more resources from the Jortt API, simply add them to the `resources` list in the configuration in [pipeline.py](src/jortt_duck/pipeline.py):

```python
"resources": [
    {
        "name": "projects",
        "endpoint": {
            "path": "projects",
            "params": {
                "per_page": 100,
            },
        },
    },
    {
        "name": "project_line_items",
        "endpoint": {
            "path": "project_line_items",
            "params": {
                "per_page": 100,
            },
        },
    },
    # Add new resources here
    {
        "name": "invoices",
        "endpoint": {
            "path": "invoices",
            "params": {
                "per_page": 100,
            },
        },
    },
]
```

That's it! No custom Python code needed. The dlt REST API source handles everything automatically.

## Dependencies

- **dlt[duckdb]**: Data loading framework with DuckDB support
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API calls

## License

MIT

## Resources

- [Jortt API Documentation](https://developer.jortt.nl/)
- [DLT Documentation](https://dlthub.com/docs)
- [DLT REST API Source Documentation](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic)
- [DuckDB Documentation](https://duckdb.org/docs/)
