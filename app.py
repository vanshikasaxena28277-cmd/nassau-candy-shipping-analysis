# ============================================================
# Step 4 - Streamlit Web App
# Nassau Candy Distributor - Shipping Route Efficiency Project
# ============================================================

import pandas as pd
import streamlit as st
import plotly.express as px
import os

# -------------------------------------------------------
# Page Setup
# -------------------------------------------------------
st.set_page_config(
    page_title="Nassau Candy - Shipping Analysis",
    page_icon="🍬",
    layout="wide"
)

# -------------------------------------------------------
# Load and Prepare Data
# (All the cleaning and feature engineering happens here)
# -------------------------------------------------------

@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, "Nassau_Candy_Distributor.csv")
    df = pd.read_csv(csv_path)

    # Fix dates
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"])

    # Calculate lead time
    df["Lead Time (Days)"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # Remove bad records
    df = df[df["Lead Time (Days)"] > 0]

    # Map products to factories
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

    # Add factory coordinates
    factory_coords = {
        "Lot's O' Nuts"     : (32.881893, -111.768036),
        "Wicked Choccy's"   : (32.076176, -81.088371),
        "Sugar Shack"       : (48.11914,  -96.18115),
        "Secret Factory"    : (41.446333, -90.565487),
        "The Other Factory" : (35.1175,   -89.971107),
    }
    df["Factory Lat"] = df["Factory"].map(lambda x: factory_coords[x][0] if pd.notna(x) else None)
    df["Factory Lon"] = df["Factory"].map(lambda x: factory_coords[x][1] if pd.notna(x) else None)

    # Create route column
    df["Route"] = df["Factory"] + " → " + df["State/Province"]

    # Mark delays (more than 4 days = delayed)
    df["Is Delayed"] = df["Lead Time (Days)"] > 4

    return df

df = load_data()

# -------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------
st.sidebar.title("🍬 Filters")
st.sidebar.markdown("Use these filters to explore the data")

# Date range filter
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region filter
all_regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=all_regions,
    default=all_regions
)

# Ship mode filter
all_modes = sorted(df["Ship Mode"].dropna().unique())
selected_modes = st.sidebar.multiselect(
    "Select Ship Mode(s)",
    options=all_modes,
    default=all_modes
)

# Lead time threshold slider
lead_threshold = st.sidebar.slider(
    "Delay Threshold (Days)",
    min_value=1,
    max_value=10,
    value=4,
    help="Orders taking more than this many days are considered delayed"
)

# -------------------------------------------------------
# Apply Filters
# -------------------------------------------------------
filtered_df = df[
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(selected_regions)) &
    (df["Ship Mode"].isin(selected_modes))
].copy()

# Recalculate delay based on slider
filtered_df["Is Delayed"] = filtered_df["Lead Time (Days)"] > lead_threshold

# -------------------------------------------------------
# Main Title
# -------------------------------------------------------
st.title("🍬 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency Dashboard")
st.markdown("---")

# -------------------------------------------------------
# KPI Cards at the top
# -------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Orders",
    value=f"{len(filtered_df):,}"
)
col2.metric(
    label="Avg Lead Time (Days)",
    value=f"{filtered_df['Lead Time (Days)'].mean():.1f}"
)
col3.metric(
    label="Delayed Orders",
    value=f"{filtered_df['Is Delayed'].sum():,}"
)
col4.metric(
    label="Delay Rate",
    value=f"{filtered_df['Is Delayed'].mean() * 100:.1f}%"
)

st.markdown("---")

# -------------------------------------------------------
# Tab Layout for Dashboard Modules
# -------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Route Efficiency",
    "🗺️ Geographic Map",
    "🚚 Ship Mode Comparison",
    "🔍 Route Drill-Down"
])

# ===========================
# TAB 1 - Route Efficiency
# ===========================
with tab1:
    st.header("📦 Route Efficiency Overview")

    # Calculate route-level KPIs
    route_df = filtered_df.groupby("Route").agg(
        Total_Shipments = ("Order ID", "count"),
        Avg_Lead_Time   = ("Lead Time (Days)", "mean"),
        Delay_Rate      = ("Is Delayed", "mean")
    ).reset_index()
    route_df["Delay_Rate"] = (route_df["Delay_Rate"] * 100).round(2)
    route_df["Avg_Lead_Time"] = route_df["Avg_Lead_Time"].round(2)

    # Efficiency score
    min_lt = route_df["Avg_Lead_Time"].min()
    max_lt = route_df["Avg_Lead_Time"].max()
    if max_lt != min_lt:
        route_df["Efficiency Score"] = (
            (max_lt - route_df["Avg_Lead_Time"]) / (max_lt - min_lt) * 100
        ).round(2)
    else:
        route_df["Efficiency Score"] = 100.0

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top 10 Fastest Routes")
        top10 = route_df.sort_values("Avg_Lead_Time").head(10)
        fig = px.bar(
            top10,
            x="Avg_Lead_Time",
            y="Route",
            orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale="Greens_r",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)", "Route": "Route"},
            title="Top 10 Most Efficient Routes"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🐢 Bottom 10 Slowest Routes")
        bottom10 = route_df.sort_values("Avg_Lead_Time", ascending=False).head(10)
        fig2 = px.bar(
            bottom10,
            x="Avg_Lead_Time",
            y="Route",
            orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale="Reds",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)", "Route": "Route"},
            title="Bottom 10 Least Efficient Routes"
        )
        fig2.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Full Route Performance Table")
    st.dataframe(
        route_df.sort_values("Avg_Lead_Time").reset_index(drop=True),
        use_container_width=True
    )

# ===========================
# TAB 2 - Geographic Map
# ===========================
with tab2:
    st.header("🗺️ Geographic Shipping Map")

    # State-level average lead time
    state_df = filtered_df.groupby("State/Province").agg(
        Avg_Lead_Time   = ("Lead Time (Days)", "mean"),
        Total_Shipments = ("Order ID", "count")
    ).reset_index()
    state_df["Avg_Lead_Time"] = state_df["Avg_Lead_Time"].round(2)

    st.subheader("US Heatmap - Average Shipping Lead Time by State")
    fig_map = px.choropleth(
        state_df,
        locations="State/Province",
        locationmode="USA-states",
        color="Avg_Lead_Time",
        scope="usa",
        color_continuous_scale="RdYlGn_r",
        labels={"Avg_Lead_Time": "Avg Lead Time (Days)"},
        hover_name="State/Province",
        hover_data={"Total_Shipments": True},
        title="Average Shipping Lead Time by State (Darker = Slower)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Factory Locations on Map")
    factory_map_df = pd.DataFrame({
        "Factory"  : ["Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack", "Secret Factory", "The Other Factory"],
        "Latitude" : [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
        "Longitude": [-111.768036, -81.088371, -96.18115, -90.565487, -89.971107],
    })
    fig_factory = px.scatter_geo(
        factory_map_df,
        lat="Latitude",
        lon="Longitude",
        text="Factory",
        scope="usa",
        title="Factory Locations Across the US",
        size_max=15
    )
    fig_factory.update_traces(marker=dict(size=12, color="blue"))
    st.plotly_chart(fig_factory, use_container_width=True)

# ===========================
# TAB 3 - Ship Mode Comparison
# ===========================
with tab3:
    st.header("🚚 Ship Mode Performance Comparison")

    ship_df = filtered_df.groupby("Ship Mode").agg(
        Total_Shipments = ("Order ID", "count"),
        Avg_Lead_Time   = ("Lead Time (Days)", "mean"),
        Delay_Rate      = ("Is Delayed", "mean")
    ).reset_index()
    ship_df["Delay_Rate (%)"] = (ship_df["Delay_Rate"] * 100).round(2)
    ship_df["Avg_Lead_Time"]  = ship_df["Avg_Lead_Time"].round(2)

    col1, col2 = st.columns(2)

    with col1:
        fig_sm1 = px.bar(
            ship_df,
            x="Ship Mode",
            y="Avg_Lead_Time",
            color="Ship Mode",
            title="Average Lead Time by Ship Mode",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)"}
        )
        st.plotly_chart(fig_sm1, use_container_width=True)

    with col2:
        fig_sm2 = px.bar(
            ship_df,
            x="Ship Mode",
            y="Delay_Rate (%)",
            color="Ship Mode",
            title="Delay Rate (%) by Ship Mode",
            labels={"Delay_Rate (%)": "Delay Rate (%)"}
        )
        st.plotly_chart(fig_sm2, use_container_width=True)

    st.subheader("Ship Mode Summary Table")
    st.dataframe(
        ship_df[["Ship Mode", "Total_Shipments", "Avg_Lead_Time", "Delay_Rate (%)"]],
        use_container_width=True
    )

    # Lead time distribution by ship mode
    st.subheader("Lead Time Distribution by Ship Mode")
    fig_box = px.box(
        filtered_df,
        x="Ship Mode",
        y="Lead Time (Days)",
        color="Ship Mode",
        title="Lead Time Spread for Each Ship Mode"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ===========================
# TAB 4 - Route Drill-Down
# ===========================
with tab4:
    st.header("🔍 Route Drill-Down")

    # State selector
    all_states = sorted(filtered_df["State/Province"].dropna().unique())
    selected_state = st.selectbox("Select a State to Explore", options=all_states)

    state_data = filtered_df[filtered_df["State/Province"] == selected_state]

    st.markdown(f"### Showing results for: **{selected_state}**")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", f"{len(state_data):,}")
    col2.metric("Avg Lead Time", f"{state_data['Lead Time (Days)'].mean():.1f} days")
    col3.metric("Delay Rate", f"{state_data['Is Delayed'].mean() * 100:.1f}%")

    # Factory performance for selected state
    st.subheader(f"Factory Performance → {selected_state}")
    factory_state = state_data.groupby("Factory").agg(
        Total_Shipments = ("Order ID", "count"),
        Avg_Lead_Time   = ("Lead Time (Days)", "mean"),
        Delay_Rate      = ("Is Delayed", "mean")
    ).reset_index()
    factory_state["Delay_Rate (%)"] = (factory_state["Delay_Rate"] * 100).round(2)
    factory_state["Avg_Lead_Time"]  = factory_state["Avg_Lead_Time"].round(2)

    fig_fd = px.bar(
        factory_state,
        x="Factory",
        y="Avg_Lead_Time",
        color="Factory",
        title=f"Avg Lead Time by Factory → {selected_state}",
        labels={"Avg_Lead_Time": "Avg Lead Time (Days)"}
    )
    st.plotly_chart(fig_fd, use_container_width=True)

    # Order-level shipment timeline
    st.subheader(f"Order-Level Shipment Timeline for {selected_state}")
    timeline_df = state_data[["Order ID", "Order Date", "Ship Date", "Lead Time (Days)", "Factory", "Ship Mode", "Is Delayed"]].copy()
    timeline_df = timeline_df.sort_values("Order Date", ascending=False).head(50)
    timeline_df["Is Delayed"] = timeline_df["Is Delayed"].map({True: "⚠ Delayed", False: "✔ On Time"})
    st.dataframe(timeline_df.reset_index(drop=True), use_container_width=True)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.markdown("---")
st.markdown(
    "<center>Nassau Candy Distributor | Shipping Route Efficiency Dashboard | Built with Streamlit</center>",
    unsafe_allow_html=True
)
