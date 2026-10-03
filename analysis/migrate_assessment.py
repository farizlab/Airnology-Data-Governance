import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE assessment_new (
        assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER NOT NULL,
        judge_id INTEGER,
        criterion_id INTEGER NOT NULL,
        score REAL NOT NULL,
        assessed_at TEXT,
        FOREIGN KEY (submission_id)
            REFERENCES submission(submission_id),
        FOREIGN KEY (judge_id)
            REFERENCES judge(judge_id),
        FOREIGN KEY (criterion_id)
            REFERENCES criterion(criterion_id)
    )
""")

cursor.execute("""
    INSERT INTO assessment_new (
        assessment_id,
        submission_id,
        judge_id,
        criterion_id,
        score,
        assessed_at
    )
    SELECT
        assessment_id,
        submission_id,
        judge_id,
        criterion_id,
        score,
        assessed_at
    FROM assessment
""")

cursor.execute("DROP TABLE assessment")
cursor.execute("ALTER TABLE assessment_new RENAME TO assessment")

conn.commit()
conn.close()

print("==========================================")
print("MIGRATION ASSESSMENT SELESAI")
print("==========================================")
print("judge_id sekarang boleh NULL.")