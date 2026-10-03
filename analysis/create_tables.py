import sqlite3
from pathlib import Path

# Menentukan lokasi database
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "airnology.db"

# Membuka koneksi ke database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ==========================================
# 1. TABEL COMPETITION
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS competition (
    competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_name TEXT NOT NULL,
    competition_code TEXT NOT NULL UNIQUE,
    description TEXT,
    status TEXT
)
""")

# ==========================================
# 2. TABEL PARTICIPANT
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS participant (
    participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT,
    whatsapp TEXT,
    institution TEXT,
    faculty TEXT,
    study_program TEXT
)
""")

# ==========================================
# 3. TABEL TEAM
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS team (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    competition_id INTEGER NOT NULL,
    institution TEXT,
    FOREIGN KEY (competition_id)
        REFERENCES competition(competition_id)
)
""")

# ==========================================
# 4. TABEL TEAM_MEMBER
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS team_member (
    team_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    role TEXT,
    FOREIGN KEY (team_id)
        REFERENCES team(team_id),
    FOREIGN KEY (participant_id)
        REFERENCES participant(participant_id)
)
""")

# ==========================================
# 5. TABEL REGISTRATION
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS registration (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    submitted_at TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    is_latest INTEGER DEFAULT 1,
    supersedes_registration_id INTEGER,
    revision_reason TEXT,
    FOREIGN KEY (team_id)
        REFERENCES team(team_id),
    FOREIGN KEY (supersedes_registration_id)
        REFERENCES registration(registration_id)
)
""")

# ==========================================
# 6. TABEL SUBMISSION
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS submission (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    submitted_at TEXT NOT NULL,
    work_file_url TEXT,
    attachment_url TEXT,
    requirement_status TEXT,
    verification_notes TEXT,
    FOREIGN KEY (team_id)
        REFERENCES team(team_id),
    FOREIGN KEY (competition_id)
        REFERENCES competition(competition_id)
)
""")

# ==========================================
# 7. TABEL JUDGE
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS judge (
    judge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    judge_name TEXT NOT NULL,
    institution TEXT
)
""")

# ==========================================
# 8. TABEL CRITERION
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS criterion (
    criterion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER NOT NULL,
    criterion_name TEXT NOT NULL,
    weight REAL,
    FOREIGN KEY (competition_id)
        REFERENCES competition(competition_id)
)
""")

# ==========================================
# 9. TABEL ASSESSMENT
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS assessment (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER NOT NULL,
    judge_id INTEGER NOT NULL,
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

# ==========================================
# 10. TABEL RANKING
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS ranking (
    ranking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER NOT NULL,
    final_score REAL NOT NULL,
    rank INTEGER,
    result_status TEXT,
    FOREIGN KEY (submission_id)
        REFERENCES submission(submission_id)
)
""")

# Menyimpan perubahan
conn.commit()

# Menutup koneksi
conn.close()

print("Semua tabel berhasil dibuat.")