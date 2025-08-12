import streamlit as st
import requests
from bs4 import BeautifulSoup

# ----------------------------
# Job fetching logic
# ----------------------------
def fetch_jobs(keyword, location):
    url = "https://weworkremotely.com/remote-jobs/search"
    params = {"term": keyword, "region": location}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    for job_section in soup.find_all("section", class_="jobs"):
        for job in job_section.find_all("li", class_="feature"):  
            title_tag = job.find("span", class_="title")
            company_tag = job.find("span", class_="company")
            date_tag = job.find("time")

            link_tag = job.find("a", href=True)
            job_link = "https://weworkremotely.com" + link_tag["href"] if link_tag else None

            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            company = company_tag.get_text(strip=True) if company_tag else "N/A"
            post_date = date_tag["datetime"] if date_tag and "datetime" in date_tag.attrs else "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "link": job_link,
                "date": post_date
            })

    return jobs

# --------------------------
