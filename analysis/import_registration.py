import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "Pendaftaran AIRNOLOGY 2026 (Jawaban).xlsx"

df = pd.read_excel(FILE_PATH)

# Menentukan nama tim sesuai cabang lomba
df["team_name_clean"] = df["Nama Tim"].astype("object")

df.loc[
    df["Pilihan Lomba"] == "Essay Competition",
    "team_name_clean"
] = df.loc[
    df["Pilihan Lomba"] == "Essay Competition",
    "Nama Tim 2"
].astype("object")

df.loc[
    df["Pilihan Lomba"] == "Technology Innovation Competition (TIC)",
    "team_name_clean"
] = df.loc[
    df["Pilihan Lomba"] == "Technology Innovation Competition (TIC)",
    "Nama Tim 3"
].astype("object"
)


# Urutkan berdasarkan waktu pengisian
df = df.sort_values("Timestamp").reset_index(drop=True)

# Membuat version berdasarkan tim
df["version"] = (
    df.groupby("team_name_clean")
    .cumcount() + 1
)

# Record terakhir dari setiap tim menjadi latest
df["is_latest"] = (
    df.groupby("team_name_clean")["Timestamp"]
    .transform("max")
    == df["Timestamp"]
).astype(int)

# Menentukan ID sementara berdasarkan urutan data
df["registration_temp_id"] = range(1, len(df) + 1)

# Menentukan registration yang digantikan
df["supersedes_registration_id"] = None

for team in df["team_name_clean"].dropna().unique():

    rows = df[df["team_name_clean"] == team].sort_values("Timestamp")

    previous_id = None

    for index in rows.index:

        df.loc[index, "supersedes_registration_id"] = previous_id

        previous_id = df.loc[
            index,
            "registration_temp_id"
        ]


# Menentukan alasan revisi
df["revision_reason"] = None

df.loc[
    df["version"] > 1,
    "revision_reason"
] = "Resubmission / correction of previous registration"


# Tampilkan hasil versioning
print("=== HASIL VERSIONING REGISTRASI ===")

for team in df["team_name_clean"].dropna().unique():

    rows = df[
        df["team_name_clean"] == team
    ].sort_values("Timestamp")

    if len(rows) > 1:

        print(f"\n{'=' * 60}")
        print(f"TIM: {team}")
        print(f"{'=' * 60}")

        for _, row in rows.iterrows():

            print(
                f"Registration ID : {row['registration_temp_id']}\n"
                f"Timestamp       : {row['Timestamp']}\n"
                f"Version         : {row['version']}\n"
                f"Is Latest       : {row['is_latest']}\n"
                f"Supersedes      : {row['supersedes_registration_id']}\n"
                f"Reason          : {row['revision_reason']}\n"
            )