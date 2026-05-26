# Product Genesis — Claude Instructions

This is the source for **Product Genesis**, a site about product design in the age of AI.
Owner: Gerald (gerald.tcd@gmail.com)

---

## Site architecture

| File | Purpose |
|---|---|
| `index.html` | Entry point. Loads React 18 (CDN), Babel, fonts, CSS. No build step. |
| `styles.css` | All visual styling. CSS custom properties at the top for palette/theme. |
| `app.jsx` | Full React app: hero, category nav, post feed, inline expand, newsletter, footer. |
| `data.js` | **All content lives here.** Two exports: `window.PG_CATEGORIES` and `window.PG_POSTS`. |
| `tweaks-panel.jsx` | In-page design controls (ignore unless doing UI work). |
| `reviews/` | Daily digest files awaiting approval. Format: `YYYY-MM-DD.md`. |
| `uploads/` | Brand assets (PDFs, images). |

To run locally: `npx serve .` then open `http://localhost:3000`.

---

## The six content categories

```
vision        → How AI changes what products are and what product design means
strategy      → Moats, roadmaps, competitive positioning for AI-native products
development   → Full build loop (5 sub-categories below)
  discovery   → User research, problem framing, jobs-to-be-done
  dev         → LLM patterns, AI coding workflows, architecture
  testing     → Evals, QA, LLM regression testing
  uiux        → Generative UI, interaction design, AI UX patterns
  cicd        → Deployment pipelines, eval-driven CI, observability
marketing     → GTM, positioning, demos, content strategy for AI products
sales         → How AI is used in sales: prospecting, pipeline management, deal intelligence, outreach automation
operations    → Cost control, team structure, incident response, AI ops
```

---

## How to add content (the daily workflow)

### Step 1 — Curate (done by Claude, daily)

Claude searches the web for the last 24 hours of AI + product news across all six categories and writes a review file:

```
reviews/YYYY-MM-DD.md
```

Each item in the file has a checkbox `[ ]` and full metadata (source, type, suggested title, dek, read time).

**To trigger manually:** Tell Claude: _"run the daily curation for today"_

Claude will:
1. Run WebSearch queries across all six categories (see detailed queries in `.claude/skills/curate-daily/SKILL.md`)
2. Search YouTube for the best video from the last 7 days in each category
3. Evaluate quality: credibility, specificity, engagement, freshness
4. Select 3–5 written items + 1 video per category
5. Write the review file with `[ ]` checkboxes, suggested titles, deks, and a short "why publish" note per item
6. Confirm the file is ready for review

**Every category must include one video pick.** Videos are searched over a 7-day window (extend to 30 days if nothing compelling is within 7). See video search queries in `.claude/skills/curate-daily/SKILL.md`.

---

### Step 2 — Approve (done by Gerald)

Open `reviews/YYYY-MM-DD.md`. For each item you want published, change:
```
- [ ] **Approve for publishing**
```
to:
```
- [x] **Approve for publishing**
```

Leave unchecked items as `[ ]` — they will be skipped.

---

### Step 3 — Publish (done by Claude)

Tell Claude: _"publish the digest for YYYY-MM-DD"_

Claude will:
1. Read `reviews/YYYY-MM-DD.md` and find all `[x]` items
2. Read `data.js` to check existing post IDs — never reuse one
3. For each approved item, fetch the source URL and write a post body:
   - **thought**: no body (dek is the post)
   - **note**: 2–3 paragraphs summarising the key insight
   - **essay**: 3–5 paragraphs with argument, evidence, and product team implication
   - **video**: 1 paragraph describing content + `videoLabel`/`videoLength` fields
   - **case-study**: setup → approach → result → lesson
4. Insert new posts at the **top** of their category block in `data.js` (most recent first)
5. **Enforce the 10-post cap:** after inserting, if a category has more than 10 posts, delete the oldest (lowest in the file) until only 10 remain
6. Confirm what was published

**New post ID convention:**
- Vision: `v4`, `v5`, `v6`…
- Strategy: `s4`, `s5`…
- Development: `d7`, `d8`…
- Marketing: `m4`, `m5`…
- Sales: `sa4`, `sa5`…
- Operations: `o4`, `o5`…

---

## Post object format (data.js)

```js
{
  id: "v4",                    // unique — check existing IDs first
  cat: "vision",               // vision | strategy | development | marketing | sales | operations
  sub: null,                   // only for development: "discovery" | "dev" | "testing" | "uiux" | "cicd"
  type: "essay",               // essay | note | video | case-study | thought
  title: "...",                // punchy, specific — avoid generic AI titles
  dek: "...",                  // one sharp sentence shown under title on cards
  author: "Genesis",
  date: "May 20, 2026",        // match existing format exactly
  read: 6,                     // reading time in minutes
  feature: false,              // true = 2-column featured card (use sparingly, 1 per category max)
  tone: null,                  // "ink" | "warm" | "sand" | "accent" — or omit
  sourceUrl: "https://...",    // original source URL
  sourceLabel: "Author · Publication",
  tweet: "...",                // suggested tweet — use [link] as placeholder for the post URL
  body: [                      // array of paragraph strings — omit for 'thought' type
    "First paragraph.",
    "Second paragraph.",
  ],
  // Video-only optional fields:
  // videoLabel: "Talk · Conference Name",
  // videoLength: "12:04",
}
```

---

## Voice and style

- **Direct and specific.** No "AI is changing everything" takes. Concrete insight only.
- **Practitioner-first.** Written for people who build products, not people who read about building products.
- **No hype.** If a claim needs to be hedged, hedge it. If a stat is striking, say where it comes from.
- **Body paragraphs:** 3–6 sentences each. Short is fine. Padding is not.
- Titles and deks should feel like something a smart person would screenshot and share.

---

## Design — do not change without asking

- Fonts: Poppins (UI) + JetBrains Mono (labels/code)
- Palette: defined in `styles.css` CSS variables (`--c-accent`, `--c-bg`, etc.)
- The Tweaks panel (bottom-right on the live site) lets Gerald test palette/density/surface variants without code changes
- If Gerald asks for a design change, edit `styles.css` or `app.jsx` — never `data.js`

---

## Detailed skill references

- Curation logic: `.claude/skills/curate-daily/SKILL.md`
- Publishing logic: `.claude/skills/publish-digest/SKILL.md`
- Sample review file: `reviews/2026-05-20-SAMPLE.md`
