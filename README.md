# Exchange Rates API Pipeline

A Python pipeline that fetches live currency exchange rates from a free 
API and stores them incrementally in a SQL Server database. 
Runs automatically every day via GitHub Actions.

## What This Project Does
Fetches daily USD exchange rates against PKR, EUR, GBP, AED, SAR, 
JPY, INR and CAD — stores each rate with its date so historical 
trends can be tracked over time.

## What is Incremental Loading?
Incremental loading means only inserting NEW records that don't already 
exist in the database. If today's rates are already loaded and the 
pipeline runs again, it skips instead of inserting duplicates.
This is the standard approach in real data pipelines to avoid 
redundant data and unnecessary processing.

## How It Works
1. `fetch_rates()` — calls ExchangeRate API and returns a pandas DataFrame
2. `load_incremental()` — checks existing dates in SQL Server, 
   inserts only dates not already present
3. GitHub Actions runs this automatically every day at midnight UTC
4. Results also saved to `data/latest_rates.csv` for cloud runs

## How to Run Locally
 pip install -r requirements.txt
 python src/pipeline.py

## Automated Scheduling
GitHub Actions workflow in `.github/workflows/daily_fetch.yml` 
triggers the pipeline daily at midnight UTC without any manual effort.

## Tech Stack
- Python
- Requests
- Pandas
- SQLAlchemy
- SQL Server (local)
- GitHub Actions (scheduling)