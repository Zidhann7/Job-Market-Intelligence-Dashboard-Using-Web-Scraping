import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="Job Market Intelligence Dashboard",
    layout="wide"
)

st.title("📊 Job Market Intelligence Dashboard")

# ---------------------------------
# File Upload
# ---------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Load Data
    df = pd.read_csv(uploaded_file)

    # Clean Column Names
    df.columns = df.columns.str.strip().str.lower()

    # Convert Date
    df["posting date"] = pd.to_datetime(df["posting date"])

    # ---------------------------------
    # Sidebar Filters
    # ---------------------------------

    st.sidebar.header("Filters")

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [
            df["posting date"].min(),
            df["posting date"].max()
        ]
    )

    company_filter = st.sidebar.multiselect(
        "Select Company",
        options=sorted(df["company"].unique())
    )

    location_filter = st.sidebar.multiselect(
        "Select Location",
        options=sorted(df["location"].unique())
    )

    # ---------------------------------
    # Show Raw Data
    # ---------------------------------

    if st.checkbox("Show Dataset"):
        st.dataframe(df)

    # ---------------------------------
    # Apply Filters
    # ---------------------------------

    filtered_data = df.copy()

    if len(date_range) == 2:
        filtered_data = filtered_data[
            (filtered_data["posting date"] >= pd.to_datetime(date_range[0])) &
            (filtered_data["posting date"] <= pd.to_datetime(date_range[1]))
        ]

    if company_filter:
        filtered_data = filtered_data[
            filtered_data["company"].isin(company_filter)
        ]

    if location_filter:
        filtered_data = filtered_data[
            filtered_data["location"].isin(location_filter)
        ]

    st.markdown("---")

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Jobs",
            filtered_data.shape[0]
        )

    with col2:
        st.metric(
            "Total Companies",
            filtered_data["company"].nunique()
        )

    with col3:
        st.metric(
            "Total Locations",
            filtered_data["location"].nunique()
        )

    st.markdown("---")

    # ---------------------------------
    # Top Companies
    # ---------------------------------

    top_companies = (
        filtered_data["company"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_companies.columns = [
        "company",
        "jobs"
    ]

    top_companies = top_companies.sort_values(
        by="jobs",
        ascending=True
    )

    fig_company = px.bar(
        top_companies,
        x="jobs",
        y="company",
        orientation="h",
        title="Top Hiring Companies"
    )

    # ---------------------------------
    # Top Locations
    # ---------------------------------

    top_locations = (
        filtered_data["location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_locations.columns = [
        "location",
        "jobs"
    ]

    top_locations = top_locations.sort_values(
        by="jobs",
        ascending=True
    )

    fig_location = px.bar(
        top_locations,
        x="jobs",
        y="location",
        orientation="h",
        title="Top Hiring Locations"
    )

    # ---------------------------------
    # Charts Row 1
    # ---------------------------------

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            fig_company,
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            fig_location,
            use_container_width=True
        )

    # ---------------------------------
    # Top Job Titles
    # ---------------------------------

    top_titles = (
        filtered_data["job_title"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_titles.columns = [
        "job_title",
        "count"
    ]

    top_titles = top_titles.sort_values(
        by="count",
        ascending=True
    )

    fig_titles = px.bar(
        top_titles,
        x="count",
        y="job_title",
        orientation="h",
        title="Most Common Job Titles"
    )

    # ---------------------------------
    # Company Share
    # ---------------------------------

    company_share = (
        filtered_data["company"]
        .value_counts()
        .head(5)
        .reset_index()
    )

    company_share.columns = [
        "company",
        "jobs"
    ]

    fig_pie = px.pie(
        company_share,
        names="company",
        values="jobs",
        title="Company Job Share"
    )

    # ---------------------------------
    # Charts Row 2
    # ---------------------------------

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            fig_titles,
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    # ---------------------------------
    # Job Posting Trend
    # ---------------------------------

    trend = (
        filtered_data.groupby("posting date")
        .size()
        .reset_index(name="jobs")
    )

    fig_trend = px.line(
        trend,
        x="posting date",
        y="jobs",
        markers=True,
        title="Job Posting Trend"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

    # ---------------------------------
    # Data Table
    # ---------------------------------

    st.subheader("Job Listings")

    st.dataframe(
        filtered_data,
        use_container_width=True
    )

    # ---------------------------------
    # Download Button
    # ---------------------------------

    csv = filtered_data.to_csv(index=False)

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_jobs.csv",
        mime="text/csv"
    )