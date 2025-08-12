from datetime import datetime, timedelta

def filter_jobs(jobs, keywords=None, days=7, location_keyword=None):
    """
    Filters jobs based on keywords, posting date, and location.
    """

    filtered = []
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    for job in jobs:
        title_match = True
        date_match = True
        location_match = True

        # Keyword filter
        if keywords:
            title_match = any(
                kw.lower() in job["title"].lower()
                for kw in keywords
            )

        # Date filter
        if "date_posted" in job and job["date_posted"]:
            try:
                job_date = datetime.strptime(job["date_posted"], "%Y-%m-%d")
                date_match = job_date >= cutoff_date
            except ValueError:
                pass

        # Location filter
        if location_keyword:
            loc = job.get("location", "").lower()
            loc_keyword = location_keyword.lower()

            worldwide_terms = ["worldwide", "anywhere", "remote - global", "global", "multiple locations"]

            # Match if location contains keyword OR is a worldwide term
            location_match = (
                loc_keyword in loc
                or any(term in loc for term in worldwide_terms)
            )

        if title_match and date_match and location_match:
            filtered.append(job)

    return filtered
