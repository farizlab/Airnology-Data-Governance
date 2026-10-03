import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

criteria = {
    "TIC": [
        ("Kualitas Visual", 8),
        ("Kejelasan Artikulasi", 8),
        ("Ketepatan Waktu", 9),
        ("Penyampaian Materi", 15),
        ("Argumentasi Ilmiah", 15),
        ("Ketepatan Jawaban", 12),
        ("Kedalaman Pemahaman", 12),
        ("Kontribusi Seluruh Anggota Tim", 11),
        ("Jumlah Likes pada Akun Airnology", 10),
    ],

    "ECC": [
        ("Kelayakan & Efektivitas Solusi", 15),
        ("Inovasi & Penerapan Keteknikan (Engineering)", 15),
        ("Kualitas Visual", 7),
        ("Kejelasan Artikulasi", 7),
        ("Ketepatan Waktu", 6),
        ("Penyampaian Materi", 10),
        ("Argumentasi Ilmiah", 10),
        ("Ketepatan Jawaban & Kedalaman Pemahaman", 15),
        ("Kejelasan Argumentasi & Kerja Sama Tim", 15),
    ],

    "ESSAY": [
        ("Akurasi Penyampaian Isi Esai", 15),
        ("Kemampuan Menjawab Pertanyaan", 15),
        ("Kebaruan Gagasan (Novelty)", 13),
        ("Kedalaman Solusi", 13),
        ("Kebermanfaatan Solusi", 14),
        ("Kualitas Visual", 7),
        ("Kejelasan Artikulasi", 8),
        ("Ketepatan Waktu", 6),
        ("Kejelasan Penyampaian", 5),
        ("Sikap Presenter", 4),
    ],
}

cursor.execute(
    "SELECT competition_id, competition_code FROM competition"
)

competition_map = {
    code: competition_id
    for competition_id, code in cursor.fetchall()
}

inserted = 0

for competition_code, criterion_list in criteria.items():

    competition_id = competition_map.get(competition_code)

    if competition_id is None:
        print(
            "WARNING: Competition tidak ditemukan:",
            competition_code
        )
        continue

    for criterion_name, weight in criterion_list:

        cursor.execute(
            """
            INSERT INTO criterion (
                competition_id,
                criterion_name,
                weight
            )
            VALUES (?, ?, ?)
            """,
            (
                competition_id,
                criterion_name,
                weight
            )
        )

        inserted += 1

conn.commit()
conn.close()

print("==========================================")
print("IMPORT CRITERIA SELESAI")
print("==========================================")
print(f"Criterion baru : {inserted}")