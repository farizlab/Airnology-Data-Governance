import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT
        s.submission_id,
        t.team_name,
        c.competition_name,
        s.submitted_at
    FROM submission s
    JOIN team t
        ON s.team_id = t.team_id
    JOIN competition c
        ON s.competition_id = c.competition_id
    ORDER BY s.submission_id
""")

rows = cursor.fetchall()

print("==========================================")
print("DATA SUBMISSION")
print("==========================================")

for row in rows:
    print(
        f"ID: {row[0]} | "
        f"Team: {row[1]} | "
        f"Competition: {row[2]} | "
        f"Submitted: {row[3]}"
    )

print()
print("Total submission:", len(rows))

conn.close()