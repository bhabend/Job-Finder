from datetime import datetime, timedelta, timezone
from dateutil import parser

# Valid location keywords
VALID_LOCATIONS = [
    "india", "asia", "apac", "anywhere in the world",
    "ww", "world wide", "worldwide", "remote"
]

def keyword_match(title, description, keywords):
    """Check if any keyword is in title or description."""
    text = f"{title} {description}".lower()
    for kw in keywords:
        if kw.lower().strip() in text:
            return True
    return False

def location_match(location, description):
    """Check if job location matches allowed remote locations."""
    text = f"{location} {description}".lower()
    return any(loc in text for loc in VALID_LOCATIONS)

def date_within_range(date_str, days):
    """
    Check if job posting date is within given days.
    Tries to parse various date formats.
    """
    try:
        post_date = parser.parse(date_str, fuzzy=True)
    except Exception:
        return False

    # Make sure post_date is timezone-aware; if naive, assume UTC
    if post_date.tzinfo is None:
        post_date = post_date.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    return (now - post_date) <= timedelta(days=days)
