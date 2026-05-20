---
name: publish-digest
description: Publish approved items from a daily digest review file to the Product Genesis website. Reads the review MD, finds [x] checked items, generates proper data.js post entries, and inserts them.
---

# Publish Digest — Product Genesis

You are publishing approved content from a daily digest review file to the Product Genesis website.

## Step 1 — Read the review file

The user will have specified a date (e.g. "publish the digest for 2026-05-21").
Read: `reviews/2026-05-21.md`

## Step 2 — Find all approved items

Scan for items where the approval checkbox is checked:
```
- [x] **Approve for publishing**
```
Ignore all items with `- [ ]`.

## Step 3 — For each approved item, build a post object

Read the current `data.js` to understand the existing post IDs and structure. Never reuse an existing ID.

Generate a new unique ID: use the category prefix + a number one higher than the last in that category (e.g. if the last vision post is `v3`, use `v4`). If unsure, use `v-YYYYMMDD`, `s-YYYYMMDD`, etc.

For each approved item, produce a post object in this format:

```js
{
  id: "v4",                    // unique — check existing IDs first
  cat: "vision",               // vision | strategy | development | marketing | sales | operations
  sub: null,                   // only for development: "discovery" | "dev" | "testing" | "uiux" | "cicd"
  type: "essay",               // essay | note | video | case-study | thought
  title: "...",                // from "Suggested site title" in the review
  dek: "...",                  // from "Suggested dek" in the review
  author: "Genesis",
  date: "May 21, 2026",        // today's date formatted like existing entries
  read: 6,                     // from "Read time" in the review
  feature: false,              // leave false unless it's truly the standout piece of the week
  tone: null,                  // omit unless: "ink" (dark/serious), "warm" (optimistic), "sand" (neutral), "accent" (bold)
  body: [                      // array of paragraph strings
    "Paragraph one...",
    "Paragraph two...",
  ],
  sourceUrl: "https://...",    // original URL — include this so the source is credited
  sourceLabel: "...",          // e.g. "Lenny's Newsletter", "Twitter · @shreyas"
}
```

### How to write the body

**For thought / quick take:** No body needed — the dek is the post. Omit the `body` field.

**For note:** 2–3 short paragraphs. Summarise the source's key insight in your own words. End with one sharp takeaway sentence.

**For essay:** 3–5 paragraphs. Open with the problem or tension the source identifies. Cover the main argument. Pull one strong quote or stat if available. End with the implication for product teams.

**For video:** 1 paragraph describing what the video covers and who it's for. Include `videoLabel` and `videoLength` fields if you can determine them.

**For case study:** 3–4 paragraphs. Setup (what was the problem), approach (what they did), result (what happened), lesson (what to take away).

Fetch the source URL if needed to write an accurate body. Write in the Product Genesis voice: direct, specific, no hype, practitioner-first.

## Step 4 — Insert into data.js, trim to 10 per category

Open `data.js`.

Find the comment block for the relevant category (e.g. `// ── VISION ──`).
Insert the new post object(s) at the **top** of that category's block (most recent first).

**Enforce the 10-post cap:** after inserting, count all posts in that category. If the count exceeds 10, delete the oldest post(s) from the bottom of that category block until only 10 remain. The oldest posts are the ones furthest from the top of the category block (i.e. lowest in the file).

## Step 5 — Confirm

After writing data.js, tell the editor:

> "Published N post(s) to the site:
> - [title] → [category] · [type]
> - ...
>
> Refresh the browser to see them live."

If the dev server is not running, remind them to start it with `npx serve .` from the project folder.
