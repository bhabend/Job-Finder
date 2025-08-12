import streamlit as st
from scraper import fetch_remoteok_jobs, fetch_wwr_jobs, fetch_remotive_jobs
from filters import filter_jobs
import pandas as pd

# Streamlit page setup
st.set_page_config(page_title="International Remote Job Finder", layout="wide")

st.title("🌎 International Remote Job Finder")

# Input fields
keywords_input = st.text_input(
    "Enter job keywords (comma separated)", 
    "SEO Manager, Python Developer"
)
days_input = st.number_input(
    "Time period (days)", 
    min_value=1, 
    max_value=60, 
    value=7
)
location_keyword = st.text_input(
    "Location keyword", 
    "India"
)

# Search button
if st.button("Find Jobs"):
    st.write("Fetching jobs... Please wait.")

    jobs = []
    jobs.extend(fetch_remoteok_jobs())    # RemoteOK
    jobs.extend(fetch_wwr_jobs())         # We Work Remotely
    jobs.extend(fetch_remotive_jobs())    # Remotive API

    # Apply filters
    filtered = filter_jobs(
        jobs,
        keywords=[k.strip() for k in keywords_input.split(",")],
        days=days_input,
        location_keyword=location_keyword
    )

    # Show results
    if filtered:
        df = pd.DataFrame(filtered)
        st.success(f"Found {len(filtered)} matching jobs!")
        st.dataframe(df)

        # Download as CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download results as CSV",
            data=csv,
            file_name="jobs.csv",
            mime="text/csv"
        )
    else:
        st.warning("No matching jobs found for the given criteria.")
