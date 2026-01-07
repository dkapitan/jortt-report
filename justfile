default:
    just --list

# ingest data from jortt API (full load)
load:
    uv run python -m jortt_duck

# analyze data in marimo notebook
report:
    uv run marimo edit notebook.py

# analyze using DuckDB CLI
duck:
    duckdb jortt.duckdb