import streamlit as st
import pandas as pd

st.title("🍬 Shipping Route Efficiency Dashboard")

# Load data
df = pd.read_csv("Nassau Candy Distributor.csv")

# Fix dates safely
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

df = df.dropna(subset=['Order Date', 'Ship Date'])

# Lead time
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# ----------------------------
# Factory Mapping (IMPORTANT)
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

# Route column
df["Route"] = df["Factory"] + " → " + df["State/Province"]

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect("Region", df["Region"].unique())
ship_mode = st.sidebar.multiselect("Ship Mode", df["Ship Mode"].unique())

if region:
    df = df[df["Region"].isin(region)]

if ship_mode:
    df = df[df["Ship Mode"].isin(ship_mode)]

# ----------------------------
# KPIs
# ----------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(df))
col2.metric("Average Lead Time", f"{df['Lead Time'].mean():.1f} days")
col3.metric("Max Lead Time", f"{df['Lead Time'].max()} days")

# ----------------------------
# Route Analysis
# ----------------------------
route_df = df.groupby("Route")["Lead Time"].mean().sort_values()

st.subheader("Top 10 Fastest Routes")
st.write(route_df.head(10))

st.subheader("Top 10 Slowest Routes")
st.write(route_df.tail(10))

# ----------------------------
# Charts
# ----------------------------
st.subheader("Average Lead Time by State")
state_avg = df.groupby("State/Province")["Lead Time"].mean()
st.bar_chart(state_avg)

st.subheader("Ship Mode Comparison")
mode_avg = df.groupby("Ship Mode")["Lead Time"].mean()
st.bar_chart(mode_avg)

# ----------------------------
# Data Preview
# ----------------------------
st.subheader("Dataset Preview")
st.write(df.head())
