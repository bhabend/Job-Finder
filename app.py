import streamlit as st
import requests
from datetime import datetime, timedelta

# --- Helper Functions ---
def fetch_remotive_jobs():
    url = "https://remotive.com/api/remote-jobs"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("jobs", [])
    except:
        return []
    return []

def fetch_wwr_jobs():
    url = "https://weworkremotely.com/remote-jobs.json"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("jobs", [])
    except:
        return []
    return []

def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == 200:
            data = res.json()
            # First element is metadata
            return data[1:]
    except:
        return []
    return []

def filter_jobs(jobs, keyword, location_kw, days):
    filtered = []
    now = datetime.utcnow()
    for job in jobs:
        title = job.get("title", "").lower()
        location = job.get("candidate_required_location", job.get("location", "")).lower()
        url = job.get("url") or job.get("url_apply") or job.get("apply_url")

        # Convert date to datetime object
        date_str = job.get("publication_date") or job.get("date") or job.get("created_at")
        job_date = None
        try:
            job_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            try:
                job_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
            except:
                job_date = now

        if keyword.lower() in title and (location_kw.lower() in location or "worldwide" in location or "anywhere" in location):
            if (now - job_date) <= timedelta(days=days):
                filtered.append({
                    "title": job.get("title"),
                    "company": job.get("company_name", job.get("company", "")),
                    "location": location,
                    "url": url
                })
    return filtered

# --- Streamlit App ---
st.set_page_config(page_title="Remote Job Finder", layout="wide")
st.title("🌍 Remote Job Finder")

keyword = st.text_input("🔍 Job Keyword", placeholder="e.g., Python Developer")
location_kw = st.text_input("📍 Location Keyword", placeholder="e.g., India, US, EU, Worldwide Remote")
days = st.number_input("🕒 Posted in last X days", min_value=1, max_value=60, value=7)

if st.button("Find Jobs"):
    with st.spinner("Fetching jobs..."):
        jobs = []
        jobs.extend(fetch_remotive_jobs())
        jobs.extend(fetch_wwr_jobs())
        jobs.extend(fetch_remoteok_jobs())

        filtered_jobs = filter_jobs(jobs, keyword, location_kw, days)

    if filtered_jobs:
        st.success(f"Found {len(filtered_jobs)} jobs matching your criteria.")
        for job in filtered_jobs:
            st.markdown(f"**[{job['title']}]({job['url']})**  \n"
                        f"📌 {job['company']} — {job['location']}")
            st.markdown("---")
    else:
        st.warning("No jobs found. Try different keywords or date range.")
