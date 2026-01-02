# Querying Jortt Data in MotherDuck

This guide shows how to query your Jortt data that's now in MotherDuck.

## Option 1: Using the MotherDuck Web UI

1. Go to [https://app.motherduck.com/](https://app.motherduck.com/)
2. Navigate to your `jortt` database
3. Browse the `jortt_raw` schema
4. Run SQL queries in the query editor

## Option 2: Using Python/DuckDB

```python
import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MotherDuck
conn = duckdb.connect(f"md:jortt?motherduck_token={os.getenv('MOTHERDUCK_TOKEN')}")

# Query projects
result = conn.execute("""
    SELECT *
    FROM my_db.jortt_raw.projects_resource
    LIMIT 10
""").fetchall()

for row in result:
    print(row)

conn.close()
```

## Example Queries

### Count total projects
```sql
SELECT COUNT(*) as total_projects
FROM my_db.jortt_raw.projects_resource;
```

### List projects with customer names
```sql
SELECT
    reference,
    customer_record__name,
    customer_record__email,
    _dlt_load_id
FROM my_db.jortt_raw.projects_resource
ORDER BY created_at DESC;
```

### Get project totals by currency
```sql
SELECT
    unbilled_total_currency as currency,
    COUNT(*) as project_count,
    SUM(CAST(unbilled_total_value as DECIMAL)) as total_unbilled
FROM my_db.jortt_raw.projects_resource
GROUP BY unbilled_total_currency;
```

### Find projects with specific customers
```sql
SELECT
    reference,
    customer_record__name,
    unbilled_total_value,
    unbilled_total_currency
FROM my_db.jortt_raw.projects_resource
WHERE customer_record__name LIKE '%Health%';
```

### Get the latest load information
```sql
SELECT
    load_id,
    schema_name,
    status,
    inserted_at
FROM my_db.jortt_raw._dlt_loads
ORDER BY inserted_at DESC
LIMIT 5;
```

## Option 3: Using the DuckDB CLI

```bash
# Install duckdb CLI if needed
brew install duckdb

# Connect to MotherDuck
duckdb -c "
  SET home_directory='/Users/yourusername/.duckdb';
  LOAD motherduck;
  ATTACH 'md:jortt?motherduck_token=${MOTHERDUCK_TOKEN}';
  SELECT * FROM my_db.jortt_raw.projects_resource LIMIT 5;
"
```

## Option 4: Using SQL Clients

MotherDuck supports many SQL clients:
- **DataGrip** (JetBrains)
- **DBeaver**
- **TablePlus**
- **Any PostgreSQL-compatible client**

Connection details:
- Host: `motherduck.com`
- Database: `jortt`
- Username: `motherduck`
- Password: `<your_motherduck_token>`

## Understanding the Schema

### Main Table: `projects_resource`

Key columns:
- `id`: Project UUID
- `reference`: Human-readable project reference
- `customer_id`: Customer UUID
- `customer_record__*`: Nested customer fields
- `unbilled_total_value`: Amount unbilled
- `unbilled_total_currency`: Currency code
- `created_at`, `updated_at`: Timestamps
- `_dlt_load_id`: DLT metadata (which pipeline run loaded this)
- `_dlt_id`: DLT unique identifier

### Metadata Tables

- `_dlt_loads`: Track pipeline execution history
- `_dlt_pipeline_state`: DLT pipeline state
- `_dlt_version`: Schema version tracking

## Refreshing Data

To get the latest data from Jortt API:

```bash
uv run python -m jortt_duck
```

This will replace all data with the current state from Jortt (full refresh).

## Exporting Data

### To CSV
```sql
COPY (
    SELECT * FROM my_db.jortt_raw.projects_resource
) TO 'projects.csv' (HEADER, DELIMITER ',');
```

### To Parquet
```sql
COPY (
    SELECT * FROM my_db.jortt_raw.projects_resource
) TO 'projects.parquet' (FORMAT PARQUET);
```

### To local DuckDB file
```python
import duckdb

# Connect to both MotherDuck and local file
conn = duckdb.connect('local.duckdb')
conn.execute(f"""
    ATTACH 'md:jortt?motherduck_token={token}' AS md;
    CREATE TABLE projects AS
    SELECT * FROM md.my_db.jortt_raw.projects_resource;
""")
```

## Tips

1. **Qualify table names**: Always use `my_db.jortt_raw.table_name` for clarity
2. **Check load metadata**: Use `_dlt_loads` table to see when data was last updated
3. **Filter by load**: Use `_dlt_load_id` to compare different loads
4. **Join nested tables**: Use the relationship keys to join nested data structures

## Troubleshooting

If you can't see your data:
1. Check you're connected to the right database: `SELECT current_database();`
2. List available schemas: `SELECT schema_name FROM information_schema.schemata;`
3. Check table exists: `SELECT table_name FROM information_schema.tables WHERE table_schema = 'jortt_raw';`
4. Verify data was loaded: `SELECT COUNT(*) FROM my_db.jortt_raw.projects_resource;`
