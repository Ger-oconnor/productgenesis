---
name: update-actions
description: After publishing a new volume, scan each category's new posts for a strong actionable insight and update the Call to Action list in data.js — adding a new top CTA and dropping the oldest.
---

# Update Actions — Product Genesis

Run this skill immediately after `publish-digest` completes for a new volume.

## Step 1 — Determine the current volume number

Read `data.js`. Find the volume number for the posts just published:

```js
const dates = [...new Set(PG_POSTS.map(p => p.date))].sort((a, b) => new Date(a) - new Date(b));
// VOL_TOTAL = dates.length
```

The new volume number is `VOL_TOTAL` (the count of unique dispatch dates after publishing).

## Step 2 — For each category, collect the new posts

The new posts are all `PG_POSTS` entries whose `date` matches today's published date.

Group them by `cat`:
- vision, strategy, development, marketing, sales, operations

## Step 3 — Evaluate each category for a strong CTA

For each category that has at least one new post, read the post bodies and ask:

**Does any post contain a single, concrete, actionable insight that a department head could act on this week?**

Strong signals:
- A specific stat or number that creates urgency (e.g. "72% fail to…", "$4,200 in fees")
- A gap between current behaviour and best practice
- A decision that can be made or triggered immediately
- A tool, practice, or audit that can be started today

Weak signals (skip):
- General awareness ("AI is changing X")
- Future predictions without present action
- Content that is purely definitional or explanatory

If no post in a category has a strong signal, **skip that category entirely** — do not add a placeholder.

## Step 4 — Draft the CTA

For qualifying categories, write a single imperative sentence in this style:

**Formula:** `[Verb] [specific thing] — [tension/consequence with a number if possible].`

Style rules:
- Start with an action verb (Audit, Redesign, Define, Map, Schedule, Build, Watch, Connect, Set, Assign)
- Include the most striking number or contrast from the source post
- End with the consequence of not acting, or what the action unlocks
- Max 25 words
- No hedging ("consider", "think about", "you might want to")

**Examples of the right tone:**
- "Redesign what your reps do with the 5 hours AI saves them each week — 72% of orgs fail to reinvest it."
- "Tag every production AI agent with an owner and cost baseline today — before the first surprise invoice, not after."
- "Schedule a red-teaming session before your next agent ships — evaluation is becoming a compliance requirement, not an engineering choice."

The `sourceUrl` and `sourceLabel` should point to the specific post source that generated the CTA (from the post's `sourceUrl` and `sourceLabel` fields).

## Step 5 — Update data.js

For each category where you drafted a new CTA:

1. Find that category's `actions` array in `PG_CATEGORIES`
2. **Prepend** the new action object at index 0:
   ```js
   { vol: VOL_TOTAL, text: "...", sourceUrl: "...", sourceLabel: "..." }
   ```
3. **Remove** the last item (index 4) to keep the array at exactly 5 items

Edit `data.js` directly. Do not add comments or change any other part of the file.

## Step 6 — Confirm

Report which categories received a new CTA and which were skipped (and why, briefly).

Example output:
```
Updated:
  vision    → "Audit whether your design team's…" (from v24)
  sales     → "Retrain your AEs to…" (from sa21)

Skipped:
  strategy  → no post with a concrete, immediate action signal
  marketing → new posts are video/awareness only
```

## Step 7 — Mark the actions checklist

Open `reviews/YYYY-MM-DD.md` (today's date) and find the `## Volume Update Checklist` section.

Mark all items under `### Actions Update` as `[x]`.

If the checklist section does not exist (older review file format), append the full template at the bottom of the review file with the Actions Update items set to `[x]` and the other sections left as `[ ]`.

At this point the full volume update is complete — all three sections of the checklist should be ticked.

---

## Completion Checklist

The full volume update requires all three stages. This is the reference — the live tracked copy lives in the review file.

### Curation ← curate-daily
- [ ] Web searches run for all 6 categories
- [ ] YouTube video search run for all 6 categories
- [ ] Duplicate check done against existing data.js sourceUrls
- [ ] Draft bodies written for all curated items
- [ ] Recommended Tweets section written
- [ ] Review file saved to reviews/YYYY-MM-DD.md

### Publishing ← publish-digest
- [ ] Approved items identified from review file
- [ ] Post IDs verified — no duplicates used
- [ ] Post objects built for all approved items
- [ ] Posts inserted at top of correct category blocks in data.js
- [ ] 10-post cap enforced for each affected category
- [ ] Tweet [link] placeholders replaced with real post URLs

### Actions Update ← this skill
- [ ] New posts scanned for CTA signals across all 6 categories
- [ ] CTAs drafted for qualifying categories
- [ ] data.js updated — new CTAs prepended with vol number
- [ ] 5th (oldest) action removed from each updated category
