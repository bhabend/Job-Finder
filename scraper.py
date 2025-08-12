import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def scrape_remoteok():
    """Scrapes RemoteOK job listings."""
    jobs = []
    url = "https://remoteok.com/remote-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for row in soup.select("tr.job"):
            title_tag = row.select_one("h2")
            company_tag = row.select_one("h3")
            link_tag = row.select_one("a.preventLink")
            location_tag = row.select_one("div.location")

            if not (title_tag and link_tag):
                continue

            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                "link": f"https://remoteok.com{link_tag['href']}",
                "location": location_tag.get_text(strip=True) if location_tag else "Worldwide",
                "date_posted": "N/A"
            })

    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")

    return jobs


def scrape_weworkremotely():
    """Scrapes WeWorkRemotely job listings."""
    jobs = []
    url = "https://weworkremotely.com/remote-jobs/search?term="
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup
