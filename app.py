import streamlit as st
import pandas as pd
from scraper import get_all_jobs

st.set_page_config(page_title="Global Remote Job Finder", layout="wide")
st.title("🌍 Global Remote Job Finder")

st.markdown(
    """
    Enter keywords separated by commas (e.g. Python, Marketing).
    Specify how many days back you want to search for job postings.
    The tool filters only jobs with location keywords like India, Asia, APAC, Worldwide, Remote.
    """
)

keywords_input = st.text_input("Enter Keywords (comma-separated):", placeholder="Python, Data Scientist, Marketing")
days_input = st.number_input("Posted Within Last (Days):", min_value=1, max_value=60, value=7, step=1)

if st.button("Search Jobs"):
    if not keywords_input.strip():
        st.warning("Please enter at least one keyword to search.")
    else:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
        with st.spinner("Searching jobs..."):
            jobs = get_all_jobs(keywords, days_input)

        if jobs:
            df = pd.DataFrame(jobs)
            st.success(f"Found {len(df)} matching jobs.")
            df_display = df[["Title", "Company", "Location", "DatePosted", "Source"]].copy()
            # Make URL clickable
            df_display["Job Link"] = df["URL"].apply(lambda url: f"[Link]({url})")

            st.dataframe(df_display, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Results as CSV", data=csv, file_name="remote_jobs.csv", mime="text/csv")
        else:
            st.info("No jobs found matching your criteria.")
