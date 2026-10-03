import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("==========================================")
print("STRUKTUR TABEL RANKING")
print("==========================================")

cursor.execute("PRAGMA table_info(ranking)")

for column in cursor.fetchall():
    print(column)

conn.close()