import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Remote Job Finder", layout="wide")

# -------------------- Job Board Scrapers -------------------- #

def fetch_weworkremotely(keyword):
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    jobs = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for job_section in soup.find_all("section", class_="jobs"):
            for li in job_section.find_all("li", class_=False):
                title_tag = li.find("span", class_="title")
                company_tag = li.find("span", class_="company")
                link_tag = li.find("a", href=True)
                if title_tag and company_tag and link_tag:
                    jobs.append({
                        "title": title_tag.text.strip(),
                        "company": company_tag.text.strip(),
                        "location": "Worldwide",
                        "link": "https://weworkremotely.com" + link_tag["href"]
                    })
    except Exception as e:
        st.error(f"WeWorkRemotely error: {e}")
    return jobs


def fetch_remoteok(keyword):
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    jobs = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for tr in soup.find_all("tr", class_="job"):
            title_tag = tr.find("h2", itemprop="title")
            company_tag = tr.find("h3", itemprop="name")
            location_tag = tr.find("div", class_="location")
            link_tag = tr.find("a", href=True)
            if title_tag and company_tag and link_tag:
                jobs.append({
                    "title": title_tag.text.strip(),
                    "company": company_tag.text.strip(),
                    "location": location_tag.text.strip() if location_tag else "Worldwide",
                    "link": "https://remoteok.com" + link_tag["href"]
                })
    except Exception as e:
        st.error(f"RemoteOK error: {e}")
    return jobs


def fetch_justremote(keyword):
    url = f"https://justremote.co/remote-{keyword}-jobs"
    jobs = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for div in soup.find_all("div", class_="job-listing"):
            title_tag = div.find("h2")
            company_tag = div.find("span", class_="company")
            location_tag = div.find("span", class_="location")
            link_tag = div.find("a", href=True)
            if title_tag and company_tag and link_tag:
                jobs.append({
                    "title": title_tag.text.strip(),
                    "company": company_tag.text.strip(),
                    "location": location_tag.text.strip() if location_tag else "Worldwide",
                    "link": "https://justremote.co" + link_tag["href"]
                })
    except Exception as e:
        st.error(f"JustRemote error: {e}")
    return jobs

# -------------------- Streamlit UI -------------------- #

st.title("🌎 Remote Job Finder")
st.write("Find remote jobs across multiple boards.")

keyword = st.text_input("Enter job keyword (e.g., Python, SEO, Data Analyst):")
location_filter = st.selectbox("Filter by location", ["All", "US", "EU", "Worldwide"])

if st.button("Search Jobs"):
    if not keyword.strip():
        st.warning("Please enter a keyword to search.")
    else:
        with st.spinner("Fetching jobs..."):
            all_jobs = []
            all_jobs.extend(fetch_weworkremotely(keyword))
            all_jobs.extend(fetch_remoteok(keyword))
            all_jobs.extend(fetch_justremote(keyword))

            # Location filter
            if location_filter != "All":
                all_jobs = [job for job in all_jobs if location_filter.lower() in job["location"].lower()]

            if all_jobs:
                for job in all_jobs:
                    st.markdown(
                        f"**[{job['title']}]({job['link']})** — {job['company']} ({job['location']})"
                    )
            else:
                st.info("No jobs found for your search criteria.")
