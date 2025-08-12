import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

LOCATION_KEYWORDS = ["india", "asia", "apac", "anywhere in the world", "ww", "worldwide", "remote"]

def is_within_days(date_str, days):
    """Check if job is within the user-specified days"""
    try:
        posted_date = datetime.fromisoformat(date_str)
    except:
        try:
            posted_date = datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return False
    return datetime.now() - posted_date <= timedelta(days=days)

def matches_location(location, description):
    text = f"{location} {description}".lower()
    return any(loc in text for loc in LOCATION_KEYWORDS)

def matches_keywords(title, description, keywords):
    text = f"{title} {description}".lower()
    return any(kw in text for kw in keywords)

def fetch_remoteok():
    jobs = []
    try:
        res = requests.get("https://remoteok.com/api", headers={"User-Agent": "Mozilla/5.0"})
        data = res.json()[1:]  # skip metadata
        for job in data:
            jobs.append({
                "title": job.get("position"),
                "company": job.get("company"),
                "location": job.get("location"),
                "url": job.get("url"),
                "date": job.get("date"),
                "description": job.get("description", "")
            })
    except:
        pass
    return jobs

def fetch_remotive():
    jobs = []
    try:
        res = requests.get("https://remotive.io/api/remote-jobs")
        for job in res.json().get("jobs", []):
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "location": job["candidate_required_location"],
                "url": job["url"],
                "date": job["publication_date"],
                "description": job.get("description", "")
            })
    except:
        pass
    return jobs

def fetch_weworkremotely():
    jobs = []
    try:
        res = requests.get("https://weworkremotely.com/remote-jobs.rss")
        soup = BeautifulSoup(res.text, "xml")
        for item in soup.find_all("item"):
            jobs.append({
                "title": item.title.text,
                "company": "",
                "location": "",
                "url": item.link.text,
                "date": item.pubDate.text,
                "description": item.description.text
            })
    except:
        pass
    return jobs

# Additional scrapers can be added below using same pattern
# Example: SkipTheDrive, Jobspresso, Remote.co, etc.

def get_all_jobs(keywords, days):
    raw_jobs = []

    # Fetch from APIs
    raw_jobs.extend(fetch_remoteok())
    raw_jobs.extend(fetch_remotive())
    raw_jobs.extend(fetch_weworkremotely())

    # TODO: Add more scrapers like SkipTheDrive, Jobspresso, Remote.co, etc.

    # Filter
    filtered_jobs = []
    for job in raw_jobs:
        if not job.get("title") or not job.get("url"):
            continue
        if not matches_keywords(job["title"], job.get("description", ""), keywords):
            continue
        if not matches_location(job.get("location", ""), job.get("description", "")):
            continue
        if not is_within_days(job.get("date", ""), days):
            continue
        filtered_jobs.append(job)

    # Remove duplicates by URL
    seen = set()
    unique_jobs = []
    for job in filtered_jobs:
        if job["url"] not in seen:
            seen.add(job["url"])
            unique_jobs.append(job)

    return unique_jobs
