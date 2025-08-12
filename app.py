import streamlit as st
from scraper import get_all_jobs
import pandas as pd

st.set_page_config(page_title="Global Remote Job Finder", layout="wide")

st.title("🌍 Global Remote Job Finder")
st.write("Find remote jobs posted within a specific time period, filtered by keywords & location.")

# User inputs
keywords_input = st.text_input(
    "Enter keywords (comma-separated)",
    placeholder="Example: Python, Data Scientist, Marketing"
)
days_input = st.number_input(
    "Posted within (days)",
    min_value=1, max_value=60, value=7
)

if st.button("Search Jobs"):
    if not keywords_input.strip():
        st.warning("Please enter at least one keyword.")
    else:
        keywords = [kw.strip().lower() for kw in keywords_input.split(",") if kw.strip()]
        jobs = get_all_jobs(keywords, days_input)

        if jobs:
            df = pd.DataFrame(jobs)
            st.success(f"Found {len(df)} jobs matching your criteria.")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv, file_name="remote_jobs.csv", mime="text/csv")
        else:
            st.error("No jobs found matching your criteria.")
