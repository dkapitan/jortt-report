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
        select *
        from jortt.raw.project_line_items
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select *
        from jortt.raw.projects
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
