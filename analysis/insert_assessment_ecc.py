import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "Transparansi Penilaian FINAL AIRNOLOGY 2026.xlsx"
DB_PATH = BASE_DIR / "database" / "airnology.db"

df = pd.read_excel(
    FILE_PATH,
    sheet_name="Engineering Case Competition",
    header=None
)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Kolom skor ECC:
# 2 = Kelayakan & Efektivitas Solusi
# 3 = Inovasi & Penerapan Keteknikan
# 4 = Kualitas Visual
# 5 = Kejelasan Artikulasi
# 6 = Ketepatan Waktu
# 7 = Penyampaian Materi
# 8 = Argumentasi Ilmiah
# 9 = Ketepatan Jawaban & Kedalaman Pemahaman
# 10 = Kejelasan Argumentasi & Kerja Sama Tim

criterion_columns = {
    2: "Kelayakan & Efektivitas Solusi",
    3: "Inovasi & Penerapan Keteknikan (Engineering)",
    4: "Kualitas Visual",
    5: "Kejelasan Artikulasi",
    6: "Ketepatan Waktu",
    7: "Penyampaian Materi",
    8: "Argumentasi Ilmiah",
    9: "Ketepatan Jawaban & Kedalaman Pemahaman",
    10: "Kejelasan Argumentasi & Kerja Sama Tim",
}

inserted = 0

for row_index in range(4, len(df)):

    team_name = df.iloc[row_index, 1]

    if pd.isna(team_name):
        continue

    team_name = str(team_name).strip()

    cursor.execute("""
        SELECT s.submission_id
        FROM submission s
        JOIN team t
            ON s.team_id = t.team_id
        WHERE LOWER(TRIM(t.team_name)) = LOWER(TRIM(?))
    """, (team_name,))

    result = cursor.fetchone()

    if not result:
        print("WARNING: Submission tidak ditemukan:", team_name)
        continue

    submission_id = result[0]

    for column_index, criterion_name in criterion_columns.items():

        score = df.iloc[row_index, column_index]

        if pd.isna(score):
            continue

        cursor.execute("""
            SELECT criterion_id
            FROM criterion
            JOIN competition
                ON criterion.competition_id = competition.competition_id
            WHERE competition.competition_code = 'ECC'
            AND criterion.criterion_name = ?
        """, (criterion_name,))

        criterion = cursor.fetchone()

        if not criterion:
            print("WARNING: Criterion tidak ditemukan:", criterion_name)
            continue

        criterion_id = criterion[0]

        cursor.execute("""
            INSERT INTO assessment (
                submission_id,
                judge_id,
                criterion_id,
                score,
                assessed_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            submission_id,
            None,
            criterion_id,
            float(score),
            None
        ))

        inserted += 1

conn.commit()
conn.close()

print("==========================================")
print("IMPORT ASSESSMENT ECC SELESAI")
print("==========================================")
print(f"Assessment baru : {inserted}")