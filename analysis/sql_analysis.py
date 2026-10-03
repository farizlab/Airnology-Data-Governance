import sqlite3
import pandas as pd

DB_PATH = "database/airnology.db"

conn = sqlite3.connect(DB_PATH)


# ==========================================================
# 1. JUMLAH PESERTA PER KOMPETISI
# ==========================================================

query_1 = """
SELECT
    c.competition_name,
    COUNT(DISTINCT p.participant_id) AS total_participants
FROM participant p
JOIN team_member tm
    ON p.participant_id = tm.participant_id
JOIN team t
    ON tm.team_id = t.team_id
JOIN competition c
    ON t.competition_id = c.competition_id
GROUP BY c.competition_id, c.competition_name
ORDER BY total_participants DESC;
"""

print("\n==========================================")
print("1. PESERTA PER KOMPETISI")
print("==========================================")

df = pd.read_sql_query(query_1, conn)
print(df.to_string(index=False))


# ==========================================================
# 2. JUMLAH TIM PER KOMPETISI
# ==========================================================

query_2 = """
SELECT
    c.competition_name,
    COUNT(t.team_id) AS total_teams
FROM team t
JOIN competition c
    ON t.competition_id = c.competition_id
GROUP BY c.competition_id, c.competition_name
ORDER BY total_teams DESC;
"""

print("\n==========================================")
print("2. TIM PER KOMPETISI")
print("==========================================")

df = pd.read_sql_query(query_2, conn)
print(df.to_string(index=False))


# ==========================================================
# 3. JUMLAH REGISTRASI DAN RESUBMISSION
# ==========================================================

query_3 = """
SELECT
    COUNT(*) AS total_registration,
    SUM(CASE WHEN version > 1 THEN 1 ELSE 0 END) AS resubmission_records,
    COUNT(DISTINCT team_id) AS total_teams
FROM registration;
"""

print("\n==========================================")
print("3. REGISTRASI & RESUBMISSION")
print("==========================================")

df = pd.read_sql_query(query_3, conn)
print(df.to_string(index=False))


# ==========================================================
# 4. TIM DENGAN LEBIH DARI SATU VERSI REGISTRASI
# ==========================================================

query_4 = """
SELECT
    t.team_name,
    COUNT(r.registration_id) AS registration_versions
FROM registration r
JOIN team t
    ON r.team_id = t.team_id
GROUP BY r.team_id, t.team_name
HAVING COUNT(r.registration_id) > 1
ORDER BY registration_versions DESC;
"""

print("\n==========================================")
print("4. TIM DENGAN MULTIPLE REGISTRATION")
print("==========================================")

df = pd.read_sql_query(query_4, conn)
print(df.to_string(index=False))


# ==========================================================
# 5. SUBMISSION YANG SUDAH DINILAI
# ==========================================================

query_5 = """
SELECT
    t.team_name,
    c.competition_name,
    COUNT(a.assessment_id) AS assessment_records
FROM submission s
JOIN team t
    ON s.team_id = t.team_id
JOIN competition c
    ON s.competition_id = c.competition_id
LEFT JOIN assessment a
    ON s.submission_id = a.submission_id
GROUP BY s.submission_id, t.team_name, c.competition_name
ORDER BY assessment_records DESC;
"""

print("\n==========================================")
print("5. ASSESSMENT PER SUBMISSION")
print("==========================================")

df = pd.read_sql_query(query_5, conn)
print(df.to_string(index=False))


# ==========================================================
# 6. RANKING PROTOTYPE
# ==========================================================

query_6 = """
SELECT
    r.rank,
    t.team_name,
    c.competition_name,
    r.final_score,
    r.result_status
FROM ranking r
JOIN submission s
    ON r.submission_id = s.submission_id
JOIN team t
    ON s.team_id = t.team_id
JOIN competition c
    ON s.competition_id = c.competition_id
ORDER BY r.rank;
"""

print("\n==========================================")
print("6. RANKING PROTOTYPE")
print("==========================================")

df = pd.read_sql_query(query_6, conn)
print(df.to_string(index=False))


# ==========================================================
# 7. DATA QUALITY SUMMARY
# ==========================================================

query_7 = """
SELECT
    (SELECT COUNT(*) FROM registration) AS registration,
    (SELECT COUNT(*) FROM team) AS teams,
    (SELECT COUNT(*) FROM participant) AS participants,
    (SELECT COUNT(*) FROM team_member) AS team_members,
    (SELECT COUNT(*) FROM submission) AS submissions,
    (SELECT COUNT(*) FROM assessment) AS assessments,
    (SELECT COUNT(*) FROM ranking) AS rankings;
"""

print("\n==========================================")
print("7. DATABASE SUMMARY")
print("==========================================")

df = pd.read_sql_query(query_7, conn)
print(df.to_string(index=False))


conn.close()

print("\n==========================================")
print("SQL ANALYSIS SELESAI")
print("==========================================")