import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import feedparser

# Allowed location keywords
LOCATION_KEYWORDS = ["india", "asia", "apac", "anywhere in the world", "ww", "worldwide", "remote"]

def fetch_remotive():
    url = "https://remotive.io/api/remote-jobs"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        jobs = []
        for job in data.get("jobs", []):
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "location": job["candidate_required_location"],
                "date": job["publication_date"],
                "url": job["url"],
                "source": "Remotive",
                "description": job["description"]
            })
        return jobs
    except Exception as e:
        print(f"Remotive error: {e}")
        return []

def fetch_remoteok():
