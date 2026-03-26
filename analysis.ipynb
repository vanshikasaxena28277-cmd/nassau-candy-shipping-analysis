import pandas as pd

df = pd.read_csv("Nassau Candy Distributor.csv")

df.head()

# Convert dates safely
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

# Create Lead Time FIRST
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Now you can use it
df.groupby('Region')['Lead Time'].mean()

df.describe()
