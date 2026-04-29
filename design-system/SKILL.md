---
name: niik-garden-design
description: Use this skill to generate well-branded interfaces and assets for niik's digital garden, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick map
- `README.md` — brand overview, content fundamentals, visual foundations, iconography
- `colors_and_type.css` — the single source of truth for tokens + semantic element defaults (import this first)
- `fonts/` — Apple Garamond + Helvetica Neue (self-hosted, all weights)
- `assets/` — logomark, favicon, rosette
- `preview/` — small specimen cards for every token / component group
- `ui_kits/garden/` — hi-fi public-site recreation (hero + notes + essay)
- `ui_kits/greenhouse/` — hi-fi writing-app recreation (three-pane editor)

## Rules the brand cares about
- **Default mode is Electric/Paper** (warm off-white + ink). Night mode (midnight + electric glow) is opt-in via `data-theme="night"` or OS dark mode.
- **No emoji in UI.** Ever. Typographic glyphs only (`—`, `·`, `→`, `§`, `✺`, `❋`).
- **Sentence case everywhere.** Brand name is always lowercase: `niik's digital garden`.
- **Icons:** Lucide, 1.5 stroke, currentColor — outlined only, no fills.
- **Display type** is Apple Garamond italic. Body is Helvetica Neue Roman. Mono is JetBrains Mono.
- **Blockquote** is the only place a coloured left-border is allowed.
- Voice is first-person, unhurried, a little literary. No urgency, no exclamation.
