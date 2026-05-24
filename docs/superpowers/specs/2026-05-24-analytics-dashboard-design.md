# Analytics Dashboard — Design Spec
**Date:** 2026-05-24  
**Status:** Approved

---

## Overview

A local `analytics.html` file that Gerald opens in a browser to see Product Genesis site performance. Claude fetches all data from Google Analytics via the GA MCP tools and bakes it inline as JavaScript each time Gerald asks for a refresh. No build step, no server dependency, no published page — it only lives on Gerald's machine.

---

## Architecture

**Single self-contained file:** `analytics.html` at the project root (alongside `index.html`).

Data flow:
1. Gerald tells Claude: *"refresh the analytics dashboard"*
2. Claude calls the GA MCP tools (getActiveUsers, getPageViews, getUserBehavior, getEvents, runReport) for the selected period
3. Claude writes the fetched data as inline `<script>` JavaScript into `analytics.html`
4. Gerald opens / refreshes `analytics.html` in the browser — no network calls required

The OKR data (objectives, key results, steps) is also stored inline in the HTML, edited by telling Claude. Gerald does not need to touch the file directly.

**Design system:** Matches Product Genesis exactly — same CSS custom properties (--accent, --ink, --bg-*, --rule), Poppins + JetBrains Mono, same border-radius/spacing conventions.

---

## Date Range Toggle

Three buttons at top-right of the header: **7d | 28d | 90d**.  
Default: 28d.  
Switching range triggers Claude to re-fetch and rewrite the file for that period (it does not do a live client-side fetch — the toggle is a signal to Gerald about what to ask Claude for next).  
The active range is visually indicated with an accent-filled button.

---

## Sections

### 1. Header
- Site name label ("Product Genesis") in mono uppercase
- Page title: "Site Analytics"
- Last refreshed timestamp (written by Claude at refresh time)
- Date range toggle (7d / 28d / 90d)

---

### 2. OKR Section

Appears above all metrics. One card per objective (typically one active at a time).

**Objective row:**
- Emoji icon + label showing quarter (e.g., "Q2 2026") + objective text
- "+ Add Objective" button (tells Gerald to ask Claude to add one)

**Key Result rows** (inside the same card, below the objective):

Each KR has:
| Field | Detail |
|---|---|
| Number | Sequential (1, 2, 3…) |
| Description | Plain-language target statement |
| Metric tag | Pill showing which GA metric is tracked (e.g., "Active Users", "Bounce Rate", "newsletter_click") |
| Current value | Auto-filled from GA at refresh time |
| Target value | Set by Gerald when defining the KR |
| Progress bar | Current / target, colour-coded (blue standard, amber for rate metrics going down) |
| Target date | Date chip (e.g., "30 Jun 2026") |
| Confidence | Badge: **High** (green) / **Med** (amber) / **Low** (red) |
| Steps button | ▶ icon, expands inline steps panel |

**Steps panel** (inline accordion below the KR row):

- Sequential numbered steps connected by a vertical timeline line
- Each step: title, description (1–2 sentences), due date
- Step states: done (green ✓), active (blue number), pending (grey)
- Steps are defined by Gerald and stored in the HTML; Claude updates them on request

OKR data persists in the HTML between refreshes — Claude only overwrites the metric values (current value on each KR), not the OKR structure itself, unless Gerald explicitly asks for a change.

---

### 3. Stat Cards (4-up grid)

| Card | Metric | Source |
|---|---|---|
| Active Users | `activeUsers` | getActiveUsers |
| Sessions | `sessions` | runReport (metric: sessions) |
| Page Views | `screenPageViews` | getPageViews |
| Bounce Rate | `bounceRate` | getUserBehavior |

Each card shows: current value, period-over-period delta (↑/↓ with % or pp), mini progress bar.  
Delta colour: green = improvement, red = regression, amber = neutral (bounce rate inverted — down is good).

---

### 4. Top Pages (panel, left column)

Fetched via `getPageViews` with `pagePath` dimension.  
Shows top 6–8 pages by views.  
Each row: page title, category pill (matched from data.js post titles), inline bar, view count.

---

### 5. Engagement (panel, right column)

| Metric | Source |
|---|---|
| Avg Session Duration | getUserBehavior |
| Pages / Session | getUserBehavior (screenPageViewsPerSession) |
| New vs Returning | runReport with `newVsReturning` dimension |
| Newsletter Clicks | getEvents, filter `newsletter_click` |
| X Share Clicks | getEvents, filter `share_x` |

---

### 6. Traffic by Country (panel, left column)

Fetched via `runReport` with `country` dimension + `activeUsers` metric.  
Top 5 countries + "Other" remainder.  
Each row: flag emoji, country name, inline bar, user count, percentage.

---

### 7. Top Events (panel, right column)

Fetched via `getEvents`.  
Shows top 7 events by count.  
Each row: event name (mono), count (accent colour).

---

### 8. Footer

Single line: `Product Genesis · Analytics · Data from Google Analytics 4 · Refreshed by Claude`

---

## Refresh Workflow

When Gerald says *"refresh the analytics dashboard"* (or specifies a period like *"refresh for the last 7 days"*):

1. Claude determines the date range (today minus N days)
2. Calls all five GA MCP tools in parallel
3. Rewrites `analytics.html` with fresh inline data
4. Reports back: "Dashboard refreshed — X active users, Y sessions, Z page views over the last N days."

Claude does **not** overwrite OKR structure, confidence levels, steps, or target values during a refresh — only the `currentValue` field on each KR and the metric sections.

---

## OKR Edit Workflow

Gerald edits OKRs by telling Claude in plain English:
- *"Add a key result: 200 X share clicks by end of June, high confidence"*
- *"Add a step to KR 2: write 3 SEO posts targeting long-tail queries, due 15 June"*
- *"Mark step 1 of KR 1 as done"*
- *"Change confidence on KR 3 to medium"*

Claude reads the current `analytics.html`, applies the change, and rewrites the file.

---

## File Location

```
analytics.html   ← project root, alongside index.html
```

Not linked from the main site nav. Not published to GitHub Pages — add `analytics.html` to `.gitignore` since it contains live traffic data and will be overwritten locally on each refresh.

---

## Out of Scope

- Live client-side GA API calls (requires API key in browser — security risk)
- Chart.js trend lines (deferred until months of historical data exist)
- Multi-objective support (one active objective is enough for now)
- Auth / password protection (local file only)
