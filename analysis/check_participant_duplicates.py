import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "Pendaftaran AIRNOLOGY 2026 (Jawaban).xlsx"

df = pd.read_excel(FILE_PATH)


def clean_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value in ["-", "–", "—"]:
        return None

    return value


records = []

for _, row in df.iterrows():

    competition = clean_value(row.iloc[3])

    if competition == "Engineering Case Competition (ECC)":

        team_name = clean_value(row.iloc[4])

        names = [
            row.iloc[5],
            row.iloc[6],
            row.iloc[7]
        ]

        whatsapp = [
            row.iloc[2],
            row.iloc[47],
            row.iloc[48]
        ]

        institution = row.iloc[8]

        faculty = [
            row.iloc[10],
            row.iloc[11],
            row.iloc[12]
        ]

        study_program = [
            row.iloc[13],
            row.iloc[14],
            row.iloc[15]
        ]

    elif competition == "Essay Competition":

        team_name = clean_value(row.iloc[16])

        names = [
            row.iloc[17],
            row.iloc[18],
            row.iloc[19]
        ]

        whatsapp = [
            row.iloc[2],
            row.iloc[50],
            row.iloc[51]
        ]

        institution = row.iloc[20]

        faculty = [
            None,
            None,
            None
        ]

        study_program = [
            None,
            None,
            None
        ]

    elif competition == "Technology Innovation Competition (TIC)":

        team_name = clean_value(row.iloc[25])

        names = [
            row.iloc[26],
            row.iloc[27],
            row.iloc[28]
        ]

        whatsapp = [
            row.iloc[2],
            row.iloc[52],
            row.iloc[53]
        ]

        institution = row.iloc[29]

        faculty = [
            row.iloc[31],
            row.iloc[32],
            row.iloc[33]
        ]

        study_program = [
            row.iloc[34],
            row.iloc[35],
            row.iloc[36]
        ]

    else:
        continue

    for i in range(3):

        name = clean_value(names[i])

        if name is None:
            continue

        records.append({
            "team_name": team_name,
            "competition": competition,
            "full_name": name,
            "whatsapp": clean_value(whatsapp[i]),
            "institution": clean_value(institution),
            "faculty": clean_value(faculty[i]),
            "study_program": clean_value(study_program[i])
        })


participants = pd.DataFrame(records)


print("==========================================")
print("DETAIL PARTICIPANT DUPLICATES")
print("==========================================")


duplicate_names = (
    participants
    .groupby("full_name")
    .size()
    .reset_index(name="count")
    .query("count > 1")
    .sort_values("count", ascending=False)
)


for name in duplicate_names["full_name"]:

    print()
    print("------------------------------------------")
    print(f"NAMA: {name}")

    result = participants[
        participants["full_name"] == name
    ][
        [
            "team_name",
            "competition",
            "whatsapp",
            "institution"
        ]
    ]

    print(result.to_string(index=False))