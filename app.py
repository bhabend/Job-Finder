import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta

# Function to scrape jobs
def scrape_jobs(keywords, location, days_limit):
    base_url = "https://weworkremotely.com/remote-jobs/search"
    params = {"term": keywords, "region": location}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        st.error("Failed to fetch jobs. Please try again later.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_sections = soup.find_all("section", {"class": "jobs"})

    jobs = []
    for section in job_sections:
        for li in section.find_all("li", {"class": None}):
            title_tag = li.find("span", {"class": "title"})
            company_tag = li.find("span", {"class": "com_
