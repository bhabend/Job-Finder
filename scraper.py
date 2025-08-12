import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

def fetch_wwr_jobs():
    url = "https://weworkremotely.com/categories/remote-programming-jobs"
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
