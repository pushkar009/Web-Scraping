import json, pandas as pd, typer, asyncio
from typing import List
from .scraper import scrape

app = typer.Typer()

@app.command()
def fetch(url: List[str], out: str = "results.json", concurrency: int = 5, timeout: int = 10, retries: int = 2):
    results = asyncio.run(scrape(url, concurrency, timeout, retries))
    if out.endswith(".csv"):
        pd.DataFrame(results).to_csv(out, index=False)
    else:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    typer.echo(f"Saved {len(results)} results to {out}")

if __name__ == "__main__":
    app()
