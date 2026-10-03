import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "database/airnology.db"


# 1. Koneksi ke database
conn = sqlite3.connect(DB_PATH)


# 2. Jumlah peserta berdasarkan kompetisi
query = """
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

df_participants = pd.read_sql_query(query, conn)

plt.figure(figsize=(8, 5))
plt.bar(
    df_participants["competition_name"],
    df_participants["total_participants"]
)
plt.title("Participants by Competition")
plt.xlabel("Competition")
plt.ylabel("Number of Participants")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# 3. Jumlah tim berdasarkan kompetisi
query = """
SELECT
    c.competition_name,
    COUNT(t.team_id) AS total_teams
FROM team t
JOIN competition c
    ON t.competition_id = c.competition_id
GROUP BY c.competition_id, c.competition_name
ORDER BY total_teams DESC;
"""

df_teams = pd.read_sql_query(query, conn)

plt.figure(figsize=(8, 5))
plt.bar(
    df_teams["competition_name"],
    df_teams["total_teams"]
)
plt.title("Teams by Competition")
plt.xlabel("Competition")
plt.ylabel("Number of Teams")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# 4. Jumlah submission berdasarkan kompetisi
query = """
SELECT
    c.competition_name,
    COUNT(s.submission_id) AS total_submissions
FROM submission s
JOIN competition c
    ON s.competition_id = c.competition_id
GROUP BY c.competition_id, c.competition_name
ORDER BY total_submissions DESC;
"""

df_submissions = pd.read_sql_query(query, conn)

plt.figure(figsize=(8, 5))
plt.bar(
    df_submissions["competition_name"],
    df_submissions["total_submissions"]
)
plt.title("Submissions by Competition")
plt.xlabel("Competition")
plt.ylabel("Number of Submissions")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()


# 5. Tutup koneksi
conn.close()

print("Visualisasi selesai.")