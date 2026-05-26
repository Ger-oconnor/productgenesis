# Product Genesis — Source

A single-page React (via inline JSX + Babel) site for Product Genesis.

## Files

- `index.html` — entry point; loads fonts, CSS, and the JSX bundle.
- `styles.css` — all styling. Look here for colors, fonts, layout.
- `app.jsx` — main React app: header, hero (3 variants), feed, category sections, inline post-expand, newsletter, about, footer, Tweaks panel.
- `data.js` — content: categories + all posts. **Add new posts here.**
- `tweaks-panel.jsx` — the in-page Tweaks panel scaffolding (you can usually ignore this).

## Run locally

No build step. Just serve the folder:

```bash
# any static server works; e.g.:
npx serve .
# or
python3 -m http.server 8000
```

Open `http://localhost:8000` (or whatever port the server prints).

## Continuing in Claude Code

1. Unzip this folder somewhere on your machine.
2. `cd` into the folder and run a static server (see above).
3. Open the folder in Claude Code:
   ```bash
   claude
   ```
4. Ask Claude Code to edit `data.js` to add new posts, or `styles.css` / `app.jsx` for design changes. The dev loop is: edit a file → refresh the browser tab.

## Adding a new post

Open `data.js`, find the `window.PG_POSTS = [ ... ]` array, and add an object like:

```js
{
  id: "v4",                                   // unique id
  cat: "vision",                              // category id (see PG_CATEGORIES)
  sub: "discovery",                           // optional — only for development
  type: "essay",                              // essay | note | video | case-study | thought
  title: "Your post title.",
  dek: "One-sentence summary that shows under the title on cards.",
  date: "May 20, 2026",
  read: 6,                                    // reading time in minutes
  feature: false,                             // true = make this the big featured card in its section
  tone: "ink",                                // optional — 'ink' | 'accent' | 'warm' | 'sand' | omit
  body: [
    "First paragraph.",
    "Second paragraph.",
    "And so on.",
  ],
  // Video-only fields:
  // videoLength: "12:04",
}
```

## Stack / decisions

- React 18 via UMD (no bundler). All JSX is transpiled in the browser by `@babel/standalone`.
- Fonts: Poppins (from Google Fonts).
- Colors: defined as CSS custom properties in `styles.css`; the `Tweaks` panel can switch between several surface presets at runtime.
- No backend. The newsletter form, reactions, share buttons, and comments are all client-only mocks — wire them to a real service when you're ready.

If you eventually want a build step (Vite + real React), the JSX is already vanilla — moving it into a Vite project is mostly: install React, change `<script type="text/babel">` to a normal import, and remove the Babel CDN script.
