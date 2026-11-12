
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "Global_Superstore2.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "global_superstore_cleaned.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load original dataset
df = pd.read_excel(INPUT_FILE, engine="openpyxl")

print("INITIAL ROWS:", len(df))

# 1. Standardize column names
df.columns = df.columns.str.strip()

# 2. Remove unnecessary spaces from text fields
text_columns = df.select_dtypes(include=["object", "str"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# 3. Convert date columns
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], errors="coerce"
)

# 4. Report invalid dates
print("\nINVALID ORDER DATES:", df["Order Date"].isna().sum())
print("INVALID SHIP DATES:", df["Ship Date"].isna().sum())

# 5. Check duplicate records
print("\nDUPLICATE ROWS:", df.duplicated().sum())
print("DUPLICATE ROW IDs:", df["Row ID"].duplicated().sum())

# 6. Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# 7. Check potentially problematic numerical values
print("\nNEGATIVE SALES:", (df["Sales"] < 0).sum())
print("NEGATIVE QUANTITIES:", (df["Quantity"] < 0).sum())
print("NEGATIVE SHIPPING COSTS:", (df["Shipping Cost"] < 0).sum())

# 8. Create analytical date columns
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month
df["Order Month Name"] = df["Order Date"].dt.month_name()

# 9. Calculate shipping duration
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# 10. Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\nCLEANING SUMMARY")
print("Final rows:", len(df))
print("Final columns:", len(df.columns))
print("Output file:", OUTPUT_FILE)

print("\nDATA CLEANING COMPLETED.")
