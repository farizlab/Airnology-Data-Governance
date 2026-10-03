import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "AIRNO'26_SUBMISSION ALL.xlsx"
DB_PATH = BASE_DIR / "database" / "airnology.db"

df = pd.read_excel(FILE_PATH)


def clean_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

submission_count = 0
matched_count = 0
unmatched_count = 0

print("==========================================")
print("IMPORT SUBMISSION")
print("==========================================")

for _, row in df.iterrows():

    timestamp = clean_value(row["Timestamp"])
    email = clean_value(row["Email Address"])
    team_name = clean_value(row["Nama Tim"])
    leader = clean_value(row["Nama Lengkap Ketua"])
    whatsapp = clean_value(row["No. WhatsApp Aktif Ketua"])
    institution = clean_value(row["Asal Instansi"])
    work_file_url = clean_value(row["Pengumpulan Karya"])
    attachment_url = clean_value(row["Pengumpulan Lampiran Karya"])
    declaration = clean_value(row["Pernyataan Kebenaran"])

    # Cari team berdasarkan nama
    cursor.execute("""
        SELECT
            t.team_id,
            t.competition_id,
            c.competition_name
        FROM team t
        JOIN competition c
            ON t.competition_id = c.competition_id
        WHERE LOWER(TRIM(t.team_name)) = LOWER(TRIM(?))
    """, (team_name,))

    result = cursor.fetchone()

    if not result:
        print()
        print("WARNING: Team tidak ditemukan")
        print("Team:", team_name)

        unmatched_count += 1
        continue

    team_id = result[0]
    competition_id = result[1]
    competition_name = result[2]

    matched_count += 1

    # Masukkan submission
    cursor.execute("""
        INSERT INTO submission (
            team_id,
            competition_id,
            submitted_at,
            work_file_url,
            attachment_url,
            requirement_status,
            verification_notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        team_id,
        competition_id,
        timestamp,
        work_file_url,
        attachment_url,
        "Submitted",
        None
    ))

    submission_count += 1

    print(
        f"✓ {team_name} "
        f"| {competition_name}"
    )


conn.commit()
conn.close()

print()
print("==========================================")
print("IMPORT SUBMISSION SELESAI")
print("==========================================")
print(f"Submission baru  : {submission_count}")
print(f"Team matched     : {matched_count}")
print(f"Team tidak cocok : {unmatched_count}")
print(f"Database         : {DB_PATH}")