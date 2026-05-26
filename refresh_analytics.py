#!/usr/bin/env python3
"""
refresh_analytics.py — Fetches live GA4 data and writes it into analytics.html.

Usage:
    python refresh_analytics.py           # last 28 days (default)
    python refresh_analytics.py --days 7  # last 7 days
    python refresh_analytics.py --days 90 # last 90 days

Requirements:
    pip install google-analytics-data

Credentials:
    Set GA_CREDENTIALS env var to path of service account JSON, or place it at:
    C:/Users/geral/Downloads/product-genesis-analytics-04aee6013029.json

Property:
    Set GA_PROPERTY_ID env var to your numeric GA4 property ID, or edit
    PROPERTY_ID below.
"""

import os
import re
import sys
import json
import argparse
from datetime import date, timedelta

PROPERTY_ID = os.environ.get("GA_PROPERTY_ID", "160712637")
CLIENT_SECRETS_PATH = "C:/Users/geral/Downloads/client_secret_153256688942-fp087vrv067kd0npauh7voqkk4877bov.apps.googleusercontent.com.json"
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "ga_token.json")
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
ANALYTICS_HTML = os.path.join(os.path.dirname(__file__), "analytics.html")


def get_client():
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return BetaAnalyticsDataClient(credentials=creds)


def run_report(client, property_id, start, end, metrics, dimensions=None):
    from google.analytics.data_v1beta.types import (
        RunReportRequest, Metric, Dimension, DateRange,
    )
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in (dimensions or [])],
        limit=20,
    )
    return client.run_report(req)


def parse_duration_secs(avg_secs):
    """Convert average session duration in seconds to M:SS string."""
    try:
        s = int(float(avg_secs))
        return f"{s // 60}:{s % 60:02d}"
    except Exception:
        return "—"


def pct_delta(curr, prev):
    """Percentage change rounded to 1dp."""
    try:
        if prev == 0:
            return 0
        return round((curr - prev) / prev * 100, 1)
    except Exception:
        return 0


CAT_MAP = {
    "vision": "vision", "strategy": "strategy", "development": "dev",
    "discovery": "discovery", "dev": "dev", "testing": "testing",
    "uiux": "uiux", "cicd": "cicd", "marketing": "marketing",
    "sales": "sales", "operations": "operations",
}

FLAG = {
    "United States": "🇺🇸", "Ireland": "🇮🇪", "United Kingdom": "🇬🇧",
    "Canada": "🇨🇦", "Australia": "🇦🇺", "India": "🇮🇳", "Germany": "🇩🇪",
    "France": "🇫🇷", "Netherlands": "🇳🇱", "Singapore": "🇸🇬",
    "New Zealand": "🇳🇿", "Brazil": "🇧🇷", "Spain": "🇪🇸", "Sweden": "🇸🇪",
    "Norway": "🇳🇴", "Denmark": "🇩🇰", "Finland": "🇫🇮", "Poland": "🇵🇱",
    "Japan": "🇯🇵", "South Korea": "🇰🇷",
}


def parse_new_returning(result):
    new_u, ret_u = 0, 0
    for row in result.rows:
        val = int(row.metric_values[0].value)
        if row.dimension_values[0].value == "new":
            new_u = val
        else:
            ret_u = val
    total = new_u + ret_u or 1
    return round(new_u / total * 100), round(ret_u / total * 100)


def fetch_user_session_stats(client, property_id, start_str, end_str, prev_start_str, prev_end_str):
    r = run_report(client, property_id, start_str, end_str, ["activeUsers"])
    active_users = int(r.rows[0].metric_values[0].value) if r.rows else 0
    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["activeUsers"])
    prev_active_users = int(r_prev.rows[0].metric_values[0].value) if r_prev.rows else 0

    r = run_report(client, property_id, start_str, end_str, ["sessions"])
    sessions = int(r.rows[0].metric_values[0].value) if r.rows else 0
    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["sessions"])
    prev_sessions = int(r_prev.rows[0].metric_values[0].value) if r_prev.rows else 0

    return {
        "activeUsers": active_users,
        "activeUsersDelta": round(pct_delta(active_users, prev_active_users)),
        "sessions": sessions,
        "sessionsDelta": round(pct_delta(sessions, prev_sessions)),
    }


def fetch_page_views(client, property_id, start_str, end_str, prev_start_str, prev_end_str):
    r = run_report(client, property_id, start_str, end_str, ["screenPageViews"], ["pagePath", "pageTitle"])
    page_views = sum(int(row.metric_values[0].value) for row in r.rows)
    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["screenPageViews"])
    prev_page_views = int(r_prev.rows[0].metric_values[0].value) if r_prev.rows else 0

    top_pages = []
    for row in r.rows[:10]:
        path = row.dimension_values[0].value
        title = row.dimension_values[1].value or path
        views = int(row.metric_values[0].value)
        cat = next((CAT_MAP[seg] for seg in path.strip("/").split("/") if seg in CAT_MAP), None)
        top_pages.append({"path": path, "title": title, "cat": cat, "views": views})

    return page_views, round(pct_delta(page_views, prev_page_views)), top_pages


def fetch_engagement(client, property_id, start_str, end_str, prev_start_str, prev_end_str):
    metrics = ["bounceRate", "averageSessionDuration", "screenPageViewsPerSession"]
    r = run_report(client, property_id, start_str, end_str, metrics)
    bounce_rate, avg_duration_secs, pages_per_session = 0, 0, 0.0
    if r.rows:
        bounce_rate = round(float(r.rows[0].metric_values[0].value) * 100)
        avg_duration_secs = r.rows[0].metric_values[1].value
        pages_per_session = round(float(r.rows[0].metric_values[2].value), 2)

    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, metrics)
    prev_bounce_rate, prev_avg_duration_secs, prev_pages_per_session = 0, 0, 0.0
    if r_prev.rows:
        prev_bounce_rate = round(float(r_prev.rows[0].metric_values[0].value) * 100)
        prev_avg_duration_secs = r_prev.rows[0].metric_values[1].value
        prev_pages_per_session = round(float(r_prev.rows[0].metric_values[2].value), 2)

    return {
        "bounceRate": bounce_rate,
        "bounceRateDelta": round(bounce_rate - prev_bounce_rate),
        "avgSessionDuration": parse_duration_secs(avg_duration_secs),
        "avgSessionDurationDeltaSecs": round(float(avg_duration_secs) - float(prev_avg_duration_secs)),
        "pagesPerSession": pages_per_session,
        "pagesPerSessionDelta": round(pages_per_session - prev_pages_per_session, 1),
    }


def fetch_new_returning(client, property_id, start_str, end_str, prev_start_str, prev_end_str):
    r = run_report(client, property_id, start_str, end_str, ["activeUsers"], ["newVsReturning"])
    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["activeUsers"], ["newVsReturning"])
    new_pct, ret_pct = parse_new_returning(r)
    prev_new_pct, _ = parse_new_returning(r_prev)
    return new_pct, ret_pct, prev_new_pct


def fetch_countries(client, property_id, start_str, end_str):
    r = run_report(client, property_id, start_str, end_str, ["activeUsers"], ["country"])
    total = sum(int(row.metric_values[0].value) for row in r.rows)
    countries = []
    top_users = 0
    for row in r.rows[:5]:
        country = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        pct = round(users / total * 100, 1) if total else 0
        countries.append({"flag": FLAG.get(country, "🌐"), "country": country, "users": users, "percent": pct})
        top_users += users
    if len(r.rows) > 5:
        other = total - top_users
        if other > 0:
            countries.append({"flag": "🌐", "country": "Other", "users": other,
                               "percent": round(other / total * 100, 1)})
    return countries


def fetch_events(client, property_id, start_str, end_str):
    r = run_report(client, property_id, start_str, end_str, ["eventCount"], ["eventName"])
    events, newsletter_clicks, share_x_clicks = [], 0, 0
    for row in r.rows:
        name = row.dimension_values[0].value
        count = int(row.metric_values[0].value)
        events.append({"name": name, "count": count})
        if name == "newsletter_click":
            newsletter_clicks = count
        if name == "share_x":
            share_x_clicks = count
    return events, newsletter_clicks, share_x_clicks


def fetch_data(property_id: str, days: int):
    import datetime as _dt
    client = get_client()
    end = date.today()
    start = end - timedelta(days=days - 1)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days - 1)

    start_str, end_str = start.isoformat(), end.isoformat()
    prev_start_str, prev_end_str = prev_start.isoformat(), prev_end.isoformat()
    print(f"Fetching {days}d: {start_str} to {end_str} (prev: {prev_start_str} to {prev_end_str})")

    user_stats = fetch_user_session_stats(client, property_id, start_str, end_str, prev_start_str, prev_end_str)
    page_views, page_views_delta, top_pages = fetch_page_views(client, property_id, start_str, end_str, prev_start_str, prev_end_str)
    eng = fetch_engagement(client, property_id, start_str, end_str, prev_start_str, prev_end_str)
    new_pct, ret_pct, prev_new_pct = fetch_new_returning(client, property_id, start_str, end_str, prev_start_str, prev_end_str)
    countries = fetch_countries(client, property_id, start_str, end_str)
    events, newsletter_clicks, share_x_clicks = fetch_events(client, property_id, start_str, end_str)

    refreshed = date.today().strftime("%a %-d %b %Y") + f" · {_dt.datetime.now().strftime('%H:%M')}"
    return {
        "refreshed": refreshed,
        "range": f"{days}d",
        "stats": {
            "activeUsers": user_stats["activeUsers"],
            "activeUsersDelta": user_stats["activeUsersDelta"],
            "sessions": user_stats["sessions"],
            "sessionsDelta": user_stats["sessionsDelta"],
            "pageViews": page_views,
            "pageViewsDelta": page_views_delta,
            "bounceRate": eng["bounceRate"],
            "bounceRateDelta": eng["bounceRateDelta"],
        },
        "topPages": top_pages,
        "engagement": {
            "avgSessionDuration": eng["avgSessionDuration"],
            "avgSessionDurationDeltaSecs": eng["avgSessionDurationDeltaSecs"],
            "pagesPerSession": eng["pagesPerSession"],
            "pagesPerSessionDelta": eng["pagesPerSessionDelta"],
            "newUsersPercent": new_pct,
            "returningUsersPercent": ret_pct,
            "newUsersPrevPercent": prev_new_pct,
            "newsletterClicks": newsletter_clicks,
            "shareXClicks": share_x_clicks,
        },
        "countries": countries,
        "events": events,
        "krCurrentValues": {"kr1": user_stats["activeUsers"], "kr2": eng["bounceRate"]},
    }


_JS_JOIN = ",\n    "


def build_data_block(data: dict) -> str:
    """Render the ANALYTICS_DATA:BEGIN…END block."""
    s = data["stats"]
    e = data["engagement"]
    pages_js = _JS_JOIN.join(
        f'{{ path: {json.dumps(p["path"])}, title: {json.dumps(p["title"])}, cat: {json.dumps(p["cat"])}, views: {p["views"]} }}'
        for p in data["topPages"]
    )
    countries_js = _JS_JOIN.join(
        f'{{ flag: {json.dumps(c["flag"])}, country: {json.dumps(c["country"])}, users: {c["users"]}, percent: {c["percent"]} }}'
        for c in data["countries"]
    )
    events_js = _JS_JOIN.join(
        f'{{ name: {json.dumps(ev["name"])}, count: {ev["count"]} }}'
        for ev in data["events"]
    )
    kr_js = ", ".join(f'"{k}": {v}' for k, v in data["krCurrentValues"].items())

    return f"""<!-- ANALYTICS_DATA:BEGIN -->
<script>
const ANALYTICS_DATA = {{
  refreshed: {json.dumps(data["refreshed"])},
  range: {json.dumps(data["range"])},
  stats: {{
    activeUsers: {s["activeUsers"]}, activeUsersDelta: {s["activeUsersDelta"]},
    sessions: {s["sessions"]},    sessionsDelta: {s["sessionsDelta"]},
    pageViews: {s["pageViews"]},   pageViewsDelta: {s["pageViewsDelta"]},
    bounceRate: {s["bounceRate"]},  bounceRateDelta: {s["bounceRateDelta"]},
  }},
  topPages: [
    {pages_js},
  ],
  engagement: {{
    avgSessionDuration: {json.dumps(e["avgSessionDuration"])}, avgSessionDurationDeltaSecs: {e["avgSessionDurationDeltaSecs"]},
    pagesPerSession: {e["pagesPerSession"]},      pagesPerSessionDelta: {e["pagesPerSessionDelta"]},
    newUsersPercent: {e["newUsersPercent"]},        returningUsersPercent: {e["returningUsersPercent"]},
    newUsersPrevPercent: {e["newUsersPrevPercent"]},
    newsletterClicks: {e["newsletterClicks"]},
    shareXClicks: {e["shareXClicks"]},
  }},
  countries: [
    {countries_js},
  ],
  events: [
    {events_js},
  ],
  krCurrentValues: {{ {kr_js} }},
}};
</script>
<!-- ANALYTICS_DATA:END -->"""


def update_html(data: dict):
    with open(ANALYTICS_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    new_block = build_data_block(data)
    updated = re.sub(
        r"<!-- ANALYTICS_DATA:BEGIN -->.*?<!-- ANALYTICS_DATA:END -->",
        new_block,
        html,
        flags=re.DOTALL,
    )
    if updated == html:
        print("WARNING: markers not found — analytics.html was not updated.")
        return

    with open(ANALYTICS_HTML, "w", encoding="utf-8") as f:
        f.write(updated)

    s = data["stats"]
    print(
        f"\nDashboard refreshed — {s['activeUsers']:,} active users, "
        f"{s['sessions']:,} sessions, {s['pageViews']:,} page views "
        f"over the last {data['range']}."
    )


def main():
    parser = argparse.ArgumentParser(description="Refresh Product Genesis analytics dashboard")
    parser.add_argument("--days", type=int, default=28, choices=[7, 28, 90],
                        help="Date range in days (default: 28)")
    parser.add_argument("--property", type=str, default=PROPERTY_ID,
                        help="GA4 numeric property ID (overrides PROPERTY_ID in script)")
    args = parser.parse_args()

    property_id = args.property
    if not property_id:
        print("ERROR: GA4 property ID not set.")
        print("  Set it in the script (PROPERTY_ID = '...') or pass --property 123456789")
        sys.exit(1)

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient  # noqa: F401
    except ImportError:
        print("ERROR: google-analytics-data not installed.")
        print("  Run: pip install google-analytics-data")
        sys.exit(1)

    data = fetch_data(property_id, args.days)
    update_html(data)


if __name__ == "__main__":
    main()
