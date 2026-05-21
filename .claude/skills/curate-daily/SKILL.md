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
5. **Sales** — selling AI products, enterprise objections, pricing conversations, closing
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
**Sales:** `site:youtube.com selling AI enterprise pricing 2026`, `site:youtube.com AI sales strategy`
**Operations:** `site:youtube.com LLM inference cost production 2026`, `site:youtube.com AI ops cost control`

For each video, record: title, channel, YouTube URL, approximate length (from search metadata if visible), and upload date.

## Hard rules — enforce before selecting any item

### 1. Freshness cap — 7 days maximum
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
**Sales:** `selling AI enterprise`, `AI pricing model`, `AI procurement objections`
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

## Output format

Save the result to: `reviews/YYYY-MM-DD.md` (today's date).

Each category section must include a `· Video ·` item using this format:

```markdown
# Product Genesis · Daily Digest — YYYY-MM-DD

> **How to approve:** Change `[ ]` to `[x]` next to any item you want published.
> When done, tell Claude: **"publish the digest for YYYY-MM-DD"**
>
> Items left unchecked will be skipped.

---

## 01 · Vision

### V1 · Essay · [Short label]
- [ ] **Approve for publishing**
- **Source:** [Title](url) · Author · Publication
- **Type:** essay | note | thought | case-study | story
- **Why publish:** One sentence on why this matters.
- **Suggested site title:** "..."
- **Suggested dek:** "..."
- **Suggested tweet:** "... [link]"
- **Recommended post type:** essay | note | thought | case-study | story
- **Suggested central message:** "..."   ← include only when Recommended post type is story

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

---

## 02 · Strategy
(same structure — always include one Video item)

(continue for all six categories)

---

## Editor notes
Brief paragraph on today's overall theme — what's the one big thing in AI + product today?
```

## After writing the file

Tell the editor:
> "Today's digest is ready at `reviews/YYYY-MM-DD.md`. Each category includes a video pick from the past week. Mark the items you want published with [x], then tell me 'publish the digest for YYYY-MM-DD'."
