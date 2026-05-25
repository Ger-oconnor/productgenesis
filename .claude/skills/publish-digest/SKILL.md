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
  type: "essay",               // essay | note | video | case-study | thought | story
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
  tweet: "...",                // tweet text with the full post URL substituted in — NEVER use [link] placeholder
                               // Format: "https://productgenesis.ai/#post-{id}" where {id} is this post's id field
                               // e.g. for id "v4": "...insight... https://productgenesis.ai/#post-v4"
  // Story-only:
  // centralMessage: "...",   // one sentence — the throughline, from the review brief
}
```

### How to get the body

**The review file contains a pre-written draft body under each approved item.** Use that draft body directly — do not rewrite or regenerate it. Gerald read and approved the content as written.

Look for the `**Draft body:**` section beneath each item's metadata. Copy the paragraphs as the `body` array, one string per paragraph.

**If no Draft body is present** (older review file format): fetch the source URL and write the body fresh following these rules:
- **thought / quick take:** No body — omit the `body` field.
- **note:** 2–3 short paragraphs. Summarise the key insight. End with one sharp takeaway.
- **essay:** 3–5 paragraphs. Problem → argument → evidence → product team implication.
- **video:** 1 paragraph describing what the video covers and who it's for.
- **case study:** Setup → approach → result → lesson.
- **story:** Use the `write-story` skill with the `centralMessage` from the review brief.

## Step 4 — Insert into data.js, trim to 10 per category

Open `data.js`.

Find the comment block for the relevant category (e.g. `// ── VISION ──`).
Insert the new post object(s) at the **top** of that category's block (most recent first).

**Enforce the 10-post cap:** after inserting, count all posts in that category. If the count exceeds 10, delete the oldest post(s) from the bottom of that category block until only 10 remain. The oldest posts are the ones furthest from the top of the category block (i.e. lowest in the file).

## Step 5 — Update tweet links in the review file

After inserting all posts into `data.js`, go back to the review file (`reviews/YYYY-MM-DD.md`) and update the **Recommended Tweets** section.

For every tweet entry whose story was just published, replace `[link]` with the real post URL:
```
https://productgenesis.ai/#post-{id}
```

Match each tweet to its post by title/category. Any carry-over items that were published on a previous date will already have their ID — use the ID for the post that is already live.

If a tweet entry's story was **not** published (checkbox left unchecked), leave `[link]` as-is — it may be carried forward to tomorrow's digest.

## Step 6 — Confirm

After writing data.js, tell the editor:

> "Published N post(s) to the site:
> - [title] → [category] · [type]
> - ...
>
> Refresh the browser to see them live."

If the dev server is not running, remind them to start it with `npx serve .` from the project folder.
