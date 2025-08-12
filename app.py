import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# ---------------------
# Helper function to fetch jobs
# ---------------------
def fetch_jobs(keywords, location, days):
    """
    Fetch jobs from remoteok.com matching keywords, location, and posted within given days.
    """
    url = "https://remoteok.com/remote-{0}-jobs".format(keywords.replace(" ", "-"))
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            st.error(f"Failed to fetch jobs. Status code: {resp.status_code}")
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for tr in soup.find_all("tr", class_="job"):
            title_tag = tr.find("h2", itemprop="title")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = tr.get("data-href")
            company_tag = tr.find("h3", itemprop="name")
            company = company_tag.get_text(strip=True) if company_tag else "N/A"
            date_tag = tr.find("time")
            post_date = date_tag["datetime"] if date_tag and "datetime" in d_
