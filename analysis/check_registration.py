import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ==========================================
# 1. JUMLAH DATA
# ==========================================

cursor.execute(
    "SELECT COUNT(*) FROM team"
)

total_team = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM registration"
)

total_registration = cursor.fetchone()[0]


print("==========================================")
print("DATABASE VALIDATION")
print("==========================================")

print(f"Total team          : {total_team}")
print(f"Total registration  : {total_registration}")


# ==========================================
# 2. CEK REGISTRASI TERBARU
# ==========================================

print("\n==========================================")
print("REGISTRATION TERBARU")
print("==========================================")

cursor.execute(
    """
    SELECT
        r.registration_id,
        t.team_name,
        r.version,
        r.is_latest,
        r.supersedes_registration_id
    FROM registration r
    JOIN team t
        ON r.team_id = t.team_id
    ORDER BY r.registration_id
    LIMIT 10
    """
)

for row in cursor.fetchall():

    print(
        f"ID: {row[0]} | "
        f"Team: {row[1]} | "
        f"Version: {row[2]} | "
        f"Latest: {row[3]} | "
        f"Supersedes: {row[4]}"
    )


# ==========================================
# 3. CEK TIM YANG MEMILIKI RESUBMISSION
# ==========================================

print("\n==========================================")
print("TIM DENGAN RESUBMISSION")
print("==========================================")

cursor.execute(
    """
    SELECT
        t.team_name,
        COUNT(r.registration_id) AS total_version
    FROM team t
    JOIN registration r
        ON t.team_id = r.team_id
    GROUP BY t.team_id
    HAVING COUNT(r.registration_id) > 1
    ORDER BY t.team_name
    """
)

rows = cursor.fetchall()

for row in rows:

    print(
        f"{row[0]} -> "
        f"{row[1]} versions"
    )


print("\n==========================================")
print(f"Total tim dengan resubmission: {len(rows)}")
print("==========================================")


conn.close()