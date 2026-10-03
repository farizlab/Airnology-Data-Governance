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


# ==========================================
# 2. BACA DATA
# ==========================================

df = pd.read_excel(FILE_PATH)


# ==========================================
# 3. FUNGSI CEK NILAI
# ==========================================

def clean_value(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    # Placeholder yang bukan data aktual
    if value in ["-", "–", "—"]:
        return None

    return value


# ==========================================
# 4. TENTUKAN KOLOM BERDASARKAN LOMBA
# ==========================================

def get_columns(competition):

    if "Engineering Case" in competition:

        return {
            "team": "Nama Tim",
            "leader": "Nama Lengkap Ketua",
            "member1": "Nama Lengkap Anggota 1",
            "member2": "Nama Lengkap Anggota 2",
            "institution": "Asal Instansi",
            "faculty_leader": "Asal Fakultas Ketua\nContoh: Fakultas Teknologi Maju dan Multidisiplin (FTMM)",
            "faculty_member1": "Asal Fakultas Anggota 1\nContoh: Fakultas Teknologi Maju dan Multidisiplin (FTMM)",
            "faculty_member2": "Fakultas Anggota 2\nContoh: Fakultas Teknologi Maju dan Multidisiplin (FTMM)",
            "study_leader": "Asal Program Studi Ketua\nContoh: S1 - Kedokteran",
            "study_member1": "Asal Program Studi Anggota 1\nContoh: S1 - Kedokteran",
            "study_member2": "Asal Program Studi Anggota 2\nContoh: S1 - Kedokteran",
            "whatsapp_leader": "Nomor WhatsApp Ketua Aktif",
            "whatsapp_member1": "Nomor WhatsApp Anggota 1",
            "whatsapp_member2": "Nomor WhatsApp Anggota 2"
        }

    if "Essay" in competition:

        return {
            "team": "Nama Tim 2",
            "leader": "Nama Lengkap Ketua 2",
            "member1": "Nama Lengkap Anggota 1 2",
            "member2": "Nama Lengkap Anggota 2 2",
            "institution": "Asal Instansi 2",
            "faculty_leader": None,
            "faculty_member1": None,
            "faculty_member2": None,
            "study_leader": None,
            "study_member1": None,
            "study_member2": None,
            "whatsapp_leader": "Nomor WhatsApp Ketua Aktif",
            "whatsapp_member1": "Nomor WhatsApp Anggota 1 2",
            "whatsapp_member2": "Nomor WhatsApp Anggota 2 2"
        }

    if "Technology Innovation" in competition:

        return {
            "team": "Nama Tim 3",
            "leader": "Nama Lengkap Ketua 3",
            "member1": "Nama Lengkap Anggota 1 3",
            "member2": "Nama Lengkap Anggota 2 3",
            "institution": "Asal Instansi 3",
            "faculty_leader": "Asal Fakultas Ketua_x000a_Contoh: Fakultas Teknologi Maju dan Multidisiplin (FTMM) 2",
            "faculty_member1": "Asal Fakultas Anggota 1_x000a_Contoh: Fakultas Teknologi Maju dan Multidisiplin (FTMM) 2",
            "faculty_member2": "Fakultas Anggota 2_x000a_Contoh: Fakultas Teknologi Maju dan Multidisiplin (FTMM) 2",
            "study_leader": "Asal Program Studi Ketua_x000a_Contoh: S1 - Kedokteran 2",
            "study_member1": "Program Studi Anggota 1\nContoh: S1 - Kedokteran",
            "study_member2": "Program Studi Anggota 2\nContoh: S1 - Kedokteran",
            "whatsapp_leader": "Nomor WhatsApp Ketua Aktif",
            "whatsapp_member1": "Nomor WhatsApp Anggota 1 3",
            "whatsapp_member2": "Nomor WhatsApp Anggota 2 3"
        }

    return None


# ==========================================
# 5. BENTUK DATA PESERTA
# ==========================================

participants = []

for _, row in df.iterrows():

    competition = clean_value(
        row["Pilihan Lomba"]
    )

    columns = get_columns(competition)

    if columns is None:
        continue


    team_name = clean_value(
        row[columns["team"]]
    )

    if team_name is None:
        continue


    members = [
        (
            row[columns["leader"]],
            "Ketua",
            columns["faculty_leader"],
            columns["study_leader"],
            columns["whatsapp_leader"]
        ),
        (
            row[columns["member1"]],
            "Anggota",
            columns["faculty_member1"],
            columns["study_member1"],
            columns["whatsapp_member1"]
        ),
        (
            row[columns["member2"]],
            "Anggota",
            columns["faculty_member2"],
            columns["study_member2"],
            columns["whatsapp_member2"]
        )
    ]


    for name, role, faculty_col, study_col, whatsapp_col in members:

        name = clean_value(name)

        if name is None:
            continue


        faculty = None

        if faculty_col is not None:
            faculty = clean_value(
                row[faculty_col]
            )


        study_program = None

        if study_col is not None:
            study_program = clean_value(
                row[study_col]
            )


        whatsapp = clean_value(
            row[whatsapp_col]
        )


        email = None

        if role == "Ketua":
            email = clean_value(
                row["Email Ketua"]
            )


        participants.append({
            "team_name": team_name,
            "competition": competition,
            "full_name": name,
            "role": role,
            "email": email,
            "whatsapp": whatsapp,
            "institution": clean_value(
                row[columns["institution"]]
            ),
            "faculty": faculty,
            "study_program": study_program
        })


# ==========================================
# 6. PREVIEW
# ==========================================

result = pd.DataFrame(participants)


print("==========================================")
print("PREVIEW PARTICIPANT")
print("==========================================")

print(f"Total team       : {result['team_name'].nunique()}")
print(f"Total participant: {len(result)}")


print("\n==========================================")
print("PARTICIPANT PER COMPETITION")
print("==========================================")

print(
    result.groupby("competition")
    .size()
)


print("\n==========================================")
print("CONTOH DATA")
print("==========================================")

print(
    result.head(15).to_string(index=False)
)