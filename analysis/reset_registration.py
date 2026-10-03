import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Hapus data hasil import sebelumnya
cursor.execute("DELETE FROM registration")
cursor.execute("DELETE FROM team")

conn.commit()
conn.close()

print("==========================================")
print("RESET REGISTRATION BERHASIL")
print("==========================================")
print("Tabel registration : kosong")
print("Tabel team         : kosong")
print("Tabel competition  : tetap dipertahankan")