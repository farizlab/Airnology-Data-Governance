import sqlite3
from pathlib import Path

# Menentukan lokasi database
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

# Membuat koneksi ke database
conn = sqlite3.connect(DB_PATH)

print("Database berhasil dibuat:", DB_PATH)

# Menutup koneksi
conn.close()