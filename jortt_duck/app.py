import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
    import os
    from pathlib import Path
    import subprocess

    import duckdb
    from great_tables import loc, style
    import polars as pl
    import polars.selectors as cs

    project_root = Path(__file__).parent.parent
    default_db_path = project_root / "jortt.duckdb"
    database_path = os.getenv("DATABASE_PATH", str(default_db_path))
    return cs, database_path, loc, pl, project_root, style, subprocess


@app.cell(hide_code=True)
def _(database_path, mo):
    timesheet = mo.sql(
        f"""
        ATTACH '{database_path}' AS jortt (READ_ONLY);

        SELECT
            p.customer_record__customer_name AS customer,
            p.name AS project_name,
            i.date AS time_registration_date,
            i.quantity AS time_registration_quantity,
            i.description AS time_registration_description,
            i.created_at,
            i.updated_at
        FROM
            jortt.raw.project_line_items AS i
            LEFT JOIN jortt.raw.projects AS p ON p.aggregate_id = i.project_id
        ORDER BY
            time_registration_date,
            customer
        """
    )
    return (timesheet,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Jortt Timesheet Dashboard

    ## Pipeline Control
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    run_button = mo.ui.run_button(label="Run Pipeline")
    mo.md(f"Click to fetch latest data from Jortt API: {run_button}")
    return (run_button,)


@app.cell(hide_code=True)
def _(project_root, run_button, subprocess):
    if run_button.value:
        # Run the pipeline using subprocess
        result = subprocess.run(
            ["uv", "run", "python", "-m", "jortt_duck"], cwd=project_root, capture_output=True, text=True
        )

        pipeline_output = result.stdout if result.returncode == 0 else result.stderr
        pipeline_status = "✓ Success" if result.returncode == 0 else "✗ Failed"
    else:
        pipeline_output = "Pipeline not run yet"
        pipeline_status = "Waiting"
    return pipeline_output, pipeline_status


@app.cell(hide_code=True)
def _(mo, pipeline_output, pipeline_status):
    mo.md(f"""
    **Status:** {pipeline_status}

    <details>
    <summary>Pipeline Output</summary>

    ```
    {pipeline_output}
    ```
    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Weekly report
    """)
    return


@app.cell
def _(timesheet):
    timesheet
    return


@app.cell
def _(cs, loc, pl, style, timesheet):
    def weekly_report(df: pl.DataFrame) -> pl.DataFrame:
        pivot = (
            df.select(
                pl.concat_str(
                    [pl.col("customer").fill_null(pl.lit("Intern")), pl.col("project_name")], separator=" | "
                ).alias("project"),
                cs.date(),
                cs.numeric(),
            )
            .pivot(
                index="project",
                on="time_registration_date",
                values="time_registration_quantity",
                aggregate_function="sum",
            )
            .with_columns(pl.sum_horizontal(cs.float()).alias("TOTAL"))
        )
        return (
            pl.concat([pivot.sum().fill_null("TOTAL PER DAY"), pivot])
            .style.tab_header(title="Weekly report")
            .tab_style(
                style=style.text(weight="bold"),
                locations=[loc.header(), loc.body(rows=pl.col("project") == pl.lit("TOTAL PER DAY")), loc.column_header()],
            )
            .tab_stub(rowname_col="project")
        )


    weekly_report(timesheet)
    return


if __name__ == "__main__":
    app.run()
