# ============================================================
# Step 3 - Route Analysis & KPI Calculations
# Nassau Candy Distributor - Shipping Route Efficiency Project
# ============================================================

import pandas as pd

# -------------------------------------------------------
# Load the cleaned dataset (created in Step 2)
# -------------------------------------------------------
df = pd.read_csv("Nassau_Candy_Cleaned.csv")

print("=" * 50)
print("STEP 3 - ROUTE ANALYSIS & KPIs STARTED")
print("=" * 50)

# -------------------------------------------------------
# KPI 1 - Average Lead Time per Route
# (How long does each factory-to-state route take on average)
# -------------------------------------------------------
route_analysis = df.groupby("Route").agg(
    Total_Shipments   = ("Order ID", "count"),
    Avg_Lead_Time     = ("Lead Time (Days)", "mean"),
    Min_Lead_Time     = ("Lead Time (Days)", "min"),
    Max_Lead_Time     = ("Lead Time (Days)", "max"),
    Std_Lead_Time     = ("Lead Time (Days)", "std"),  # how much lead time varies
).reset_index()

# Round to 2 decimal places for cleanliness
route_analysis = route_analysis.round(2)

print("\n✔ Route-level KPIs calculated!")

# -------------------------------------------------------
# KPI 2 - Delay Frequency
# We define a delay as: Lead Time > 4 days (threshold)
# -------------------------------------------------------
DELAY_THRESHOLD = 4  # days

df["Is Delayed"] = df["Lead Time (Days)"] > DELAY_THRESHOLD

delay_by_route = df.groupby("Route").agg(
    Delayed_Shipments = ("Is Delayed", "sum"),
    Total_Shipments   = ("Order ID", "count")
).reset_index()

delay_by_route["Delay Rate (%)"] = (
    delay_by_route["Delayed_Shipments"] / delay_by_route["Total_Shipments"] * 100
).round(2)

# Merge delay info into route analysis
route_analysis = route_analysis.merge(
    delay_by_route[["Route", "Delay Rate (%)"]],
    on="Route"
)

print("✔ Delay frequency calculated!")

# -------------------------------------------------------
# KPI 3 - Route Efficiency Score
# Lower average lead time = Higher efficiency score
# Score goes from 0 to 100 (100 = fastest route)
# -------------------------------------------------------
min_lt = route_analysis["Avg_Lead_Time"].min()
max_lt = route_analysis["Avg_Lead_Time"].max()

route_analysis["Efficiency Score"] = (
    (max_lt - route_analysis["Avg_Lead_Time"]) / (max_lt - min_lt) * 100
).round(2)

print("✔ Efficiency scores calculated!")

# -------------------------------------------------------
# Top 10 Most Efficient Routes (Fastest)
# -------------------------------------------------------
top10_fast = route_analysis.sort_values("Avg_Lead_Time").head(10)

print("\n" + "=" * 50)
print("TOP 10 FASTEST ROUTES")
print("=" * 50)
print(top10_fast[["Route", "Total_Shipments", "Avg_Lead_Time", "Efficiency Score"]].to_string(index=False))

# -------------------------------------------------------
# Bottom 10 Least Efficient Routes (Slowest)
# -------------------------------------------------------
top10_slow = route_analysis.sort_values("Avg_Lead_Time", ascending=False).head(10)

print("\n" + "=" * 50)
print("BOTTOM 10 SLOWEST ROUTES")
print("=" * 50)
print(top10_slow[["Route", "Total_Shipments", "Avg_Lead_Time", "Efficiency Score"]].to_string(index=False))

# -------------------------------------------------------
# KPI 4 - Ship Mode Performance
# Compare average lead time by shipping method
# -------------------------------------------------------
ship_mode_analysis = df.groupby("Ship Mode").agg(
    Total_Shipments = ("Order ID", "count"),
    Avg_Lead_Time   = ("Lead Time (Days)", "mean"),
    Delay_Rate      = ("Is Delayed", "mean")
).reset_index()

ship_mode_analysis["Delay_Rate"] = (ship_mode_analysis["Delay_Rate"] * 100).round(2)
ship_mode_analysis["Avg_Lead_Time"] = ship_mode_analysis["Avg_Lead_Time"].round(2)

print("\n" + "=" * 50)
print("SHIP MODE PERFORMANCE")
print("=" * 50)
print(ship_mode_analysis.to_string(index=False))

# -------------------------------------------------------
# KPI 5 - Regional Performance
# Which regions have the best and worst shipping times
# -------------------------------------------------------
region_analysis = df.groupby("Region").agg(
    Total_Shipments = ("Order ID", "count"),
    Avg_Lead_Time   = ("Lead Time (Days)", "mean"),
    Delay_Rate      = ("Is Delayed", "mean")
).reset_index()

region_analysis["Delay_Rate"] = (region_analysis["Delay_Rate"] * 100).round(2)
region_analysis["Avg_Lead_Time"] = region_analysis["Avg_Lead_Time"].round(2)

print("\n" + "=" * 50)
print("REGIONAL PERFORMANCE")
print("=" * 50)
print(region_analysis.to_string(index=False))

# -------------------------------------------------------
# Save all analysis results to CSV files
# -------------------------------------------------------
route_analysis.to_csv("Route_Analysis.csv", index=False)
ship_mode_analysis.to_csv("ShipMode_Analysis.csv", index=False)
region_analysis.to_csv("Region_Analysis.csv", index=False)

print("\n" + "=" * 50)
print("✔ Route_Analysis.csv saved!")
print("✔ ShipMode_Analysis.csv saved!")
print("✔ Region_Analysis.csv saved!")
print("=" * 50)
print("STEP 3 COMPLETE! Ready for Step 4 - Streamlit App")
print("=" * 50)
