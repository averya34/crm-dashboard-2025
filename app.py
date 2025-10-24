import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os

st.set_page_config(page_title="CRM Dashboard 2025", layout="wide")

# Title
st.title("📊 CRM Dashboard 2025")

# Load data
data_dir = Path("data")
csv_files = list(data_dir.glob("*.csv"))

if not csv_files:
    st.error("No CSV files found in /data/ folder. Please run the notebook first.")
    st.stop()

# Sidebar - File Selection
st.sidebar.header("🗂️ Data Selection")
selected_files = st.sidebar.multiselect(
    "Select CSV files to analyze:",
    options=[f.name for f in csv_files],
    default=[csv_files[0].name] if csv_files else []
)

if not selected_files:
    st.warning("Please select at least one CSV file from the sidebar.")
    st.stop()

# Load and merge selected files
dfs = []
for file in selected_files:
    df_temp = pd.read_csv(data_dir / file)
    dfs.append(df_temp)

df = pd.concat(dfs, ignore_index=True)

# Convert dates
df["Date Added"] = pd.to_datetime(df["Date Added"], errors="coerce")
df["Last Assigned"] = pd.to_datetime(df["Last Assigned"], errors="coerce")

# Sidebar - Filters
st.sidebar.header("🧭 Filters")

# Project filter
if "Project" in df.columns:
    projects = ["All"] + sorted(df["Project"].dropna().unique().tolist())
    selected_project = st.sidebar.selectbox("Project", projects)
    if selected_project != "All":
        df = df[df["Project"] == selected_project]

# Source filter
if "Source" in df.columns:
    sources = ["All"] + sorted(df["Source"].dropna().unique().tolist())
    selected_source = st.sidebar.selectbox("Source", sources)
    if selected_source != "All":
        df = df[df["Source"] == selected_source]

# Lead Type filter
if "Lead Type" in df.columns:
    lead_types = ["All"] + sorted(df["Lead Type"].dropna().unique().tolist())
    selected_lead_type = st.sidebar.selectbox("Lead Type", lead_types)
    if selected_lead_type != "All":
        df = df[df["Lead Type"] == selected_lead_type]

# Date Type Toggle
st.sidebar.header("📅 Date Settings")
date_type = st.sidebar.radio("Date Type", ["Date Added", "Last Assigned"])

# Date Range Filter
date_col = "Date Added" if date_type == "Date Added" else "Last Assigned"
valid_dates = df[date_col].dropna()

if len(valid_dates) > 0:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        df = df[(df[date_col].dt.date >= date_range[0]) & (df[date_col].dt.date <= date_range[1])]

# Top Metrics
st.header("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Leads", len(df))

with col2:
    if "Project" in df.columns:
        st.metric("🏗 Unique Projects", df["Project"].nunique())
    else:
        st.metric("🏗 Unique Projects", "N/A")

with col3:
    if "Source" in df.columns:
        st.metric("🌐 Unique Sources", df["Source"].nunique())
    else:
        st.metric("🌐 Unique Sources", "N/A")

with col4:
    if "Lead Type" in df.columns:
        reengaged_pct = (df["Lead Type"] == "Reengaged").sum() / len(df) * 100 if len(df) > 0 else 0
        st.metric("🔁 Reengaged %", f"{reengaged_pct:.1f}%")
    else:
        st.metric("🔁 Reengaged %", "N/A")

# Charts
st.header("📊 Visualizations")

# Leads by Project
if "Project" in df.columns:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Leads by Project")
        project_counts = df["Project"].value_counts().reset_index()
        project_counts.columns = ["Project", "Count"]
        fig1 = px.bar(project_counts, x="Project", y="Count", color="Project")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Leads by Source")
        if "Source" in df.columns:
            source_counts = df["Source"].value_counts().reset_index()
            source_counts.columns = ["Source", "Count"]
            fig2 = px.pie(source_counts, names="Source", values="Count")
            st.plotly_chart(fig2, use_container_width=True)

# Lead Timeline
st.subheader("📅 Lead Creation Timeline")

freq_col1, freq_col2 = st.columns([1, 3])
with freq_col1:
    frequency = st.radio("Frequency", ["Daily", "Weekly", "Monthly"])

freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}

if len(df[date_col].dropna()) > 0:
    timeline_df = df.copy()
    timeline_df = timeline_df.dropna(subset=[date_col])
    timeline_df["Date"] = timeline_df[date_col].dt.to_period(freq_map[frequency]).dt.to_timestamp()
    
    if "Source" in timeline_df.columns:
        timeline_counts = timeline_df.groupby(["Date", "Source"]).size().reset_index(name="Count")
        fig3 = px.line(timeline_counts, x="Date", y="Count", color="Source", markers=True)
    else:
        timeline_counts = timeline_df.groupby("Date").size().reset_index(name="Count")
        fig3 = px.line(timeline_counts, x="Date", y="Count", markers=True)
    
    st.plotly_chart(fig3, use_container_width=True)

# Reengagement Trend
if "Lead Type" in df.columns:
    st.subheader("🔁 Reengagement Trend")
    
    reeng_df = df.dropna(subset=[date_col])
    reeng_df["Date"] = reeng_df[date_col].dt.to_period(freq_map[frequency]).dt.to_timestamp()
    reeng_counts = reeng_df.groupby(["Date", "Lead Type"]).size().reset_index(name="Count")
    
    fig4 = px.line(reeng_counts, x="Date", y="Count", color="Lead Type", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

# Data Preview
st.header("🔍 Data Preview")
with st.expander("View Raw Data"):
    st.dataframe(df, use_container_width=True)
