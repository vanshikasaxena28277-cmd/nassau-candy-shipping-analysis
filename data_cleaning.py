# ============================================================
# Step 2 - Data Cleaning & Feature Engineering
# Nassau Candy Distributor - Shipping Route Efficiency Project
# ============================================================

import pandas as pd

# -------------------------------------------------------
# Load the dataset
# -------------------------------------------------------
df = pd.read_csv("Nassau_Candy_Distributor.csv")

print("=" * 50)
print("STEP 2 - DATA CLEANING STARTED")
print("=" * 50)

# -------------------------------------------------------
# Fix Date Columns
# Convert Order Date and Ship Date from text to real dates
# -------------------------------------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"]  = pd.to_datetime(df["Ship Date"])

print("\n✔ Dates converted successfully!")

# -------------------------------------------------------
# Calculate Shipping Lead Time
# Lead Time = How many days it took to ship the order
# -------------------------------------------------------
df["Lead Time (Days)"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("✔ Lead Time calculated!")

# -------------------------------------------------------
# Remove rows where Lead Time is negative or zero
# (These are bad/incorrect records)
# -------------------------------------------------------
before = len(df)
df = df[df["Lead Time (Days)"] > 0]
after = len(df)

print(f"✔ Removed {before - after} invalid rows (negative or zero lead time)")

# -------------------------------------------------------
# Map each Product to its Factory
# (Based on the Products and Factories table given)
# -------------------------------------------------------
product_to_factory = {
    "Wonka Bar - Nutty Crunch Surprise"  : "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows"          : "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious"     : "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate"         : "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel"  : "Wicked Choccy's",
    "Laffy Taffy"                        : "Sugar Shack",
    "SweeTARTS"                          : "Sugar Shack",
    "Nerds"                              : "Sugar Shack",
    "Fun Dip"                            : "Sugar Shack",
    "Fizzy Lifting Drinks"               : "Sugar Shack",
    "Everlasting Gobstopper"             : "Secret Factory",
    "Lickable Wallpaper"                 : "Secret Factory",
    "Wonka Gum"                          : "Secret Factory",
    "Hair Toffee"                        : "The Other Factory",
    "Kazookles"                          : "The Other Factory",
}

df["Factory"] = df["Product Name"].map(product_to_factory)

print("✔ Factory names mapped to each product!")

# -------------------------------------------------------
# Add Factory Coordinates (Latitude & Longitude)
# -------------------------------------------------------
factory_coords = {
    "Lot's O' Nuts"     : (32.881893, -111.768036),
    "Wicked Choccy's"   : (32.076176, -81.088371),
    "Sugar Shack"       : (48.11914,  -96.18115),
    "Secret Factory"    : (41.446333, -90.565487),
    "The Other Factory" : (35.1175,   -89.971107),
}

df["Factory Lat"] = df["Factory"].map(lambda x: factory_coords[x][0] if pd.notna(x) else None)
df["Factory Lon"] = df["Factory"].map(lambda x: factory_coords[x][1] if pd.notna(x) else None)

print("✔ Factory coordinates added!")

# -------------------------------------------------------
# Create a Route Column
# Route = Factory --> Customer State
# -------------------------------------------------------
df["Route"] = df["Factory"] + " → " + df["State/Province"]

print("✔ Route column created!")

# -------------------------------------------------------
# Check for any products that didn't get a factory mapped
# -------------------------------------------------------
missing_factory = df[df["Factory"].isnull()]
if len(missing_factory) > 0:
    print(f"\n⚠ Warning: {len(missing_factory)} rows have no factory mapped!")
    print(missing_factory["Product Name"].unique())
else:
    print("✔ All products have a factory mapped!")

# -------------------------------------------------------
# Save the cleaned dataset
# -------------------------------------------------------
df.to_csv("Nassau_Candy_Cleaned.csv", index=False)

print("\n" + "=" * 50)
print(f"✔ Cleaned dataset saved as: Nassau_Candy_Cleaned.csv")
print(f"  Total rows after cleaning : {len(df)}")
print(f"  Total columns now         : {len(df.columns)}")
print("\nNew columns added:")
print("  - Lead Time (Days)")
print("  - Factory")
print("  - Factory Lat")
print("  - Factory Lon")
print("  - Route")
print("=" * 50)
print("STEP 2 COMPLETE! Ready for Step 3 - Route Analysis")
print("=" * 50)
