# Analytics Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a self-contained `analytics.html` dashboard that Claude populates with Google Analytics data and OKRs on demand, matching the Product Genesis design system.

**Architecture:** Single HTML file at project root with two inline `<script>` data blocks — `ANALYTICS_DATA` (Claude rewrites on refresh) and `OKR_DATA` (Claude edits on request). Vanilla JS render functions build the DOM from those objects on page load. No framework, no build step, no network calls from the browser.

**Tech Stack:** HTML5, CSS custom properties (matching Product Genesis), vanilla JavaScript (ES2020 template literals + DOM API), Google Fonts (Poppins + JetBrains Mono via CDN).

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `analytics.html` | Create | Full dashboard: CSS, data blocks, render engine |
| `.gitignore` | Modify | Exclude analytics.html from git |

---

### Task 1: Scaffold analytics.html — head, CSS, shell

**Files:**
- Create: `analytics.html`

- [ ] **Step 1: Create the file with HTML shell, Google Fonts, and complete CSS**

Create `analytics.html` at the project root with this exact content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Product Genesis — Analytics</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<style>
:root {
  --bg:          #ffffff;
  --bg-2:        #f3f6fb;
  --bg-3:        #e4ecf6;
  --ink:         #14244C;
  --ink-soft:    rgba(20,36,76,.70);
  --ink-mute:    rgba(20,36,76,.46);
  --rule:        rgba(20,36,76,.14);
  --accent:      #4A95D0;
  --accent-soft: rgba(74,149,208,.14);
  --card:        #ffffff;
  --radius:      14px;
  --mono:        "JetBrains Mono", monospace;
  --sans:        "Poppins", sans-serif;
  --green:       #22c55e;
  --green-soft:  rgba(34,197,94,.12);
  --red:         #ef4444;
  --amber:       #f59e0b;
  --amber-soft:  rgba(245,158,11,.12);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--sans); background: var(--bg-2); color: var(--ink); min-height: 100vh; }
.page { max-width: 1100px; margin: 0 auto; padding: 32px 24px 64px; }

/* Header */
.dash-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 28px; gap: 16px; flex-wrap: wrap; }
.dash-site { font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--ink-mute); font-family: var(--mono); margin-bottom: 4px; }
.dash-heading { font-size: 26px; font-weight: 700; line-height: 1.1; }
.dash-updated { font-size: 11px; color: var(--ink-mute); font-family: var(--mono); margin-top: 4px; }
.range-toggle { display: flex; background: var(--bg-3); border-radius: 9px; padding: 3px; gap: 2px; }
.range-btn { font-family: var(--mono); font-size: 11px; font-weight: 500; padding: 6px 14px; border-radius: 7px; border: none; cursor: pointer; background: transparent; color: var(--ink-mute); }
.range-btn.active { background: var(--accent); color: #fff; }

/* Panels */
.panel { background: var(--card); border-radius: var(--radius); border: 1px solid var(--rule); overflow: hidden; }
.panel-head { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px 14px; border-bottom: 1px solid var(--rule); }
.panel-title { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .09em; color: var(--ink-mute); font-family: var(--mono); }

/* Layout */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
.section-gap { margin-bottom: 20px; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
.stat-card { background: var(--card); border-radius: var(--radius); padding: 20px 22px 18px; border: 1px solid var(--rule); }
.stat-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; color: var(--ink-mute); font-family: var(--mono); margin-bottom: 8px; }
.stat-value { font-size: 30px; font-weight: 700; line-height: 1; margin-bottom: 8px; font-family: var(--mono); }
.stat-delta { font-size: 11px; font-family: var(--mono); font-weight: 500; }
.delta-up { color: var(--green); }
.delta-down { color: var(--red); }
.delta-neutral { color: var(--ink-mute); }
.stat-bar { height: 3px; background: var(--bg-3); border-radius: 2px; margin-top: 14px; overflow: hidden; }
.stat-bar-fill { height: 100%; border-radius: 2px; }

/* OKR section */
.okr-section { background: var(--card); border-radius: var(--radius); border: 1px solid var(--rule); margin-bottom: 20px; overflow: hidden; }
.okr-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 22px 16px; border-bottom: 1px solid var(--rule); gap: 12px; }
.okr-badge { font-family: var(--mono); font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; background: var(--accent); color: #fff; padding: 3px 9px; border-radius: 5px; }
.okr-section-title { font-size: 13px; font-weight: 600; }
.okr-add-btn { font-family: var(--mono); font-size: 11px; font-weight: 600; color: var(--accent); background: var(--accent-soft); border: none; border-radius: 7px; padding: 6px 13px; cursor: default; opacity: .7; }
.objective-row { display: flex; align-items: center; gap: 14px; padding: 16px 22px; border-bottom: 1px solid var(--rule); background: var(--bg-2); }
.obj-icon { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, var(--accent), #14244C); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
.obj-label { font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; color: var(--ink-mute); font-family: var(--mono); margin-bottom: 3px; }
.obj-text { font-size: 15px; font-weight: 600; }
.kr-list { list-style: none; }
.kr-item { border-bottom: 1px solid var(--rule); }
.kr-item:last-child { border-bottom: none; }
.kr-row { display: grid; grid-template-columns: 24px 1fr auto auto auto; align-items: center; gap: 14px; padding: 14px 22px; }
.kr-num { font-family: var(--mono); font-size: 11px; font-weight: 700; color: var(--ink-mute); text-align: center; }
.kr-main { min-width: 0; }
.kr-description { font-size: 13px; font-weight: 500; margin-bottom: 6px; }
.kr-metric-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.kr-metric-tag { font-family: var(--mono); font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; background: var(--accent-soft); color: var(--accent); padding: 2px 8px; border-radius: 4px; }
.kr-progress-wrap { flex: 1; min-width: 80px; max-width: 160px; }
.kr-progress-track { height: 5px; background: var(--bg-3); border-radius: 3px; overflow: hidden; }
.kr-progress-fill { height: 100%; border-radius: 3px; }
.kr-values { font-family: var(--mono); font-size: 11px; color: var(--ink-mute); margin-top: 2px; }
.kr-values strong { color: var(--ink); font-weight: 600; }
.kr-date-chip { font-family: var(--mono); font-size: 10px; font-weight: 500; color: var(--ink-soft); background: var(--bg-2); border: 1px solid var(--rule); border-radius: 6px; padding: 4px 10px; white-space: nowrap; }
.confidence-chip { font-family: var(--mono); font-size: 10px; font-weight: 700; border-radius: 6px; padding: 4px 10px; white-space: nowrap; }
.conf-high { background: var(--green-soft); color: var(--green); }
.conf-med  { background: var(--amber-soft); color: var(--amber); }
.conf-low  { background: rgba(239,68,68,.1); color: var(--red); }
.steps-btn { width: 32px; height: 32px; border-radius: 8px; background: var(--bg-3); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; color: var(--ink-mute); font-size: 14px; flex-shrink: 0; }
.steps-btn.open { background: var(--accent); color: #fff; }
.steps-panel { display: none; padding: 0 22px 18px 60px; }
.steps-panel.open { display: block; }
.steps-list { list-style: none; position: relative; }
.steps-list::before { content: ''; position: absolute; left: 13px; top: 8px; bottom: 8px; width: 2px; background: var(--rule); }
.step-item { display: flex; gap: 14px; align-items: flex-start; padding: 6px 0; }
.step-dot { width: 28px; height: 28px; border-radius: 50%; background: var(--bg-2); border: 2px solid var(--rule); display: flex; align-items: center; justify-content: center; font-family: var(--mono); font-size: 10px; font-weight: 700; color: var(--ink-mute); flex-shrink: 0; position: relative; z-index: 1; }
.step-dot.done { background: var(--green); border-color: var(--green); color: #fff; }
.step-dot.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.step-content { padding-top: 4px; }
.step-title { font-size: 12px; font-weight: 600; margin-bottom: 2px; }
.step-desc { font-size: 11px; color: var(--ink-mute); line-height: 1.4; margin-bottom: 4px; }
.step-date { font-family: var(--mono); font-size: 10px; color: var(--accent); font-weight: 500; }

/* Top pages */
.pages-table { width: 100%; border-collapse: collapse; }
.pages-table tr { border-bottom: 1px solid var(--rule); }
.pages-table tr:last-child { border-bottom: none; }
.pages-table td { padding: 11px 20px; font-size: 13px; vertical-align: middle; }
.pages-table td:last-child { text-align: right; font-family: var(--mono); font-size: 12px; font-weight: 500; color: var(--ink-soft); }
.page-bar-cell { width: 80px; padding-right: 12px !important; }
.page-mini-bar { height: 4px; background: var(--bg-3); border-radius: 2px; overflow: hidden; }
.page-mini-bar-fill { height: 100%; background: var(--accent); border-radius: 2px; opacity: .65; }
.page-cat-pill { display: inline-block; font-family: var(--mono); font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; padding: 2px 7px; border-radius: 4px; background: var(--accent-soft); color: var(--accent); margin-left: 6px; }

/* Engagement */
.eng-list { list-style: none; }
.eng-item { display: flex; align-items: center; justify-content: space-between; padding: 13px 20px; border-bottom: 1px solid var(--rule); gap: 12px; }
.eng-item:last-child { border-bottom: none; }
.eng-metric { font-size: 13px; font-weight: 500; }
.eng-sub { font-size: 11px; color: var(--ink-mute); margin-top: 1px; font-family: var(--mono); }
.eng-value { font-family: var(--mono); font-size: 18px; font-weight: 700; text-align: right; }
.eng-value small { font-size: 11px; font-weight: 400; color: var(--ink-mute); display: block; }

/* Country */
.country-table { width: 100%; border-collapse: collapse; }
.country-table tr { border-bottom: 1px solid var(--rule); }
.country-table tr:last-child { border-bottom: none; }
.country-table td { padding: 10px 20px; font-size: 13px; vertical-align: middle; }
.country-table td:nth-child(3), .country-table td:nth-child(4) { text-align: right; font-family: var(--mono); font-size: 12px; color: var(--ink-soft); }
.country-flag { margin-right: 8px; }
.country-bar-wrap { min-width: 100px; }
.country-bar-bg { height: 4px; background: var(--bg-3); border-radius: 2px; overflow: hidden; }
.country-bar-fill { height: 100%; background: var(--accent); border-radius: 2px; opacity: .5; }

/* Events */
.events-list { list-style: none; }
.event-item { display: flex; align-items: center; justify-content: space-between; padding: 11px 20px; border-bottom: 1px solid var(--rule); gap: 12px; }
.event-item:last-child { border-bottom: none; }
.event-name { font-family: var(--mono); font-size: 12px; font-weight: 500; }
.event-count { font-family: var(--mono); font-size: 13px; font-weight: 600; color: var(--accent); }

/* Footer */
.dash-footer { margin-top: 32px; font-size: 11px; color: var(--ink-mute); font-family: var(--mono); text-align: center; }
</style>
</head>
<body>
<div id="root"></div>
<!-- DATA AND RENDER SCRIPT — added in subsequent tasks -->
</body>
</html>
```

- [ ] **Step 2: Verify the shell opens without errors**

Open `analytics.html` directly in a browser (double-click, or run `npx serve .` from the project root and visit `http://localhost:3000/analytics.html`).

Expected: blank page with `#f3f6fb` background and no console errors.

- [ ] **Step 3: Commit**

```bash
git add analytics.html
git commit -m "feat: add analytics dashboard scaffold with CSS"
```

---

### Task 2: Define the inline data contract

**Files:**
- Modify: `analytics.html`

The two `<script>` data blocks are the only interface between Claude (data provider) and the render engine (consumer). Comment markers tell Claude exactly what to replace on each operation.

- [ ] **Step 1: Replace the placeholder comment with both data blocks**

In `analytics.html`, replace:
```html
<!-- DATA AND RENDER SCRIPT — added in subsequent tasks -->
```

With:
```html
<!-- ANALYTICS_DATA:BEGIN -->
<script>
const ANALYTICS_DATA = {
  refreshed: "—",
  range: "28d",
  stats: {
    activeUsers: 0, activeUsersDelta: 0,
    sessions: 0,    sessionsDelta: 0,
    pageViews: 0,   pageViewsDelta: 0,
    bounceRate: 0,  bounceRateDelta: 0,
  },
  topPages: [],
  engagement: {
    avgSessionDuration: "—", avgSessionDurationDeltaSecs: 0,
    pagesPerSession: 0,      pagesPerSessionDelta: 0,
    newUsersPercent: 0,      returningUsersPercent: 0,
    newUsersPrevPercent: 0,
    newsletterClicks: 0,
    shareXClicks: 0,
  },
  countries: [],
  events: [],
  krCurrentValues: {},
};
</script>
<!-- ANALYTICS_DATA:END -->

<!-- OKR_DATA:BEGIN -->
<script>
const OKR_DATA = {
  objectives: [],
};
</script>
<!-- OKR_DATA:END -->

<script>
// render engine — added in subsequent tasks
</script>
```

- [ ] **Step 2: Verify both objects are accessible in the browser console**

Reload `analytics.html`. Open DevTools → Console and run:

```javascript
console.log(ANALYTICS_DATA.range);   // → "28d"
console.log(OKR_DATA.objectives);    // → []
```

Expected: both log without errors.

- [ ] **Step 3: Commit**

```bash
git add analytics.html
git commit -m "feat: add ANALYTICS_DATA and OKR_DATA inline data contracts"
```

---

### Task 3: Render engine — header and stat cards

**Files:**
- Modify: `analytics.html` (the `// render engine` script block)

- [ ] **Step 1: Replace `// render engine — added in subsequent tasks` with helpers, header, stat card functions, and the app entry point**

Replace the comment line with:

```javascript
// ── helpers ──────────────────────────────────────────────────────────
function fmt(n) {
  if (n === undefined || n === null || n === 0) return '—';
  return Number(n).toLocaleString();
}
function fmtDelta(n, unit, invert) {
  if (!n) return '<span class="delta-neutral">—</span>';
  const improved = invert ? n < 0 : n > 0;
  const cls = improved ? 'delta-up' : 'delta-down';
  const arrow = n > 0 ? '↑' : '↓';
  return `<span class="${cls}">${arrow} ${Math.abs(n)}${unit} vs prev period</span>`;
}
function barFill(delta) {
  return Math.min(99, Math.abs(delta || 0) * 3 + 30);
}

// ── Header ───────────────────────────────────────────────────────────
function renderHeader() {
  const { refreshed, range } = ANALYTICS_DATA;
  const btn = (r) => `<button class="range-btn${range === r ? ' active' : ''}" data-range="${r}">${r}</button>`;
  return `
    <div class="dash-header">
      <div>
        <div class="dash-site">Product Genesis</div>
        <div class="dash-heading">Site Analytics</div>
        <div class="dash-updated">Last refreshed: ${refreshed}</div>
      </div>
      <div class="range-toggle">${btn('7d')}${btn('28d')}${btn('90d')}</div>
    </div>`;
}

// ── Stat cards ───────────────────────────────────────────────────────
function renderStats() {
  const s = ANALYTICS_DATA.stats;
  const card = ({ label, value, delta, unit, invert, barColor }) => `
    <div class="stat-card">
      <div class="stat-label">${label}</div>
      <div class="stat-value">${value}</div>
      <div class="stat-delta">${fmtDelta(delta, unit, invert)}</div>
      <div class="stat-bar"><div class="stat-bar-fill" style="width:${barFill(delta)}%;background:${barColor || 'var(--accent)'}"></div></div>
    </div>`;
  return `
    <div class="stat-grid">
      ${card({ label: 'Active Users', value: fmt(s.activeUsers), delta: s.activeUsersDelta, unit: '%' })}
      ${card({ label: 'Sessions',     value: fmt(s.sessions),    delta: s.sessionsDelta,    unit: '%' })}
      ${card({ label: 'Page Views',   value: fmt(s.pageViews),   delta: s.pageViewsDelta,   unit: '%' })}
      ${card({ label: 'Bounce Rate',  value: s.bounceRate ? s.bounceRate + '%' : '—', delta: s.bounceRateDelta, unit: 'pp', invert: true, barColor: 'var(--amber)' })}
    </div>`;
}

// ── App entry point ──────────────────────────────────────────────────
function renderApp() {
  document.getElementById('root').innerHTML = `
    <div class="page">
      ${renderHeader()}
      <div id="okr-slot"></div>
      ${renderStats()}
      <div id="panels-slot"></div>
      <div class="dash-footer">Product Genesis · Analytics · Data from Google Analytics 4 · Refreshed by Claude</div>
    </div>`;
  initRangeToggle();
}

function initRangeToggle() {
  document.querySelectorAll('.range-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.range-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
}

document.addEventListener('DOMContentLoaded', renderApp);
```

- [ ] **Step 2: Reload and verify header and empty stat cards render**

Reload `analytics.html`.
Expected:
- Header shows "Product Genesis / Site Analytics", refreshed "—", "28d" button active in accent blue
- Four stat cards appear in a row with "—" values and no console errors
- Clicking "7d" / "90d" buttons updates which one appears active

- [ ] **Step 3: Add sample data to ANALYTICS_DATA.stats to verify formatting**

In the `ANALYTICS_DATA` block, update `stats` to:
```javascript
stats: {
  activeUsers: 1284, activeUsersDelta: 18,
  sessions: 1841,    sessionsDelta: 12,
  pageViews: 4203,   pageViewsDelta: 24,
  bounceRate: 41,    bounceRateDelta: -6,
},
```

Reload. Expected:
- Active Users card: "1,284", green "↑ 18% vs prev period"
- Bounce Rate card: "41%", green "↓ 6pp vs prev period" (invert=true so down is good)

- [ ] **Step 4: Commit**

```bash
git add analytics.html
git commit -m "feat: render header and stat cards from ANALYTICS_DATA"
```

---

### Task 4: Render OKR section with steps accordion

**Files:**
- Modify: `analytics.html`

- [ ] **Step 1: Add OKR render functions inside the render engine `<script>`, before `renderApp()`**

Insert the following block before the `// ── App entry point` line:

```javascript
// ── OKR section ──────────────────────────────────────────────────────
function confClass(c) {
  return { high: 'conf-high', med: 'conf-med', low: 'conf-low' }[c] || 'conf-med';
}
function confLabel(c) {
  return { high: 'High', med: 'Med', low: 'Low' }[c] || c;
}

function renderStep(step, index) {
  const dotClass = step.status === 'done' ? 'done' : step.status === 'active' ? 'active' : '';
  const dotInner = step.status === 'done' ? '✓' : String(index + 1);
  const statusSuffix = step.status === 'done' ? ' · Complete' : step.status === 'active' ? ' · In progress' : '';
  return `
    <li class="step-item">
      <div class="step-dot ${dotClass}">${dotInner}</div>
      <div class="step-content">
        <div class="step-title">${step.title}</div>
        <div class="step-desc">${step.description}</div>
        <div class="step-date">${step.date}${statusSuffix}</div>
      </div>
    </li>`;
}

function renderKR(kr, index) {
  const current = ANALYTICS_DATA.krCurrentValues[kr.id] ?? 0;
  const pct = kr.target > 0 ? Math.min(100, (current / kr.target) * 100).toFixed(0) : 0;
  const barColor = kr.invertProgress ? 'var(--amber)' : 'var(--accent)';
  const currentDisplay = kr.isPercent ? (current || '—') + (current ? '%' : '') : fmt(current);
  const targetDisplay  = kr.isPercent ? '< ' + kr.target + '%' : fmt(kr.target);
  const stepsHtml = (kr.steps || []).map((s, i) => renderStep(s, i)).join('');
  return `
    <li class="kr-item">
      <div class="kr-row">
        <div class="kr-num">${index + 1}</div>
        <div class="kr-main">
          <div class="kr-description">${kr.description}</div>
          <div class="kr-metric-row">
            <span class="kr-metric-tag">${kr.metricLabel}</span>
            <div class="kr-progress-wrap">
              <div class="kr-progress-track">
                <div class="kr-progress-fill" style="width:${pct}%;background:${barColor}"></div>
              </div>
              <div class="kr-values"><strong>${currentDisplay}</strong> / ${targetDisplay}</div>
            </div>
          </div>
        </div>
        <div class="kr-date-chip">${kr.targetDate}</div>
        <div class="confidence-chip ${confClass(kr.confidence)}">${confLabel(kr.confidence)}</div>
        <button class="steps-btn" data-kr-id="${kr.id}" title="View action steps">▶</button>
      </div>
      <div class="steps-panel" id="steps-${kr.id}">
        <ul class="steps-list">${stepsHtml}</ul>
      </div>
    </li>`;
}

function renderObjective(obj) {
  const krsHtml = (obj.keyResults || []).map((kr, i) => renderKR(kr, i)).join('');
  return `
    <div class="okr-section">
      <div class="okr-header">
        <div style="display:flex;align-items:center;gap:12px">
          <span class="okr-badge">OKR</span>
          <span class="okr-section-title">Objectives & Key Results</span>
        </div>
        <button class="okr-add-btn">+ Add via Claude</button>
      </div>
      <div class="objective-row">
        <div class="obj-icon">${obj.icon || '🎯'}</div>
        <div>
          <div class="obj-label">Objective · ${obj.quarter}</div>
          <div class="obj-text">${obj.text}</div>
        </div>
      </div>
      <ul class="kr-list">${krsHtml}</ul>
    </div>`;
}

function renderOKR() {
  return (OKR_DATA.objectives || []).map(renderObjective).join('');
}

function initAccordions() {
  document.querySelectorAll('.steps-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const panel = document.getElementById('steps-' + btn.dataset.krId);
      const open = panel.classList.toggle('open');
      btn.classList.toggle('open', open);
      btn.textContent = open ? '▼' : '▶';
    });
  });
}
```

- [ ] **Step 2: Update `renderApp()` to call `renderOKR()` and `initAccordions()`**

Replace the existing `renderApp()` function with:

```javascript
function renderApp() {
  document.getElementById('root').innerHTML = `
    <div class="page">
      ${renderHeader()}
      ${renderOKR()}
      ${renderStats()}
      <div id="panels-slot"></div>
      <div class="dash-footer">Product Genesis · Analytics · Data from Google Analytics 4 · Refreshed by Claude</div>
    </div>`;
  initRangeToggle();
  initAccordions();
}
```

- [ ] **Step 3: Add a sample objective to OKR_DATA to verify rendering**

Replace the `OKR_DATA` block with:

```javascript
const OKR_DATA = {
  objectives: [
    {
      id: "obj1",
      quarter: "Q2 2026",
      icon: "🎯",
      text: "Grow Product Genesis into a destination for 5,000 active product builders per month",
      keyResults: [
        {
          id: "kr1",
          description: "Reach 3,500 monthly active users",
          metricLabel: "Active Users",
          target: 3500,
          targetDate: "30 Jun 2026",
          confidence: "med",
          isPercent: false,
          invertProgress: false,
          steps: [
            { title: "Launch daily digest workflow", description: "Publish curated content 5 days/week to build habit-forming visit cadence.", date: "10 May 2026", status: "done" },
            { title: "Publish to 3 distribution channels", description: "Cross-post digests to LinkedIn, X, and one newsletter to drive referral traffic.", date: "1 Jun 2026", status: "active" },
            { title: "SEO: optimise top 10 posts", description: "Add meta descriptions, structured headings, and internal links to highest-traffic posts.", date: "20 Jun 2026", status: "pending" }
          ]
        },
        {
          id: "kr2",
          description: "Reduce bounce rate below 30%",
          metricLabel: "Bounce Rate",
          target: 30,
          targetDate: "30 Jun 2026",
          confidence: "low",
          isPercent: true,
          invertProgress: true,
          steps: [
            { title: "Add related posts to each article", description: "Surface 3 related posts at the bottom of every expanded post to encourage next reads.", date: "5 Jun 2026", status: "pending" },
            { title: "Improve above-the-fold hook", description: "Rewrite hero dek and category intros to immediately signal value to new visitors.", date: "15 Jun 2026", status: "pending" }
          ]
        }
      ]
    }
  ]
};
```

Also update `krCurrentValues` in `ANALYTICS_DATA`:
```javascript
krCurrentValues: { "kr1": 1284, "kr2": 41 },
```

Reload. Expected:
- OKR card appears above stat cards
- KR1: "1,284 / 3,500" with blue progress bar at ~37%
- KR2: "41% / < 30%" with amber progress bar
- Clicking ▶ on KR1: steps panel expands; step 1 has green ✓, step 2 blue dot, step 3 grey
- Clicking ▼: panel collapses
- No console errors

- [ ] **Step 4: Commit**

```bash
git add analytics.html
git commit -m "feat: render OKR section with steps accordion"
```

---

### Task 5: Render Top Pages and Engagement panels

**Files:**
- Modify: `analytics.html`

- [ ] **Step 1: Add `renderTopPages()` and `renderEngagement()` before `renderApp()`**

```javascript
// ── Top Pages ─────────────────────────────────────────────────────────
function renderTopPages() {
  const pages = ANALYTICS_DATA.topPages;
  const maxViews = pages.length ? Math.max(...pages.map(p => p.views)) : 1;
  const rows = pages.map(p => {
    const pct = ((p.views / maxViews) * 100).toFixed(0);
    const pill = p.cat ? `<span class="page-cat-pill">${p.cat}</span>` : '';
    return `
      <tr>
        <td>${p.title}${pill}</td>
        <td class="page-bar-cell"><div class="page-mini-bar"><div class="page-mini-bar-fill" style="width:${pct}%"></div></div></td>
        <td>${fmt(p.views)}</td>
      </tr>`;
  }).join('');
  const empty = `<tr><td colspan="3" style="padding:20px;text-align:center;color:var(--ink-mute);font-family:var(--mono);font-size:12px">No data — refresh the dashboard</td></tr>`;
  return `
    <div class="panel">
      <div class="panel-head"><span class="panel-title">Top Pages</span></div>
      <table class="pages-table">${rows || empty}</table>
    </div>`;
}

// ── Engagement ────────────────────────────────────────────────────────
function renderEngagement() {
  const e = ANALYTICS_DATA.engagement;
  const durDelta = e.avgSessionDurationDeltaSecs
    ? `${e.avgSessionDurationDeltaSecs > 0 ? '↑' : '↓'} ${Math.abs(e.avgSessionDurationDeltaSecs)}s`
    : '—';
  const ppsDelta = e.pagesPerSessionDelta
    ? `${e.pagesPerSessionDelta > 0 ? '↑' : '↓'} ${Math.abs(e.pagesPerSessionDelta).toFixed(1)}`
    : '—';
  const newPrev = e.newUsersPrevPercent || '—';
  const retPrev = e.newUsersPrevPercent ? 100 - e.newUsersPrevPercent : '—';
  const row = (metric, sub, value, small) => `
    <li class="eng-item">
      <div><div class="eng-metric">${metric}</div><div class="eng-sub">${sub}</div></div>
      <div class="eng-value">${value}<small>${small}</small></div>
    </li>`;
  return `
    <div class="panel">
      <div class="panel-head"><span class="panel-title">Engagement</span></div>
      <ul class="eng-list">
        ${row('Avg Session Duration', 'time on site per visit', e.avgSessionDuration || '—', durDelta)}
        ${row('Pages / Session', 'avg posts read per visit', e.pagesPerSession || '—', ppsDelta)}
        ${row('New vs Returning', 'user type split', `${e.newUsersPercent || '—'}/${e.returningUsersPercent || '—'}%`, `vs ${newPrev}/${retPrev}%`)}
        ${row('Newsletter Clicks', 'sign-up link taps', fmt(e.newsletterClicks), 'events')}
        ${row('X Share Clicks', 'tweet button taps', fmt(e.shareXClicks), 'events')}
      </ul>
    </div>`;
}
```

- [ ] **Step 2: Update `renderApp()` to render the first two-column row**

Replace `<div id="panels-slot"></div>` inside `renderApp()` with:

```javascript
<div class="two-col section-gap">
  ${renderTopPages()}
  ${renderEngagement()}
</div>
<div id="bottom-row-slot"></div>
```

Full updated `renderApp()`:
```javascript
function renderApp() {
  document.getElementById('root').innerHTML = `
    <div class="page">
      ${renderHeader()}
      ${renderOKR()}
      ${renderStats()}
      <div class="two-col section-gap">
        ${renderTopPages()}
        ${renderEngagement()}
      </div>
      <div id="bottom-row-slot"></div>
      <div class="dash-footer">Product Genesis · Analytics · Data from Google Analytics 4 · Refreshed by Claude</div>
    </div>`;
  initRangeToggle();
  initAccordions();
}
```

- [ ] **Step 3: Add sample data and verify**

Update `ANALYTICS_DATA` with:
```javascript
topPages: [
  { path: "/", title: "Homepage", cat: null, views: 1021 },
  { path: "/post/why-ai-products-fail", title: "Why AI Products Fail", cat: "vision", views: 736 },
  { path: "/post/the-moat-myth", title: "The Moat Myth", cat: "strategy", views: 524 },
  { path: "/post/evals-that-work", title: "Evals That Actually Work", cat: "dev", views: 391 },
  { path: "/post/ai-pricing", title: "AI Pricing Strategies", cat: "strategy", views: 298 },
  { path: "/post/gtm-loop", title: "Building Your GTM Loop", cat: "marketing", views: 227 },
],
engagement: {
  avgSessionDuration: "3:42", avgSessionDurationDeltaSecs: 18,
  pagesPerSession: 2.28,      pagesPerSessionDelta: 0.3,
  newUsersPercent: 68,        returningUsersPercent: 32,
  newUsersPrevPercent: 71,
  newsletterClicks: 47,
  shareXClicks: 89,
},
```

Reload. Expected:
- Two-column row: Top Pages left (6 rows, proportional bars, category pills), Engagement right (5 rows with values)
- No console errors

- [ ] **Step 4: Commit**

```bash
git add analytics.html
git commit -m "feat: render top pages and engagement panels"
```

---

### Task 6: Render Country and Events panels, complete layout

**Files:**
- Modify: `analytics.html`

- [ ] **Step 1: Add `renderCountries()` and `renderEvents()` before `renderApp()`**

```javascript
// ── Countries ─────────────────────────────────────────────────────────
function renderCountries() {
  const countries = ANALYTICS_DATA.countries;
  const maxUsers = countries.length ? Math.max(...countries.map(c => c.users)) : 1;
  const rows = countries.map(c => {
    const pct = ((c.users / maxUsers) * 100).toFixed(0);
    return `
      <tr>
        <td><span class="country-flag">${c.flag}</span>${c.country}</td>
        <td class="country-bar-wrap"><div class="country-bar-bg"><div class="country-bar-fill" style="width:${pct}%"></div></div></td>
        <td>${fmt(c.users)}</td>
        <td>${c.percent}%</td>
      </tr>`;
  }).join('');
  const empty = `<tr><td colspan="4" style="padding:20px;text-align:center;color:var(--ink-mute);font-family:var(--mono);font-size:12px">No data — refresh the dashboard</td></tr>`;
  return `
    <div class="panel">
      <div class="panel-head"><span class="panel-title">Traffic by Country</span></div>
      <table class="country-table">${rows || empty}</table>
    </div>`;
}

// ── Events ────────────────────────────────────────────────────────────
function renderEvents() {
  const events = ANALYTICS_DATA.events;
  const rows = events.map(e => `
    <li class="event-item">
      <span class="event-name">${e.name}</span>
      <span class="event-count">${fmt(e.count)}</span>
    </li>`).join('');
  const empty = `<li class="event-item" style="justify-content:center;color:var(--ink-mute);font-family:var(--mono);font-size:12px">No data — refresh the dashboard</li>`;
  return `
    <div class="panel">
      <div class="panel-head"><span class="panel-title">Top Events</span></div>
      <ul class="events-list">${rows || empty}</ul>
    </div>`;
}
```

- [ ] **Step 2: Update `renderApp()` to include the bottom two-column row**

Replace `<div id="bottom-row-slot"></div>` with:

```javascript
<div class="two-col section-gap">
  ${renderCountries()}
  ${renderEvents()}
</div>
```

Full final `renderApp()`:
```javascript
function renderApp() {
  document.getElementById('root').innerHTML = `
    <div class="page">
      ${renderHeader()}
      ${renderOKR()}
      ${renderStats()}
      <div class="two-col section-gap">
        ${renderTopPages()}
        ${renderEngagement()}
      </div>
      <div class="two-col section-gap">
        ${renderCountries()}
        ${renderEvents()}
      </div>
      <div class="dash-footer">Product Genesis · Analytics · Data from Google Analytics 4 · Refreshed by Claude</div>
    </div>`;
  initRangeToggle();
  initAccordions();
}
```

- [ ] **Step 3: Add sample data and verify**

Update `ANALYTICS_DATA` with:
```javascript
countries: [
  { flag: "🇺🇸", country: "United States", users: 512, percent: 39.8 },
  { flag: "🇮🇪", country: "Ireland",        users: 308, percent: 24.0 },
  { flag: "🇬🇧", country: "United Kingdom", users: 186, percent: 14.5 },
  { flag: "🇨🇦", country: "Canada",         users: 94,  percent: 7.3  },
  { flag: "🇦🇺", country: "Australia",      users: 57,  percent: 4.4  },
  { flag: "🌐",  country: "Other",           users: 127, percent: 9.9  },
],
events: [
  { name: "page_view",        count: 4203 },
  { name: "scroll",           count: 2841 },
  { name: "post_expand",      count: 1104 },
  { name: "category_nav",     count: 382  },
  { name: "share_x",         count: 89   },
  { name: "newsletter_click", count: 47   },
  { name: "video_click",      count: 61   },
],
```

Reload. Expected: full dashboard visible — OKR → stat cards → pages/engagement → countries/events → footer. No console errors.

- [ ] **Step 4: Commit**

```bash
git add analytics.html
git commit -m "feat: render country and events panels, complete dashboard layout"
```

---

### Task 7: Add analytics.html to .gitignore

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add the entry**

In `.gitignore`, add after the `# Uploads` block:

```
# Analytics dashboard — contains live GA traffic data, regenerated locally by Claude
analytics.html
```

- [ ] **Step 2: Verify git ignores the file**

```bash
git check-ignore -v analytics.html
```

Expected output contains `analytics.html` with the `.gitignore` source path.

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: exclude analytics.html from git (contains live GA data)"
```

---

### Task 8: Final integration check

**Files:** none — verification only

- [ ] **Step 1: Clear ANALYTICS_DATA to zeroes and verify empty states**

Set all numeric fields in `ANALYTICS_DATA` to `0`, arrays to `[]`, `krCurrentValues` to `{}`, `refreshed` to `"—"`.

Reload. Expected:
- All stat cards show "—"
- "No data — refresh the dashboard" messages in Top Pages, Countries
- OKR KRs show "— / 3,500" (target from OKR_DATA is preserved; current from krCurrentValues is missing)
- No console errors

- [ ] **Step 2: Restore sample data and run the full smoke checklist**

Restore all sample data from Tasks 3–6.

- [ ] Header: "Last refreshed: —" (or a timestamp if set), "28d" button active in blue
- [ ] Clicking "7d" button: "7d" becomes active, "28d" loses active style
- [ ] OKR objective text visible above stat cards
- [ ] KR1 progress bar ~37% filled in blue
- [ ] KR2 progress bar amber, shows "41% / < 30%"
- [ ] Clicking ▶ on KR1 expands steps; step 1 has green ✓, step 2 blue, step 3 grey dot
- [ ] Clicking ▼ collapses KR1 steps again
- [ ] 4 stat cards: correct values, correct delta colours (bounce rate green for negative delta)
- [ ] Top Pages: 6 rows, bars proportional, "vision" / "strategy" / "dev" / "marketing" pills
- [ ] Engagement: 5 rows with values
- [ ] Countries: 6 rows with flags and bars, "Other" at bottom
- [ ] Events: 7 rows, counts in accent blue
- [ ] Footer text correct

- [ ] **Step 3: Confirm main site unaffected**

Open `index.html` in the same browser. Expected: main site loads normally with no console errors from analytics code.

- [ ] **Step 4: Final commit**

```bash
git add analytics.html
git commit -m "feat: analytics dashboard complete with OKR section, sample data verified"
```

---

## Refresh Workflow Reference (Claude operating instructions — not code to implement)

When Gerald says *"refresh the analytics dashboard"* (or *"refresh for the last 7 days"*):

1. Determine date range: `endDate = today`, `startDate = today − N days`
2. Call GA MCP tools in parallel:
   - `getActiveUsers(startDate, endDate)` → `stats.activeUsers` + delta vs prev period
   - `runReport(startDate, endDate, [{name:"sessions"}], [])` → `stats.sessions` + delta
   - `getPageViews(startDate, endDate, [{name:"pagePath"}])` → `stats.pageViews`, `stats.pageViewsDelta`, populate `topPages` array
   - `getUserBehavior(startDate, endDate)` → `stats.bounceRate`, `stats.bounceRateDelta`, `engagement.avgSessionDuration`, `engagement.avgSessionDurationDeltaSecs`, `engagement.pagesPerSession`, `engagement.pagesPerSessionDelta`
   - `getEvents(startDate, endDate)` → populate `events` array; set `engagement.newsletterClicks` from `newsletter_click` event count; set `engagement.shareXClicks` from `share_x` event count
   - `runReport(startDate, endDate, [{name:"activeUsers"}], [{name:"country"}])` → populate `countries` array (top 5 + sum remainder as "Other" with 🌐)
   - `runReport(startDate, endDate, [{name:"activeUsers"}], [{name:"newVsReturning"}])` → `engagement.newUsersPercent`, `engagement.returningUsersPercent`, `engagement.newUsersPrevPercent`
3. Set `refreshed` to current datetime (e.g. `"Sat 24 May 2026 · 09:41"`)
4. Set `range` to `"7d"`, `"28d"`, or `"90d"` matching the request
5. For each KR in `OKR_DATA.objectives[*].keyResults`: look up its current value from fetched data and set `krCurrentValues[kr.id]`
6. Read `analytics.html`, replace everything between `<!-- ANALYTICS_DATA:BEGIN -->` and `<!-- ANALYTICS_DATA:END -->` (inclusive) with the new data block
7. Write the updated file
8. Report: *"Dashboard refreshed — X active users, Y sessions, Z page views over the last N days."*

**Claude does NOT touch OKR_DATA during a refresh.**
