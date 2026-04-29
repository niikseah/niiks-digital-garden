# Garden — niik's digital garden (public site) UI kit

A hi-fi recreation of the public-facing garden. Click-thru prototype covering:

- **Home** — aurora hero + six-up note grid + reading log
- **Essay** — long-form reader view (open any note card)
- **Reading** — the booklist in isolation
- **Now**, **About** — short pages

## Files

- `index.html` — entry point, routes between views
- `Nav.jsx` — sticky top nav with wordmark, link rail, ⌘K chip, day/night toggle
- `Hero.jsx` — aurora-backed landing hero
- `NoteCard.jsx` — the note card used across the site; includes state badge (seedling / budding / evergreen / uprooted)
- `ReadingList.jsx` — the reading log row/list
- `Home.jsx` — composes hero + notes grid + reading
- `Footer.jsx` — quiet two-row footer + the `Essay` long-read view
- `garden.css` — all site-specific styles (imports `../_kit.css` via the HTML)

Use `_kit.css` for shared primitives (button, card, chip, input, kbd).
