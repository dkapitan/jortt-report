import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    from jortt_duck.pipeline import run_pipeline
    return (run_pipeline,)


@app.cell
def _(run_pipeline):
    run_pipeline()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
