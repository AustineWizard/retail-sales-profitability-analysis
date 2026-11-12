import pandas as pd
import os

file_path = r"C:\Users\austi\Desktop\retail-sales-profitability-analysis\data\Global_Superstore2.xlsx"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Dataset not found: {file_path}")

excel = pd.ExcelFile(file_path, engine="openpyxl")

print("AVAILABLE SHEETS:")
print(excel.sheet_names)

df = pd.read_excel(file_path, sheet_name=excel.sheet_names[0])

print("\n--- DATASET DIMENSIONS ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- FIRST FIVE RECORDS ---")
print(df.head())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE RECORDS ---")
print(df.duplicated().sum())

print("\n--- NUMERICAL SUMMARY ---")
print(df.describe())

print("\n--- DATASET INFORMATION ---")
df.info()

print("\nDataset inspection completed.")