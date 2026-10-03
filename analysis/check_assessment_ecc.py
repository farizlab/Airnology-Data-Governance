import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT
        t.team_name,
        COUNT(a.assessment_id) AS jumlah_kriteria,
        ROUND(SUM(a.score), 2) AS total_score
    FROM assessment a
    JOIN submission s
        ON a.submission_id = s.submission_id
    JOIN team t
        ON s.team_id = t.team_id
    JOIN criterion c
        ON a.criterion_id = c.criterion_id
    JOIN competition comp
        ON c.competition_id = comp.competition_id
    WHERE comp.competition_code = 'ECC'
    GROUP BY t.team_name
    ORDER BY t.team_name
""")

rows = cursor.fetchall()

print("==========================================")
print("VALIDASI ASSESSMENT ECC")
print("==========================================")

for team_name, count, total in rows:
    print(
        f"{team_name} | "
        f"{count} kriteria | "
        f"Total skor: {total}"
    )

print()
print("Total assessment:", sum(row[1] for row in rows))

conn.close()