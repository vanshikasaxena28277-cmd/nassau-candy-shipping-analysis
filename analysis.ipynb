import pandas as pd

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("Nassau Candy Distributor.csv")

print("Shape:", df.shape)
print("\nColumns:\n", df.columns)

# ----------------------------
# Data Cleaning
# ----------------------------
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

df = df.dropna(subset=['Order Date', 'Ship Date'])

# Lead Time
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Remove invalid lead times
df = df[df['Lead Time'] > 0]

print("\nData cleaned successfully!")

# ----------------------------
# Factory Mapping
# ----------------------------
product_factory = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(product_factory)

# Route
df["Route"] = df["Factory"] + " → " + df["State/Province"]

# ----------------------------
# Route Analysis
# ----------------------------
route_analysis = df.groupby("Route").agg(
    Total_Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean")
).reset_index()

route_analysis = route_analysis.sort_values("Avg_Lead_Time")

print("\nTop 10 Fastest Routes")
print(route_analysis.head(10))

print("\nTop 10 Slowest Routes")
print(route_analysis.tail(10))

# ----------------------------
# Ship Mode Analysis
# ----------------------------
ship_mode_analysis = df.groupby("Ship Mode").agg(
    Total_Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean")
).reset_index()

print("\nShip Mode Performance")
print(ship_mode_analysis)

# ----------------------------
# Region Analysis
# ----------------------------
region_analysis = df.groupby("Region").agg(
    Total_Shipments=("Order ID", "count"),
    Avg_Lead_Time=("Lead Time", "mean")
).reset_index()

print("\nRegion Performance")
print(region_analysis)

# ----------------------------
# Save Outputs (optional)
# ----------------------------
route_analysis.to_csv("Route_Analysis.csv", index=False)
ship_mode_analysis.to_csv("ShipMode_Analysis.csv", index=False)
region_analysis.to_csv("Region_Analysis.csv", index=False)

print("\nAll analysis completed and files saved!")
