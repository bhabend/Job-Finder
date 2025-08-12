import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# -------------------------------
# Function to fetch jobs from Crossover
# -------------------------------
def fetch_jobs():
    url = "https://www.crossover.com/job-roles"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "lxml")
    jobs = []

    for card in soup.find_all("a", class_="job-card"):
        title_tag = card.find("h3")
        location_tag = card.find("span", class_="location")
        date_tag = card.find("time")

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        location = location_tag.get_text(strip=True) if location_tag else "No location"
        post_date = date_tag["datetime"] if date_tag and date_tag.has_attr("datetime"_
