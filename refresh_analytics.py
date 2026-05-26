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


def fetch_data(property_id: str, days: int):
    client = get_client()
    end = date.today()
    start = end - timedelta(days=days - 1)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days - 1)

    start_str = start.isoformat()
    end_str = end.isoformat()
    prev_start_str = prev_start.isoformat()
    prev_end_str = prev_end.isoformat()

    print(f"Fetching {days}d: {start_str} to {end_str} (prev: {prev_start_str} to {prev_end_str})")

    # ── Active users (current + prev) ────────────────────────────────────
    r = run_report(client, property_id, start_str, end_str, ["activeUsers"])
    active_users = int(r.rows[0].metric_values[0].value) if r.rows else 0

    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["activeUsers"])
    prev_active_users = int(r_prev.rows[0].metric_values[0].value) if r_prev.rows else 0
    active_users_delta = round(pct_delta(active_users, prev_active_users))

    # ── Sessions ──────────────────────────────────────────────────────────
    r = run_report(client, property_id, start_str, end_str, ["sessions"])
    sessions = int(r.rows[0].metric_values[0].value) if r.rows else 0

    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["sessions"])
    prev_sessions = int(r_prev.rows[0].metric_values[0].value) if r_prev.rows else 0
    sessions_delta = round(pct_delta(sessions, prev_sessions))

    # ── Page views + top pages ────────────────────────────────────────────
    r = run_report(client, property_id, start_str, end_str, ["screenPageViews"], ["pagePath", "pageTitle"])
    page_views = sum(int(row.metric_values[0].value) for row in r.rows)

    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["screenPageViews"])
    prev_page_views = int(r_prev.rows[0].metric_values[0].value) if r_prev.rows else 0
    page_views_delta = round(pct_delta(page_views, prev_page_views))

    CAT_MAP = {
        "vision": "vision", "strategy": "strategy", "development": "dev",
        "discovery": "discovery", "dev": "dev", "testing": "testing",
        "uiux": "uiux", "cicd": "cicd", "marketing": "marketing",
        "sales": "sales", "operations": "operations",
    }
    top_pages = []
    for row in r.rows[:10]:
        path = row.dimension_values[0].value
        title = row.dimension_values[1].value or path
        views = int(row.metric_values[0].value)
        cat = None
        for seg in path.strip("/").split("/"):
            if seg in CAT_MAP:
                cat = CAT_MAP[seg]
                break
        top_pages.append({"path": path, "title": title, "cat": cat, "views": views})

    # ── Bounce rate + engagement metrics ──────────────────────────────────
    r = run_report(client, property_id, start_str, end_str,
                   ["bounceRate", "averageSessionDuration", "screenPageViewsPerSession"])
    bounce_rate = 0
    avg_duration_secs = 0
    pages_per_session = 0.0
    if r.rows:
        bounce_rate = round(float(r.rows[0].metric_values[0].value) * 100)
        avg_duration_secs = r.rows[0].metric_values[1].value
        pages_per_session = round(float(r.rows[0].metric_values[2].value), 2)

    r_prev = run_report(client, property_id, prev_start_str, prev_end_str,
                        ["bounceRate", "averageSessionDuration", "screenPageViewsPerSession"])
    prev_bounce_rate = 0
    prev_avg_duration_secs = 0
    prev_pages_per_session = 0.0
    if r_prev.rows:
        prev_bounce_rate = round(float(r_prev.rows[0].metric_values[0].value) * 100)
        prev_avg_duration_secs = r_prev.rows[0].metric_values[1].value
        prev_pages_per_session = round(float(r_prev.rows[0].metric_values[2].value), 2)

    bounce_rate_delta = round(bounce_rate - prev_bounce_rate)
    avg_duration_delta_secs = round(float(avg_duration_secs) - float(prev_avg_duration_secs))
    pages_per_session_delta = round(pages_per_session - prev_pages_per_session, 1)

    # ── New vs Returning ──────────────────────────────────────────────────
    r = run_report(client, property_id, start_str, end_str, ["activeUsers"], ["newVsReturning"])
    r_prev = run_report(client, property_id, prev_start_str, prev_end_str, ["activeUsers"], ["newVsReturning"])

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

    new_pct, ret_pct = parse_new_returning(r)
    prev_new_pct, _ = parse_new_returning(r_prev)

    # ── Countries ─────────────────────────────────────────────────────────
    FLAG = {
        "United States": "🇺🇸", "Ireland": "🇮🇪", "United Kingdom": "🇬🇧",
        "Canada": "🇨🇦", "Australia": "🇦🇺", "India": "🇮🇳", "Germany": "🇩🇪",
        "France": "🇫🇷", "Netherlands": "🇳🇱", "Singapore": "🇸🇬",
        "New Zealand": "🇳🇿", "Brazil": "🇧🇷", "Spain": "🇪🇸", "Sweden": "🇸🇪",
        "Norway": "🇳🇴", "Denmark": "🇩🇰", "Finland": "🇫🇮", "Poland": "🇵🇱",
        "Japan": "🇯🇵", "South Korea": "🇰🇷",
    }
    r = run_report(client, property_id, start_str, end_str, ["activeUsers"], ["country"])
    total_country_users = sum(int(row.metric_values[0].value) for row in r.rows)
    countries = []
    other_users = 0
    for row in r.rows[:5]:
        country = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        pct = round(users / total_country_users * 100, 1) if total_country_users else 0
        countries.append({
            "flag": FLAG.get(country, "🌐"),
            "country": country,
            "users": users,
            "percent": pct,
        })
        other_users += users
    if len(r.rows) > 5:
        other = total_country_users - other_users
        if other > 0:
            countries.append({
                "flag": "🌐",
                "country": "Other",
                "users": other,
                "percent": round(other / total_country_users * 100, 1),
            })

    # ── Events ────────────────────────────────────────────────────────────
    r = run_report(client, property_id, start_str, end_str, ["eventCount"], ["eventName"])
    events = []
    newsletter_clicks = 0
    share_x_clicks = 0
    for row in r.rows:
        name = row.dimension_values[0].value
        count = int(row.metric_values[0].value)
        events.append({"name": name, "count": count})
        if name == "newsletter_click":
            newsletter_clicks = count
        if name == "share_x":
            share_x_clicks = count

    # ── KR current values ─────────────────────────────────────────────────
    kr_current_values = {
        "kr1": active_users,
        "kr2": bounce_rate,
    }

    # ── Assemble ──────────────────────────────────────────────────────────
    range_label = f"{days}d"
    refreshed = date.today().strftime("%a %-d %b %Y") + f" · {__import__('datetime').datetime.now().strftime('%H:%M')}"

    return {
        "refreshed": refreshed,
        "range": range_label,
        "stats": {
            "activeUsers": active_users,
            "activeUsersDelta": active_users_delta,
            "sessions": sessions,
            "sessionsDelta": sessions_delta,
            "pageViews": page_views,
            "pageViewsDelta": page_views_delta,
            "bounceRate": bounce_rate,
            "bounceRateDelta": bounce_rate_delta,
        },
        "topPages": top_pages,
        "engagement": {
            "avgSessionDuration": parse_duration_secs(avg_duration_secs),
            "avgSessionDurationDeltaSecs": avg_duration_delta_secs,
            "pagesPerSession": pages_per_session,
            "pagesPerSessionDelta": pages_per_session_delta,
            "newUsersPercent": new_pct,
            "returningUsersPercent": ret_pct,
            "newUsersPrevPercent": prev_new_pct,
            "newsletterClicks": newsletter_clicks,
            "shareXClicks": share_x_clicks,
        },
        "countries": countries,
        "events": events,
        "krCurrentValues": kr_current_values,
    }


def build_data_block(data: dict) -> str:
    """Render the ANALYTICS_DATA:BEGIN…END block."""
    def js_val(v):
        if isinstance(v, str):
            return json.dumps(v)
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        return json.dumps(v)

    s = data["stats"]
    e = data["engagement"]
    pages_js = ",\n    ".join(
        f'{{ path: {json.dumps(p["path"])}, title: {json.dumps(p["title"])}, cat: {json.dumps(p["cat"])}, views: {p["views"]} }}'
        for p in data["topPages"]
    )
    countries_js = ",\n    ".join(
        f'{{ flag: {json.dumps(c["flag"])}, country: {json.dumps(c["country"])}, users: {c["users"]}, percent: {c["percent"]} }}'
        for c in data["countries"]
    )
    events_js = ",\n    ".join(
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
