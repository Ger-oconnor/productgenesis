---
name: curate-daily
description: Run the daily Product Genesis content curation. Searches the web for the last 24 hours of AI + product news AND the best video from the last 7 days across all six categories, then writes a review file for Gerald to approve.
---

# Daily Curation — Product Genesis

You are running the daily content curation for Product Genesis, a site about product design in the age of AI. Your job is to search the web for the most important content published in the last 24 hours — plus one compelling video from the last 7 days — across six categories, evaluate quality, and produce a structured review file for the editor to approve.

## The six categories to cover

1. **Vision** — how AI is changing what products are and what product design means at the highest level
2. **Strategy** — AI moats, roadmaps, competitive positioning, pricing, and bets for AI-native products
3. **Development** — five sub-areas: Discovery (user research, problem framing), Development (LLM patterns, AI coding), Testing (evals, QA), UI/UX (generative UI, interaction design), CI/CD (deployment, eval pipelines)
4. **Marketing** — AI-era go-to-market, positioning, content strategy, demos, messaging
5. **Sales** — how AI is being used in sales: prospecting tools, CRM automation, deal intelligence, outreach personalisation, pipeline analysis, revenue ops
6. **Operations** — running AI products: cost control, team structure, incident response, tooling

## What to find

### Written content (last 24 hours)
For each category, search for content published in the last 24 hours. Prioritise:
- **Tweets / X threads** with significant engagement (retweets, replies, likes)
- **Substack / newsletter posts** from known product/AI writers
- **Blog posts and essays** from practitioners
- **Podcast episodes** with strong episode titles
- **LinkedIn posts** with high engagement from credible people

### Video pick (last 7 days) — ONE per category
Each category must also include exactly one video pick. Search YouTube for the most compelling, high-quality video published in the last 7 days. Prioritise:
- Talks, keynotes, or walkthroughs from credible practitioners (founders, engineers, PMs, researchers)
- Videos with concrete, specific insight — not generic explainers
- Channels with an established audience in the product/AI space
- Recent upload (within the past 7 days — extend to last 30 days only if nothing good is within 7)

**Video search queries (per category):**

**Vision:** `site:youtube.com AI product design future 2026`, `site:youtube.com product management AI era talk`
**Strategy:** `site:youtube.com AI product strategy moat competitive 2026`, `site:youtube.com AI startup strategy talk`
**Development:** `site:youtube.com LLM engineering workflow coding 2026`, `site:youtube.com AI developer tools walkthrough`
**Marketing:** `site:youtube.com AI product marketing positioning storytelling 2026`
**Sales:** `site:youtube.com AI sales tools prospecting 2026`, `site:youtube.com AI CRM automation deal intelligence`
**Operations:** `site:youtube.com LLM inference cost production 2026`, `site:youtube.com AI ops cost control`

For each video, record: title, channel, YouTube URL, approximate length (from search metadata if visible), and upload date.

## Hard rules — enforce before selecting any item

### 1. Current happenings only — no broad guides
**Reject any article or video framed as a broad survey, evergreen reference, or year-spanning overview.** Titles like "The Complete Guide to X", "Everything You Need to Know About X", "The Ultimate Guide to X", "X in 2026: A Full Overview", or "Year in Review" are disqualified regardless of publication date. The digest covers what is happening right now — specific announcements, new data or research, practitioner takes on a recent event, product launches, conference recaps, arguments made in response to something that just occurred.

Ask this question before including any item: **"Is this about something specific that happened recently?"** If the answer is no — if the piece would have been equally valid to publish six months ago — skip it.

### 2. Freshness cap — 7 days maximum
**No item may be older than 7 days from today's date.** This applies to all content types: written articles, tweets, newsletters, podcast episodes, and videos. If the only available video is older than 7 days, leave the video slot empty rather than include stale content. Do not extend the window beyond 7 days under any circumstances.

### 2. No duplicates — check data.js before finalising
**Before writing the review file, read `data.js` and extract every `sourceUrl` already in the site.** If a candidate item's URL matches any existing `sourceUrl`, skip it — even if it's an excellent piece. The same story must never appear twice on the site. This check applies to all content types.

```
// Pseudocode for dedup check
existingUrls = all sourceUrl values in data.js
for each candidate:
  if candidate.url in existingUrls → skip
  else → include
```

## Quality signals

For all content:
- Credible practitioner perspective (not generic AI commentary)
- Concrete and specific — not "AI is changing everything"
- Engagement relative to audience size
- Freshness (must be within 7 days — see hard rule above)

Aim for 3–5 written items + 1 video per category. Curated, not exhaustive.

## Search queries (written content)

Run at least 2–3 searches per category:

**Vision:** `AI product design 2026`, `future of product management AI`, `product design AI era site:substack.com OR site:medium.com`
**Strategy:** `AI product strategy moat`, `AI competitive advantage product`, `AI roadmap planning 2026`
**Development (Discovery):** `AI user research tools`, `AI jobs to be done`, `qualitative research AI`
**Development (Dev):** `LLM patterns production`, `AI feature shipping`, `vibe coding workflow`
**Development (Testing):** `LLM evals 2026`, `AI testing pipeline`, `prompt regression testing`
**Development (UI/UX):** `generative UI design`, `AI interaction design`, `streaming UX patterns`
**Development (CI/CD):** `AI deployment pipeline`, `eval driven CI`, `LLM observability`
**Marketing:** `AI product marketing`, `AI go to market`, `AI demo storytelling`
**Sales:** `AI sales prospecting tools`, `AI CRM automation 2026`, `AI deal intelligence pipeline`
**Operations:** `AI inference cost control`, `AI ops team`, `LLM cost per user`

## Writing the tweet

Every item must include a suggested tweet. Rules:

- **Under 280 characters** including the URL placeholder `[link]` (count it as 24 chars)
- **Lead with the insight, not the source.** Don't start with "Great article by…" — start with the provocative claim or surprising stat
- **Specific over general.** "87% of enterprise buyers want fixed pricing" beats "AI pricing is changing"
- **One idea per tweet.** No lists, no thread bait unless the content genuinely calls for it
- **Match the site voice:** direct, practitioner-first, no hype
- **End with pull** — a question, a sharp implication, or a "this changes X" statement that makes someone want to click
- Hashtags: 0–1 maximum, only if genuinely useful (e.g. `#prodmgmt`, `#llmops`). Never generic (`#AI #tech`)

Good example:
> BCG data: orgs using AI strategically capture 3.5x more value than those chasing tactical wins. The sprint-and-ship teams are already behind. [link]

Bad example:
> Great read on AI strategy! So many insights here 🔥 Check it out! #AI #strategy [link]

## Writing the draft body

**After selecting all items, fetch each source URL and write the full post body directly in the review file.** Gerald reads the draft body before approving — he should never be approving blind.

The body must be written from the source content itself — not from the search snippet. Fetch the URL and read the article. If the source is paywalled or returns no readable content, write what you can from the search metadata and add a note: `⚠️ Source paywalled — body written from search preview only.` so Gerald knows the draft is partial.

Body rules by type:

- **thought:** No body. The dek is the post. Omit the Draft body section entirely.
- **note:** 2–3 paragraphs. Summarise the source's key insight in your own words. End with one sharp takeaway sentence.
- **essay:** 3–5 paragraphs. Open with the problem or tension the source identifies. Cover the main argument. Pull one strong quote or stat if available. End with the implication for product teams.
- **video:** 1 paragraph describing what the video covers and why it's worth watching. Include what format it is (talk, walkthrough, interview) and who it's for.
- **case-study:** 3–4 paragraphs: setup → approach → result → lesson.
- **story:** 500–600 words following SCR structure. Open with a strong hook. Include at least one direct quote from the source. Repeat the central message in the hook and the resolution.

Write in the Product Genesis voice: direct, specific, no hype, practitioner-first. 3–6 sentences per paragraph. No padding.

**Suggested read time:** estimate from body length. Notes = 2–3 min. Essays = 5–7 min. Videos = the video length in minutes.

## Carry-over tweet check

Before writing the review file, check yesterday's review file (`reviews/YYYY-MM-DD.md` for the day before today):

1. Look for the `## Recommended Tweets` section at the top of that file.
2. Collect any items where the tweet checkbox is **NOT** ticked (`- [ ]`). These are stories Gerald has not yet tweeted.
3. Carry each unchecked item forward as a candidate for today's Recommended Tweets list — include its title, tweet text, source URL, category, and the original date.
4. If there is no previous review file, or no Recommended Tweets section, skip this step.

## Recommended Tweets section

At the very top of the review file — before the category sections — write a `## Recommended Tweets` section listing up to 10 stories to tweet today.

**Ranking the list:** Pool together (a) today's curated items and (b) any carry-overs from yesterday. Rank by tweet quality: sharp insight, punchy phrasing, likely engagement. Pick the best 10. If fewer than 10 are genuinely tweet-worthy, keep the list shorter — quality over completeness.

**Carry-over labelling:** Any item carried over from a previous day must include `*(Carried over from YYYY-MM-DD)*` so Gerald knows it is not new.

**Format each entry as:**

```markdown
- [ ] **[Story title]** · [Category]
  > [Full tweet text including [link] placeholder]
  - Source: URL
  - *(Carried over from YYYY-MM-DD)*   ← only for carry-overs
```

**How Gerald uses this section:** He ticks `[x]` after he tweets a story. Unticked items are candidates for carry-over into tomorrow's list. This section is separate from the publish approval checkboxes — ticking here means "I tweeted it", not "publish it to the site".

## Output format

Save the result to: `reviews/YYYY-MM-DD.md` (today's date).

Each item must include the full draft body. The format for each written item:

```markdown
# Product Genesis · Daily Digest — YYYY-MM-DD

> **How to approve:** Change `[ ]` to `[x]` next to any item you want published.
> When done, tell Claude: **"publish the digest for YYYY-MM-DD"**
>
> Items left unchecked will be skipped.

---

## Recommended Tweets

> Tick `[x]` after you tweet a story. Unticked items may carry forward to tomorrow.

- [ ] **[Story title]** · [Category]
  > [Tweet text including [link]]
  - Source: URL

- [ ] **[Story title]** · [Category]  *(Carried over from YYYY-MM-DD)*
  > [Tweet text including [link]]
  - Source: URL

(up to 10 entries — fewer is fine if not all are tweet-worthy)

---

## 01 · Vision

### V1 · Essay · [Short label]
- [ ] **Approve for publishing**
- **Source:** [Title](url) · Author · Publication
- **Type:** essay | note | thought | case-study | story
- **Published:** date
- **Why publish:** One sentence on why this matters.
- **Suggested site title:** "..."
- **Suggested dek:** "..."
- **Suggested tweet:** "... [link]"
- **Recommended post type:** essay | note | thought | case-study | story
- **Suggested read time:** N min
- **Suggested central message:** "..."   ← include only when Recommended post type is story

**Draft body:**

First paragraph of the post body.

Second paragraph of the post body.

Third paragraph of the post body.

---

### V2 · Video · [Short label]   ← REQUIRED — one per category
- [ ] **Approve for publishing**
- **Source:** [Title](YouTube URL) · Channel name · YouTube
- **Type:** video
- **Upload date:** e.g. May 18, 2026
- **Video length:** e.g. 24:30
- **Why publish:** One sentence on why this is the best video pick this week.
- **Suggested site title:** "..."
- **Suggested dek:** "..."
- **Suggested tweet:** "... [link]"
- **Video label:** e.g. "Talk · Re:Design Berlin" or "Walkthrough · Matt Pocock"
- **Recommended post type:** video

**Draft body:**

One paragraph describing what the video covers, what format it takes, and who it's for.

---

## 02 · Strategy
(same structure — always include one Video item with draft body)

(continue for all six categories)

---

## Editor notes
Brief paragraph on today's overall theme — what's the one big thing in AI + product today?
```

## After writing the file

Tell the editor:
> "Today's digest is ready at `reviews/YYYY-MM-DD.md`. Every item includes a draft body for you to read before approving. Mark what you want published with [x], then tell me 'publish the digest for YYYY-MM-DD'."
