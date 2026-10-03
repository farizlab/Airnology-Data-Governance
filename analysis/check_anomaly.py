import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "Pendaftaran AIRNOLOGY 2026 (Jawaban).xlsx"

df = pd.read_excel(FILE_PATH)

print("==========================================")
print("CHECK ANOMALOUS PARTICIPANT DATA")
print("==========================================")

# Cari baris yang memiliki nilai nama peserta "1"
for index, row in df.iterrows():

    values = row.astype(str).tolist()

    if "1" in values:
        print()
        print("------------------------------------------")
        print(f"Excel row : {index + 2}")
        print("Competition:", row.iloc[3])
        print("Nama Tim:", row.iloc[4])
        print("Nama Tim 2:", row.iloc[16])
        print("Nama Tim 3:", row.iloc[25])

        print("Ketua:", row.iloc[5])
        print("Ketua 2:", row.iloc[17])
        print("Ketua 3:", row.iloc[26])

        print("Anggota 1:", row.iloc[6])
        print("Anggota 1 2:", row.iloc[18])
        print("Anggota 1 3:", row.iloc[27])

        print("Anggota 2:", row.iloc[7])
        print("Anggota 2 2:", row.iloc[19])
        print("Anggota 2 3:", row.iloc[28])