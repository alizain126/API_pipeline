import requests
import pandas as pd
import os
from datetime import datetime

# only import SQL libraries if available (not on GitHub Actions)
try:
    import pyodbc
    from sqlalchemy import create_engine, text
    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

# ── CONFIG ──────────────────────────────────────────
API_KEY       = "f56245b208d6cd2a3f5e8899"
BASE_CURRENCY = "USD"
CURRENCIES    = ["PKR", "EUR", "GBP", "AED", "SAR", "JPY", "INR", "CAD"]

# ── FETCH FROM API ───────────────────────────────────
def fetch_rates():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
    response = requests.get(url)
    data = response.json()
    fetch_date = datetime.utcnow().date()
    rows = []
    for currency in CURRENCIES:
        rows.append({
            "base_currency":   BASE_CURRENCY,
            "target_currency": currency,
            "rate":            data["conversion_rates"][currency],
            "fetch_date":      fetch_date
        })
    return pd.DataFrame(rows)

# ── INCREMENTAL LOAD ─────────────────────────────────
def load_incremental(df):
    # engine created here, only runs when function is called
    engine = create_engine(
        "mssql+pyodbc://DESKTOP-APM96JF\\MSSQLSERVER2025/ExchangeRatesDB"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
    with engine.connect() as conn:
        existing = pd.read_sql(
            "SELECT DISTINCT fetch_date FROM exchange_rates", conn
        )
        existing_dates = existing["fetch_date"].astype(str).tolist()
        df["fetch_date"] = df["fetch_date"].astype(str)
        new_data = df[~df["fetch_date"].isin(existing_dates)]
        if new_data.empty:
            print("No new data — today's rates already loaded.")
            return
        new_data.to_sql(
            "exchange_rates",
            engine,
            if_exists="append",
            index=False
        )
        print(f"Inserted {len(new_data)} new rows for {new_data['fetch_date'].iloc[0]}")

# ── RUN PIPELINE ─────────────────────────────────────
if __name__ == "__main__":
    print("Fetching rates...")
    df = fetch_rates()
    print(df)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/latest_rates.csv", index=False)
    print("Saved to data/latest_rates.csv")

    if SQL_AVAILABLE:
        print("Loading to database...")
        load_incremental(df)
    else:
        print("SQL skipped — running on GitHub Actions")