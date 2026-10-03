import sqlite3
import pandas as pd
from pathlib import Path


# ==========================================
# 1. PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "Pendaftaran AIRNOLOGY 2026 (Jawaban).xlsx"
)

DB_PATH = BASE_DIR / "database" / "airnology.db"


# ==========================================
# 2. BACA DATA EXCEL
# ==========================================

df = pd.read_excel(FILE_PATH)


# ==========================================
# 3. TENTUKAN NAMA TIM SESUAI CABANG LOMBA
# ==========================================

df["team_name_clean"] = df["Nama Tim"].astype(object)

df.loc[
    df["Pilihan Lomba"] == "Essay Competition",
    "team_name_clean"
] = df.loc[
    df["Pilihan Lomba"] == "Essay Competition",
    "Nama Tim 2"
].astype(object)

df.loc[
    df["Pilihan Lomba"] == "Technology Innovation Competition (TIC)",
    "team_name_clean"
] = df.loc[
    df["Pilihan Lomba"] == "Technology Innovation Competition (TIC)",
    "Nama Tim 3"
].astype(object)


# ==========================================
# 4. BERSIHKAN NAMA TIM
# ==========================================

df["team_name_clean"] = (
    df["team_name_clean"]
    .where(df["team_name_clean"].notna(), None)
)

df["team_name_clean"] = df["team_name_clean"].apply(
    lambda x: x.strip() if isinstance(x, str) else x
)


# ==========================================
# 5. URUTKAN BERDASARKAN TIM + TIMESTAMP
# ==========================================

df = df.sort_values(
    ["team_name_clean", "Timestamp"]
).reset_index(drop=True)


# ==========================================
# 6. VERSIONING
# ==========================================

df["version"] = (
    df.groupby("team_name_clean")
    .cumcount() + 1
)

df["is_latest"] = (
    df.groupby("team_name_clean")["Timestamp"]
    .transform("max")
    == df["Timestamp"]
).astype(int)


# ==========================================
# 7. CONNECT DATABASE
# ==========================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ==========================================
# 8. AMBIL COMPETITION DARI DATABASE
# ==========================================

cursor.execute(
    """
    SELECT competition_id, competition_code
    FROM competition
    """
)

competition_rows = cursor.fetchall()

competition_map = {
    code: competition_id
    for competition_id, code in competition_rows
}


# ==========================================
# 9. FUNGSI MENENTUKAN COMPETITION
# ==========================================

def get_competition_code(value):

    if "Engineering Case" in value:
        return "ECC"

    if "Technology Innovation" in value:
        return "TIC"

    if "Essay" in value:
        return "ESSAY"

    return None


# ==========================================
# 10. IMPORT
# ==========================================

registration_count = 0
team_count = 0


for _, row in df.iterrows():

    team_name = row["team_name_clean"]

    # Lewati data tanpa nama tim
    if pd.isna(team_name):
        continue

    team_name = str(team_name).strip()

    competition_code = get_competition_code(
        row["Pilihan Lomba"]
    )

    if competition_code is None:
        print(
            "WARNING: Competition tidak dikenali:",
            row["Pilihan Lomba"]
        )
        continue

    competition_id = competition_map.get(
        competition_code
    )

    if competition_id is None:
        print(
            "WARNING: Competition code tidak ditemukan:",
            competition_code
        )
        continue


    # ======================================
    # CARI / BUAT TEAM
    # ======================================

    cursor.execute(
        """
        SELECT team_id
        FROM team
        WHERE team_name = ?
        AND competition_id = ?
        """,
        (
            team_name,
            competition_id
        )
    )

    result = cursor.fetchone()


    if result:

        team_id = result[0]

    else:

        cursor.execute(
            """
            INSERT INTO team (
                team_name,
                competition_id
            )
            VALUES (?, ?)
            """,
            (
                team_name,
                competition_id
            )
        )

        team_id = cursor.lastrowid
        team_count += 1


    # ======================================
    # TIMESTAMP
    # ======================================

    submitted_at = str(
        row["Timestamp"]
    )


    # ======================================
    # VERSION
    # ======================================

    version = int(
        row["version"]
    )

    is_latest = int(
        row["is_latest"]
    )


    # ======================================
    # SUPERSEDES
    # ======================================

    supersedes_registration_id = None

    if version > 1:

        cursor.execute(
            """
            SELECT registration_id
            FROM registration
            WHERE team_id = ?
            ORDER BY version DESC
            LIMIT 1
            """,
            (team_id,)
        )

        previous = cursor.fetchone()

        if previous:
            supersedes_registration_id = previous[0]


    # ======================================
    # REVISION REASON
    # ======================================

    revision_reason = None

    if version > 1:

        revision_reason = (
            "Resubmission / correction "
            "of previous registration"
        )


    # ======================================
    # INSERT REGISTRATION
    # ======================================

    cursor.execute(
        """
        INSERT INTO registration (
            team_id,
            submitted_at,
            version,
            is_latest,
            supersedes_registration_id,
            revision_reason
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            team_id,
            submitted_at,
            version,
            is_latest,
            supersedes_registration_id,
            revision_reason
        )
    )

    registration_count += 1


# ==========================================
# 11. SIMPAN
# ==========================================

conn.commit()
conn.close()


# ==========================================
# 12. HASIL
# ==========================================

print("==========================================")
print("IMPORT REGISTRASI SELESAI")
print("==========================================")

print(f"Team baru       : {team_count}")
print(f"Registration    : {registration_count}")
print(f"Database        : {DB_PATH}")