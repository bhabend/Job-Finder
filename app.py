import streamlit as st
from scraper import scrape_jobs
from filters import filter_jobs

st.set_page_config(page_title="Job Finder", page_icon="💼", layout="wide")

st.title("💼 Job Finder - Worldwide & Remote Search")

# Sidebar filters
st.sidebar.header("Filter Jobs")

keywords = st.sidebar.text_input(
    "Keywords (comma-separated)", value="Python, AI, Data"
).split(",")

days = st.sidebar.slider(
    "Show jobs posted in the last X days", min_value=1, max_value=30, value=7
)

location_keyword = st.sidebar.text_input(
    "Location filter (leave blank for worldwide)", value=""
)

if st.sidebar.button("Search Jobs"):
    st.info("🔍 Searching for jobs... please wait.")

    try:
        jobs = scrape_jobs()  # Fetch jobs from your scraper
        filtered = filter_jobs(jobs, keywords, days, location_keyword)

        if not filtered:
            st.warning("No jobs found with the given filters.")
        else:
            st.success(f"Found {len(filtered)} matching jobs.")

            for job in filtered:
                with st.container():
                    st.markdown(
                        f"### [{job['title']}]({job['link']})"
                    )
                    st.write(f"📍 **Location:** {job.get('location', 'N/A')}")
                    st.write(f"📅 **Date Posted:** {job.get('date_posted', 'N/A')}")
                    st.write(f"📝 **Company:** {job.get('company', 'N/A')}")
                    st.markdown("---")

    except Exception as e:
        st.error(f"Error fetching jobs: {e}")

else:
    st.info("Use the filters in the sidebar and click **Search Jobs** to get started.")
