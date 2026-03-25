# ============================================================
# Step 1 - Exploratory Data Analysis (EDA)
# Nassau Candy Distributor - Shipping Route Efficiency Project
# ============================================================

# Import the libraries we need
import pandas as pd

# -------------------------------------------------------
# Load the dataset
# -------------------------------------------------------
df = pd.read_csv("Nassau_Candy_Distributor.csv")

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)

# How many rows and columns are in the dataset
print(f"\nTotal Rows    : {df.shape[0]}")
print(f"Total Columns : {df.shape[1]}")

# Show column names
print("\nColumn Names:")
for col in df.columns:
    print(f"  - {col}")

# -------------------------------------------------------
# Check data types of each column
# -------------------------------------------------------
print("\n" + "=" * 50)
print("DATA TYPES OF EACH COLUMN")
print("=" * 50)
print(df.dtypes)

# -------------------------------------------------------
# Check for missing values
# -------------------------------------------------------
print("\n" + "=" * 50)
print("MISSING VALUES IN EACH COLUMN")
print("=" * 50)
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No missing values found!")

# -------------------------------------------------------
# Show the first 5 rows to understand what data looks like
# -------------------------------------------------------
print("\n" + "=" * 50)
print("FIRST 5 ROWS OF THE DATASET")
print("=" * 50)
print(df.head())

# -------------------------------------------------------
# Basic stats for number columns (Sales, Cost, etc.)
# -------------------------------------------------------
print("\n" + "=" * 50)
print("BASIC STATISTICS (Numbers Only)")
print("=" * 50)
print(df.describe())

# -------------------------------------------------------
# Unique values in important columns
# -------------------------------------------------------
print("\n" + "=" * 50)
print("UNIQUE VALUES IN KEY COLUMNS")
print("=" * 50)

key_cols = ["Ship Mode", "Region", "Division", "Country/Region"]
for col in key_cols:
    print(f"\n{col}: {df[col].nunique()} unique values")
    print(f"  {df[col].unique()}")

print("\n" + "=" * 50)
print("EDA COMPLETE! Ready for Step 2 - Data Cleaning")
print("=" * 50)
