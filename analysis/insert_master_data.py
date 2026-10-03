import sqlite3
from pathlib import Path

# Menentukan lokasi database
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

# Membuka koneksi ke database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================================
# DATA MASTER KOMPETISI
# ==========================================
competitions = [
    (
        "Engineering Case Competition",
        "ECC",
        "Kompetisi penyelesaian kasus di bidang engineering dan teknologi.",
        "completed"
    ),
    (
        "Technology Innovation Competition",
        "TIC",
        "Kompetisi inovasi teknologi dan perancangan solusi.",
        "completed"
    ),
    (
        "Essay Competition",
        "ESSAY",
        "Kompetisi penulisan gagasan dan inovasi.",
        "completed"
    )
]

# Memasukkan data ke tabel competition
cursor.executemany("""
    INSERT OR IGNORE INTO competition
    (competition_name, competition_code, description, status)
    VALUES (?, ?, ?, ?)
""", competitions)

# Menyimpan perubahan
conn.commit()

# Mengecek data yang sudah masuk
cursor.execute("""
    SELECT competition_id, competition_name, competition_code
    FROM competition
""")

rows = cursor.fetchall()

print("Data kompetisi:")
for row in rows:
    print(row)

# Menutup koneksi
conn.close()