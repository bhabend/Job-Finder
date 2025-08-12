# scraper.py
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timezone
from utils import keyword_match, location_match, date_within_range

def fetch_remoteok():
    jobs = []
    try:
        res = requests.get("https://remoteok.com/api", headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        res.raise_for_status()
        data = res.json()
        for item in data:
            if not isinstance(item, dict) or not item.get("position"):
                continue
            jobs.append({
                "title": item.get("position", ""),
                "company": item.get("company", ""),
                "location": item.get("location", ""),
                "date": item.get("date", ""),
                "url": item.get("url", "") or item.get("url_apply", ""),
                "description": item.get("description", ""),
                "source": "RemoteOK"
            })
    except:
        pass
    return jobs

def fetch_remotive():
    jobs = []
    try:
        res = requests.get("https://remotive.io/api/remote-jobs", timeout=15)
        res.raise_for_status()
        data = res.json()
        for item in data.get("jobs", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("candidate_required_location", ""),
                "date": item.get("publication_date", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "source": "Remotive"
            })
    except:
        pass
    return jobs

def fetch_weworkremotely():
    jobs = []
    try:
        feed = feedparser.parse("https://weworkremotely.com/remote-jobs.rss")
        for entry in feed.entries:
            jobs.append({
                "title": entry.get("title", ""),
                "company": "",
                "location": "",
                "date": entry.get("published", ""),
                "url": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "source": "WeWorkRemotely"
            })
    except:
        pass
    return jobs

def fetch_workingnomads():
    jobs = []
    try:
        feed = feedparser.parse("https://www.workingnomads.co/jobs.rss")
        for entry in feed.entries:
            jobs.append({
                "title": entry.get("title", ""),
                "company": "",
                "location": "",
                "date": entry.get("published", ""),
                "url": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "source": "WorkingNomads"
            })
    except:
        pass
    return jobs

def fetch_himalayas():
    jobs = []
    try:
        res = requests.get("https://himalayas.app/jobs/api", timeout=15)
        res.raise_for_status()
        data = res.json()
        for item in data.get("jobs", []):
            company = item.get("company", {}).get("name", "") if item.get("company") else ""
            slug = item.get("slug", "")
            url = f"https://himalayas.app/jobs/{slug}" if slug else ""
            location = ", ".join(item.get("locations", [])) if item.get("locations") else ""
            jobs.append({
                "title": item.get("title", ""),
                "company": company,
                "location": location,
                "date": item.get("publishedAt", ""),
                "url": url,
                "description": item.get("description", ""),
                "source": "Himalayas"
            })
    except:
        pass
    return jobs

def fetch_arcdev():
    jobs = []
    try:
        res = requests.get("https://arc.dev/api/public/jobs", timeout=15)
        res.raise_for_status()
        data = res.json()
        for item in data.get("jobs", []):
            location = item.get("location", "")
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company", ""),
                "location": location,
                "date": item.get("posted_at", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "source": "Arc.dev"
            })
    except:
        pass
    return jobs

def fetch_jobspresso():
    jobs = []
    try:
        feed = feedparser.parse("https://jobspresso.co/remote-work/rss")
        for entry in feed.entries:
            jobs.append({
                "title": entry.get("title", ""),
                "company": "",
                "location": "",
                "date": entry.get("published", ""),
                "url": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "source": "Jobspresso"
            })
    except:
        pass
    return jobs

def fetch_skipthedrive():
    jobs = []
    try:
        feed = feedparser.parse("https://www.skipthedrive.com/feed/")
        for entry in feed.entries:
            jobs.append({
                "title": entry.get("title", ""),
                "company": "",
                "location": "",
                "date": entry.get("published", ""),
                "url": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "source": "SkipTheDrive"
            })
    except:
        pass
    return jobs

def fetch_pangian():
    jobs = []
    try:
        res = requests.get("https://pangian.com/api/jobs?per_page=100", timeout=15)
        res.raise_for_status()
        data = res.json()
        for item in data.get("jobs", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("location", ""),
                "date": item.get("published_at", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "source": "Pangian"
            })
    except:
        pass
    return jobs

def fetch_europeremotely():
    jobs = []
    try:
        res = requests.get("https://euremotejobs.com/", timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        for article in soup.select("article.job_listing"):
            title_tag = article.find("h3")
            link_tag = article.find("a", href=True)
            date_tag = article.find("time")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = link_tag["href"] if link_tag else ""
            date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else ""
            jobs.append({
                "title": title,
                "company": "",
                "location": "Europe",
                "date": date,
                "url": link,
                "description": "",
                "source": "EuropeRemotely"
            })
    except:
        pass
    return jobs

def get_all_jobs(keywords, days):
    keywords = [kw.strip().lower() for kw in keywords if kw.strip()]
    all_jobs = []
    collectors = [
        fetch_remoteok,
        fetch_remotive,
        fetch_weworkremotely,
        fetch_workingnomads,
        fetch_himalayas,
        fetch_arcdev,
        fetch_jobspresso,
        fetch_skipthedrive,
        fetch_pangian,
        fetch_europeremotely,
    ]

    for fn in collectors:
        try:
            jobs = fn()
            all_jobs.extend(jobs)
        except:
            # Ignore source errors, continue
            continue

    filtered_jobs = []
    seen_urls = set()
    for job in all_jobs:
        url = job.get("url", "")
        title = job.get("title", "")
        location = job.get("location", "")
        description = job.get("description", "")
        date = job.get("date", "")

        if not url or not title:
            continue
        if url in seen_urls:
            continue

        if not date_within_range(date, days):
            continue
        if not location_match(location, description):
            continue
        if keywords and not keyword_match(title, description, keywords):
            continue

        seen_urls.add(url)
        filtered_jobs.append({
            "Title": title,
            "Company": job.get("company", ""),
            "Location": location,
            "DatePosted": date,
            "URL": url,
            "Source": job.get("source", ""),
        })

    return filtered_jobs
