import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        ATTACH 'jortt.duckdb' AS jortt (READ_ONLY);
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        show tables from jortt;
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select
            p.customer_record__customer_name as customer,
            p.name as project_name,
            i.date as time_registration_date,
            i.quantity as time_registration_quantity,
            i.description as time_registration_description,
            i.created_at,
            i.updated_at
        from jortt.raw.project_line_items as i
        left join jortt.raw.projects as p on p.aggregate_id = i.project_id
        order by
            time_registration_date,
            customer
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""

        """
    )
    return


if __name__ == "__main__":
    app.run()
