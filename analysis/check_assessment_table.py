import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for table in ["judge", "criterion"]:
    print()
    print("==========================================")
    print(f"TABEL {table.upper()}")
    print("==========================================")

    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()

    for column in columns:
        print(column)

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    print(f"\nJumlah data: {len(rows)}")

    for row in rows:
        print(row)

conn.close()