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
        ROUND(SUM(a.score), 2) AS final_score
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
    GROUP BY s.submission_id, t.team_name
    ORDER BY final_score DESC
""")

rows = cursor.fetchall()

print("==========================================")
print("IMPORT RANKING ECC")
print("==========================================")

for rank, (submission_id, team_name, final_score) in enumerate(rows, start=1):

    result_status = "Participant"

    if rank == 1:
        result_status = "Winner"
    elif rank <= 3:
        result_status = "Finalist"

    cursor.execute("""
        INSERT INTO ranking (
            submission_id,
            final_score,
            rank,
            result_status
        )
        VALUES (?, ?, ?, ?)
    """, (
        submission_id,
        final_score,
        rank,
        result_status
    ))

    print(
        f"{rank}. {team_name} | "
        f"{final_score} | {result_status}"
    )

conn.commit()
conn.close()

print()
print("==========================================")
print("IMPORT RANKING ECC SELESAI")
print("==========================================")
print(f"Ranking baru : {len(rows)}")