import streamlit as st
import pandas as pd

st.title("Shipping Route Efficiency Dashboard")

# Load data (your actual file name)
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Create Lead Time
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Sidebar filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect("Select Region", df['Region'].unique())
ship_mode = st.sidebar.multiselect("Select Ship Mode", df['Ship Mode'].unique())

# Apply filters
if region:
    df = df[df['Region'].isin(region)]

if ship_mode:
    df = df[df['Ship Mode'].isin(ship_mode)]

# Charts
st.subheader("Average Lead Time by State")
state_avg = df.groupby('State/Province')['Lead Time'].mean().sort_values()
st.bar_chart(state_avg)

st.subheader("Ship Mode Comparison")
mode_avg = df.groupby('Ship Mode')['Lead Time'].mean()
st.bar_chart(mode_avg)

# Fastest routes
st.subheader("Top 10 Fastest Routes")
fast_routes = df.groupby(['Region', 'State/Province'])['Lead Time'].mean().nsmallest(10)
st.write(fast_routes)

# Slowest routes
st.subheader("Top 10 Slowest Routes")
slow_routes = df.groupby(['Region', 'State/Province'])['Lead Time'].mean().nlargest(10)
st.write(slow_routes)
