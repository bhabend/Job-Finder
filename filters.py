from datetime import datetime, timedelta

def filter_jobs(jobs, keywords, days, location_keyword):
    filtered = []
    allowed_terms = ["remote", "worldwide", "world wide", "global", "work from anywhere", location_keyword.lower()]
    cutoff_date = datetime.now() - timedelta(days=days)

    for job in jobs:
        title = job["title"].lower()
        desc = job["description"].lower() if job.get("description") else ""
        loc = job["location"].lower()
        date_str = job["posted_date"]
        
        # Parse date safely
        try:
            job_date = datetime.fromisoformat(date_str.replace("Z", ""))
        except:
            try:
                job_date = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                job_date = datetime.now()

        # Keyword filter
        if not any(k.lower() in title or k.lower() in desc for k in keywords):
            continue

        # Date filter
        if job_date < cutoff_date:
            continue

        # Location filter
        if not any(term in loc or term in desc for term in allowed_terms):
            continue

        filtered.append(job)

    return filtered
