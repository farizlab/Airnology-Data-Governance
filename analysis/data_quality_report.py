import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("==========================================")
print("AIRNOLOGY DATA QUALITY REPORT")
print("==========================================")

# 1. Registration
cursor.execute("SELECT COUNT(*) FROM registration")
registration_count = cursor.fetchone()[0]

# 2. Team
cursor.execute("SELECT COUNT(*) FROM team")
team_count = cursor.fetchone()[0]

# 3. Participant
cursor.execute("SELECT COUNT(*) FROM participant")
participant_count = cursor.fetchone()[0]

# 4. Team Member
cursor.execute("SELECT COUNT(*) FROM team_member")
team_member_count = cursor.fetchone()[0]

# 5. Submission
cursor.execute("SELECT COUNT(*) FROM submission")
submission_count = cursor.fetchone()[0]

# 6. Assessment
cursor.execute("SELECT COUNT(*) FROM assessment")
assessment_count = cursor.fetchone()[0]

# 7. Ranking
cursor.execute("SELECT COUNT(*) FROM ranking")
ranking_count = cursor.fetchone()[0]

# 8. Resubmission
cursor.execute("""
    SELECT COUNT(*)
    FROM registration
    WHERE version > 1
""")
resubmission_count = cursor.fetchone()[0]

# 9. Latest registration
cursor.execute("""
    SELECT COUNT(*)
    FROM registration
    WHERE is_latest = 1
""")
latest_count = cursor.fetchone()[0]

print()
print("RECORD COUNT")
print("------------------------------------------")
print("Registration :", registration_count)
print("Team         :", team_count)
print("Participant  :", participant_count)
print("Team Member  :", team_member_count)
print("Submission   :", submission_count)
print("Assessment   :", assessment_count)
print("Ranking      :", ranking_count)

print()
print("REGISTRATION QUALITY")
print("------------------------------------------")
print("Resubmission records :", resubmission_count)
print("Latest registrations :", latest_count)

# 10. Assessment coverage
cursor.execute("""
    SELECT
        COUNT(DISTINCT submission_id)
    FROM assessment
""")
assessed_submissions = cursor.fetchone()[0]

print()
print("ASSESSMENT COVERAGE")
print("------------------------------------------")
print("Submission dinilai :", assessed_submissions)
print("Assessment records :", assessment_count)

conn.close()

print()
print("==========================================")
print("REPORT SELESAI")
print("==========================================")