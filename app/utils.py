import os
import shutil
import pandas as pd
from datetime import datetime

DATA_FILE = "data/transactions.csv"

def save_csv(df):
    os.makedirs("data", exist_ok=True)
    if not df.empty and "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df.to_csv(DATA_FILE, index=False)

def backup_csv():
    if os.path.exists(DATA_FILE):
        backup_dir = "data/backups"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(DATA_FILE, os.path.join(backup_dir, f"transactions_{timestamp}.csv"))