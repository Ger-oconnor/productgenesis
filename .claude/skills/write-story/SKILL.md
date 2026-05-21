---
name: write-story
description: Use when writing a story-type post for Product Genesis — 500–600 word narrative with SCR structure, a central message that repeats in hook and resolution, vivid descriptors, and at least one direct quote from the source.
---

# Write Story — Product Genesis

Stories are the most narrative-driven post type. They translate a source article into a 500–600 word piece that puts a senior leader *inside* a situation, not just above it.

**Audience:** Read `docs/personas/empathy-map-senior-leaders.md` before writing. These are C-suite and function heads under pressure — fear of falling behind, pride at stake, the gap between what they say and what they actually feel. Write into that inner world.

## Post object

Stories use all standard fields plus one addition:

```js
{
  id: "v4",
  cat: "vision",
  sub: null,
  type: "story",
  title: "...",
  dek: "...",
  centralMessage: "...",     // one sentence — the idea the reader must leave with
  author: "Genesis",
  date: "May 21, 2026",
  read: 4,
  feature: false,
  tone: null,
  sourceUrl: "https://...",
  sourceLabel: "Author · Publication",
  tweet: "...",
  body: [...]
}
```

## Central message

The central message is the single idea the reader must leave with. It is suggested by Claude during curation and confirmed by Gerald in the review file.

It must appear in **two places**:
- **Hook** — as a provocation, a contradiction, or an unanswered question that makes it feel urgent
- **Resolution** — stated directly, now earned by the story

Never leave it implicit in both. At minimum, state it explicitly in the resolution.

## SCR structure

**Situation** (~150 words)
Ground the reader. Who, where, when, what was at stake. Specific — name the company, the role, the moment. Avoid generic setup ("In an era of AI transformation...").

**Complication** (~200 words)
The sharp turn. What went wrong, what was revealed, what the situation demanded. This is where vivid descriptors matter most — the complication must *feel* hard, not just sound hard. Place the source quote here or in the resolution.

**Resolution** (~150–200 words)
What happened, what was learned. Restate the central message — now with weight behind it. End on a single clean implication for the reader. One sentence. Make it land.

## Hook

The first 1–2 sentences of the body. Must earn the read.

**Pass:** Would a senior leader stop scrolling? Does it create tension, contradiction, or recognition? Is it specific? ("The model worked in demo. It never worked after that.")

**Fail:** Scene-setting openers. Rhetorical questions. "In [year], AI changed..."

## Vivid descriptors

Specificity is the descriptor. Concrete over adjective.

- ❌ "It was a difficult situation"
- ✅ "Three engineers stared at a model that had worked perfectly for six weeks and now returned nonsense for a third of queries"

Numbers, names, stakes. Avoid: "rapidly," "increasingly," "significant." If you can't be specific, be short.

## Quote

Include at least one direct quote from the source. Place it in the complication or resolution — where it lands hardest. Block quote or inline with attribution, never paraphrased and attributed as a quote.

## Word count

Target: 500–600 words (body array concatenated). If over: trim the complication first. If under: deepen the situation or sharpen the resolution — never pad.

## Tone

Direct and declarative. Short sentences when stating truths. No hype. No hedging unless the source hedges.

Write from the reader's perspective: under pressure, looking for signal, wary of being sold to. Earn trust through specificity and honesty.

Empathy without softness. Grit without bravado.
