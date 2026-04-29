# Greenhouse — niik's writing app UI kit

The private writing environment. Three-pane layout:

- **Sidebar** — brand, ⌘K search, notes list (state-dotted), tag chips.
- **Composer** — topbar (state badge, save indicator, publish), title input, markdown body with blockquote.
- **Inspector** — metadata, backlinks, actions (archive / uproot).

## Files

- `index.html` — entry, three-pane grid, click-to-switch notes.
- `Greenhouse.jsx` — `Sidebar`, `Composer`, `Inspector` components.
- `greenhouse.css` — three-pane layout + list + composer styles.

The app is forced into `data-theme="night"` — midnight is the writing mood.
