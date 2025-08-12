import streamlit as st
from scraper import get_all_jobs

st.set_page_config(page_title="Remote Job Finder", layout="wide")

st.title("🌎 Remote Job Finder")
st.write("Find remote jobs filtered by keywords, location, and posted date.")

keywords_input = st.text_input("Enter keywords (comma separated)", "python, seo, data")
days_input = st.number_input("Posted within the last N days", min_value=1, max_value=60, value=7)

if st.button("Search Jobs"):
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    if not keywords:
        st.error("Please enter at least one keyword.")
    else:
        with st.spinner("Fetching jobs..."):
            jobs = get_all_jobs(keywords, days_input)
        if not jobs:
            st.warning("No jobs found for your filters.")
        else:
            st.success(f"Found {len(jobs)} jobs!")
            st.dataframe(jobs)
