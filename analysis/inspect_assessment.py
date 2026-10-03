import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "raw" / "Transparansi Penilaian FINAL AIRNOLOGY 2026.xlsx"

excel = pd.ExcelFile(FILE_PATH)

for sheet in excel.sheet_names:
    df = pd.read_excel(
        FILE_PATH,
        sheet_name=sheet,
        header=None
    )

    print()
    print("==========================================")
    print(sheet)
    print("==========================================")

    print(df.to_string(index=True, header=False))