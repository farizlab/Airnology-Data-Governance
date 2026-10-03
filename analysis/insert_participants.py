import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "Pendaftaran AIRNOLOGY 2026 (Jawaban).xlsx"
DB_PATH = BASE_DIR / "database" / "airnology.db"

df = pd.read_excel(FILE_PATH)


def clean_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value in ["-", "–", "—"]:
        return None

    return value


def normalize_whatsapp(value):
    value = clean_value(value)

    if value is None:
        return None

    # Hilangkan spasi, tanda +, dan tanda -
    value = (
        value
        .replace(" ", "")
        .replace("-", "")
        .replace("+", "")
    )

    # Ubah 08xxxxxxxx menjadi 628xxxxxxxx
    if value.startswith("08"):
        value = "62" + value[1:]

    return value


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# Ambil team yang merupakan latest registration
cursor.execute("""
    SELECT
        r.registration_id,
        r.team_id
    FROM registration r
    WHERE r.is_latest = 1
""")

latest_registrations = cursor.fetchall()


participant_count = 0
team_member_count = 0
skipped_count = 0


for registration_id, team_id in latest_registrations:

    cursor.execute("""
        SELECT team_name
        FROM team
        WHERE team_id = ?
    """, (team_id,))

    team_result = cursor.fetchone()

    if not team_result:
        continue

    team_name = team_result[0]

    # Cari baris Excel berdasarkan nama team
    for _, row in df.iterrows():

        competition = clean_value(row.iloc[3])

        # Tentukan nama team sesuai branching Google Form
        if competition == "Engineering Case Competition (ECC)":
            excel_team_name = clean_value(row.iloc[4])

        elif competition == "Essay Competition":
            excel_team_name = clean_value(row.iloc[16])

        elif competition == "Technology Innovation Competition (TIC)":
            excel_team_name = clean_value(row.iloc[25])

        else:
            continue

        if excel_team_name != team_name:
            continue

        # ==========================================
        # Tentukan data participant
        # ==========================================

        if competition == "Engineering Case Competition (ECC)":

            names = [
                row.iloc[5],
                row.iloc[6],
                row.iloc[7]
            ]

            whatsapp = [
                row.iloc[2],
                row.iloc[47],
                row.iloc[48]
            ]

            institution = row.iloc[8]

            faculty = [
                row.iloc[10],
                row.iloc[11],
                row.iloc[12]
            ]

            study_program = [
                row.iloc[13],
                row.iloc[14],
                row.iloc[15]
            ]

        elif competition == "Essay Competition":

            names = [
                row.iloc[17],
                row.iloc[18],
                row.iloc[19]
            ]

            whatsapp = [
                row.iloc[2],
                row.iloc[50],
                row.iloc[51]
            ]

            institution = row.iloc[20]

            faculty = [
                None,
                None,
                None
            ]

            study_program = [
                None,
                None,
                None
            ]

        else:

            names = [
                row.iloc[26],
                row.iloc[27],
                row.iloc[28]
            ]

            whatsapp = [
                row.iloc[2],
                row.iloc[52],
                row.iloc[53]
            ]

            institution = row.iloc[29]

            faculty = [
                row.iloc[31],
                row.iloc[32],
                row.iloc[33]
            ]

            study_program = [
                row.iloc[34],
                row.iloc[35],
                row.iloc[36]
            ]

        # ==========================================
        # Insert participant
        # ==========================================

        for i in range(3):

            name = clean_value(names[i])

            # Skip kosong / placeholder
            if name is None:
                continue

            # Skip anomaly yang sudah kita identifikasi
            if name == "1" and team_name == "1":
                skipped_count += 1
                continue

            phone = normalize_whatsapp(whatsapp[i])
            inst = clean_value(institution)
            fac = clean_value(faculty[i])
            study = clean_value(study_program[i])

            # Cari participant berdasarkan identitas
            cursor.execute("""
                SELECT participant_id
                FROM participant
                WHERE full_name = ?
                AND (
                    whatsapp = ?
                    OR (
                        whatsapp IS NULL
                        AND ? IS NULL
                        AND institution = ?
                    )
                )
                LIMIT 1
            """, (
                name,
                phone,
                phone,
                inst
            ))

            result = cursor.fetchone()

            if result:
                participant_id = result[0]

            else:

                cursor.execute("""
                    INSERT INTO participant (
                        full_name,
                        email,
                        whatsapp,
                        institution,
                        faculty,
                        study_program
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    name,
                    None,
                    phone,
                    inst,
                    fac,
                    study
                ))

                participant_id = cursor.lastrowid
                participant_count += 1

            # Tentukan role
            if i == 0:
                role = "Ketua"
            else:
                role = "Anggota"

            # Cek apakah relasi sudah ada
            cursor.execute("""
                SELECT team_member_id
                FROM team_member
                WHERE team_id = ?
                AND participant_id = ?
            """, (
                team_id,
                participant_id
            ))

            existing_member = cursor.fetchone()

            if not existing_member:

                cursor.execute("""
                    INSERT INTO team_member (
                        team_id,
                        participant_id,
                        role
                    )
                    VALUES (?, ?, ?)
                """, (
                    team_id,
                    participant_id,
                    role
                ))

                team_member_count += 1

        break


conn.commit()
conn.close()


print("==========================================")
print("IMPORT PARTICIPANT SELESAI")
print("==========================================")
print(f"Participant baru : {participant_count}")
print(f"Team member baru : {team_member_count}")
print(f"Record dilewati  : {skipped_count}")
print(f"Database         : {DB_PATH}")