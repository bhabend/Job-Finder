import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Fetch from RemoteOK
def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        jobs = resp.json()[1:]  # First item is metadata
        result = []
        for job in jobs:
            result.append({
                "title": job.get("position", ""),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "posted_date": job.get("date", ""),
                "url": job.get("url", ""),
                "description": job.get("description", "")
            })
        return result
    except Exception as e:
        print(f"Error fetching RemoteOK jobs: {e}")
        return []

# Fetch from We Work Remotely
def fetch_wwr_jobs():
    url = "https://weworkremotely.com/remote-jobs"
    jobs_list = []
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = soup.find_all("li", class_="feature")
        for job in jobs:
            link = "https://weworkremotely.com" + job.find("a")["href"]
            company = job.find("span", class_="company").text.strip()
            title = job.find("span", class_="title").text.strip()
            location = job.find("span", class_="region").text.strip() if job.find("span", class_="region") else "Remote"
            jobs_list.append({
                "title": title,
                "company": company,
                "location": location,
                "posted_date": datetime.now().strftime("%Y-%m-%d"),
                "url": link,
                "description": ""
            })
        return jobs_list
    except Exception as e:
        print(f"Error fetching WWR jobs: {e}")
        return []

# Fetch from Remotive API
def fetch_remotive_jobs():
    url = "https://remotive.com/api/remote-jobs"
    try:
        resp = requests.get(url)
        jobs = resp.json().get("jobs", [])
        result = []
        for job in jobs:
            # Only keep jobs that are remote and global or in US/EU
            location_str = job.get("candidate_required_location", "").lower()
            if any(loc in location_str for loc in ["worldwide", "global", "united states", "europe", "eu"]):
                result.append({
                    "title": job.get("title", ""),
                    "company": job.get("company_name", ""),
                    "location": job.get("candidate_required_location", ""),
                    "posted_date": job.get("publication_date", ""),
                    "url": job.get("url", ""),
                    "description": job.get("description", "")
                })
        return result
    except Exception as e:
        print(f"Error fetching Remotive jobs: {e}")
        return []
