# niik's digital garden — Design System

A personal digital garden for **niik** — a quiet, unhurried corner of the internet for essays, field-notes, reading logs, and half-finished ideas left to grow. The system pairs **midnight blues** with **electric accents** and a classic **Apple Garamond + Helvetica Neue** voice, reaching for a whimsical-minimalism that feels more like a moleskin held up to a night sky than a SaaS dashboard.

> _"A garden grows in public. Notes wander. Some die back; some bloom. Everything is a draft."_

---

## Sources

This system was seeded from a single mounted codebase:

- **`design-system/`** — colors_and_type.css (tokens + semantic defaults) and a full set of self-hosted webfonts (Apple Garamond + Helvetica Neue, both provided as TTF/OTF).

No Figma links, slide decks, or production code were attached. The UI kit and sample screens in this project are therefore **net-new recreations** designed _against_ the provided tokens and voice — they should be treated as a starting canon rather than a mirror of live product. Flag anything that drifts from your intent.

---

## Products in scope

niik's digital garden is a single product expressed as two surfaces:

1. **The Garden (web)** — the public site. Essays, notes, reading log, "now" page, about. A mostly-static, deeply readable surface.
2. **The Greenhouse (writing app)** — a personal writing environment for drafting, pruning, and replanting notes. Unified sidebar, markdown composer, tag/link graph.

Both share one token surface — the Greenhouse is the Garden after dark with editing affordances turned on.

---

## Index (manifest)

Root files:

- `README.md` — this file. Overview, content, visual foundations, iconography.
- `SKILL.md` — Agent-Skills-compatible entry point for Claude Code.
- `colors_and_type.css` — **the single source of truth** for tokens + semantic element defaults. Import this in every artifact.
- `fonts/` — Apple Garamond (6 cuts), Helvetica Neue (16 cuts), `fonts.css` @font-face manifest. JetBrains Mono pulled from Google Fonts.
- `assets/` — logomarks, favicons, ornaments, placeholder imagery.
- `preview/` — small HTML cards populating the Design System tab.
- `ui_kits/` — high-fidelity recreations, one folder per surface.
  - `ui_kits/garden/` — the public site (index.html + JSX components).
  - `ui_kits/greenhouse/` — the writing app (index.html + JSX components).

---

## Content Fundamentals

The voice is **first-person, unhurried, and slightly literary** — closer to a personal journal than product copy. It should feel handwritten even when it isn't.

**Person & address.**
- First-person **"I"**, second-person **"you"** when addressing the reader directly. Never "we" — there is no team here.
- Names: the site is **niik's digital garden** (lowercase _niik_, Apple Garamond italic where display allows). Never _Niik_. Never _NIIK_.

**Tone.**
- Warm, curious, a little wry. Prefers the specific detail to the grand claim.
- "I've been thinking about…" over "This post explores…"
- "I don't know yet" is allowed and preferred to pretending you do.
- Never urgent. Never sales-y. Never exclamatory — a single `!` is a budget for a whole week.

**Casing.**
- **Sentence case everywhere.** Page titles, section headers, buttons, menu items.
- Lowercase the brand name: `niik's digital garden`.
- Title Case reserved for proper nouns and book/essay titles mentioned inside copy.

**Punctuation & rhythm.**
- Em dashes — welcome — used as breath marks.
- Oxford commas, always.
- Ellipses are fine; one per paragraph maximum.
- Contractions: yes ("it's", "I'm", "don't"). The voice is spoken.
- Numbers under ten spelled out in prose ("three notes", "7.2 °C" when quoting data).

**Emoji.**
- **No emoji in product UI.** No 🌱, no ✨, no 💡 — the temptation to paint a digital garden with them is strong; resist it.
- The only allowed decorative glyphs are typographic: `—`, `·`, `→`, `§`, `†`, `✳`, `❋`, `✺` (used very rarely, as ornaments, not icons).
- Unicode arrows `→` `↗` `↩` `↷` are permitted inside running text as meaningful connectors.

**Examples.**

| Good | Avoid |
|---|---|
| "Three notes that are slowly becoming an essay." | "🌱 3 new notes just dropped!" |
| "Last updated — two Tuesdays ago." | "Updated 2d ago" |
| "I'm planting this half-thought here to return to." | "Save draft" (as a primary CTA) |
| "Read on" / "Go to note" | "Click here" / "Learn more" |
| "This is unfinished on purpose." | "Coming soon!" |

**Microcopy pattern.**
Empty states get a sentence, not a graphic. Error states apologise in first person ("I seem to have lost this page."). Loading states prefer an em-dash pulse to a spinner where feasible.

---

## Visual Foundations

### The overall vibe
**Night-sky study.** Deep midnight backgrounds, a single electric-blue accent used with discipline, generous negative space, and type that does most of the work. Imagery is warm and grainy. Everything breathes.

## Modes — Electric (default) &amp; Night

Two modes, equal citizens — but the **default is Electric/Paper**.

- **Electric / Day (default)** — warm `--paper-50` canvas, ink-dark text, electric blues for accents and links. This is what visitors see on first load.
- **Night** — deep midnight canvas, off-white ink, glowing electric highlights. Opt-in via `data-theme="night"` on `<html>`, **or** the visitor has OS dark mode on (we respect `prefers-color-scheme: dark` unless `data-theme="day"` is explicitly set).

```html
<html data-theme="night">   <!-- force night -->
<html data-theme="day">     <!-- force day, even on OS dark -->
<html>                      <!-- default: day, unless OS is dark -->
```

Three colour families:
1. **Midnight** (7 stops) for Night-mode structure: backgrounds, cards, borders.
2. **Electric** (9 stops) for intent: primary actions, links, selection, the halo on focused elements. **This is the brand accent in both modes.**
3. **Paper &amp; ink** (7 stops) for Day-mode surfaces &amp; type.
4. **Garden semantic** — a small, soft palette used _sparingly_ to tag meaning:
   - `--moss` — seedling / fresh
   - `--bloom` — budding / in progress
   - `--amber` — evergreen / featured
   - `--rose` — destructive / removal

Never use the garden palette as decoration — only as signal. A card with a green stripe means _something_, not _visual interest_.

### Typography

- **Display** — Apple Garamond, weights 300/400/700 + italic cuts. Used for H1–H3, pull-quotes, and the site wordmark. Italic is **not optional for flourish** — it is how the brand speaks emphatically.
- **Body** — Helvetica Neue, the full weight range. Default body is Roman (400), 16–17 px, 1.6 line-height.
- **Mono** — JetBrains Mono for code, keyboard keys, timestamps, and very short metadata.
- **Scale** — fluid, 7 steps (`--step--1` → `--step-5`). Display uses steps 3–5; body is step 0.
- **Rules** — tight negative letter-spacing on display (`-0.015em` → `-0.025em`). Body copy capped at `62ch`. Eyebrows are Helvetica, all-caps, `0.14em` tracking. **Never mix two weights of Garamond in the same word-group** — let the italic do the work.

### Spacing

A 4 + 8 hybrid scale (`--s-1` = 4 px through `--s-10` = 144 px). The system _likes_ to be loose — prefer `--s-6`/`--s-7` between sections, `--s-4`/`--s-5` between card innards. Tight layouts are a smell.

### Radii

Four sizes + pill. The canonical card radius is `--radius-3` (14 px). `--radius-4` (22 px) for hero/large cards. Small chips and inputs use `--radius-2` (8 px). Pills (`999px`) are reserved for badges/tags, never buttons.

### Backgrounds

Three distinct background treatments:
1. **Paper** — `--bg-1` on day/default. Warm off-white, almost no ornament. Most pages.
2. **Flat midnight** — `--bg-1` resolves to midnight when night mode is active.
3. **Aurora** — `.aurora-bg` class. A blurred radial mesh (electric stops) + grain overlay. Used for hero sections and empty states. Looks different but valid in both modes.

Imagery, when used, is **warm, grainy, filmic**. Sunrise/dusk palettes preferred. Black-and-white is welcome. Heavy saturation and crisp digital photography are not the brand. Full-bleed hero photographs are permitted on individual essay pages; never on index pages.

### Grain & texture

A subtle noise overlay is baked into `.aurora-bg` via an inline `feTurbulence` SVG at 18% opacity + `mix-blend-mode: overlay`. That same recipe can be applied to any dark surface that needs a touch of analogue.

### Borders

Borders are **glowing hairlines**, not boxes. The border tokens are all alpha-blue:
- `--border-1` (10% alpha) — default card edge, barely-there
- `--border-2` (18% alpha) — hover / focus
- `--border-strong` (32% alpha) — separated sections

Dashed 1 px dividers for `<hr>`. Solid 2 px `--electric-400` left-border on blockquotes — this is the **only** place a coloured left-border accent is allowed.

### Shadows & glow

Two shadow systems, used with distinction:
- **Shadow** (`--shadow-1/2/3`) — neutral drop shadows for things that sit on paper/day surfaces.
- **Glow** (`--glow-sm/md/lg`) — electric-blue outer glows for focused/primary elements on night surfaces. `--glow-sm` is the default _focus ring_.

A card on night mode leans on the `--border-1` hairline + a soft inner glow on hover, not a drop shadow.

### Motion

- **Easings.** `--ease-out` (cubic-bezier(.2,.7,.2,1)) for everything default. `--ease-spring` (subtle overshoot) for the small flourishes — a bookmark settling, an empty state landing.
- **Durations.** `--dur-1` 120 ms (micro-feedback), `--dur-2` 200 ms (hover/state), `--dur-3` 320 ms (page transitions), `--dur-4` 520 ms (hero moments).
- **Philosophy.** Fades and gentle slides. No bounces, no parallax, no scroll-triggered cinematography. The garden doesn't hustle.

### Hover & press

- **Hover** — colour shift only, never scale. Links brighten to `--fg-link-hover`. Cards grow a `--border-2` ring + `--glow-sm`. Buttons lighten by ~8% OKLCH L.
- **Press** — 98% scale + 120 ms ease-out. No ripple, no colour flip.
- **Focus-visible** — `--glow-sm` halo, always. Never the browser default.

### Transparency & blur

- `backdrop-filter: blur(14px) saturate(1.4)` is reserved for the top nav and modal scrims. Don't sprinkle it.
- Semi-transparent fg tokens (`--fg-2/3/4`) handle hierarchy _inside_ text. Don't use opacity on wrappers — it flattens accents.

### Cards

The canonical card:
```
background: var(--bg-3);
border: 1px solid var(--border-1);
border-radius: var(--radius-3);
padding: var(--s-5);
```
On hover: `border-color: var(--border-2); box-shadow: var(--glow-sm);` with a 200 ms ease-out. No lift, no rotate.

### Layout rules

- Max content width **72ch** for essays, **1200 px** for product surfaces.
- Top nav is sticky, `backdrop-blur`, 64 px tall, `--border-1` bottom hairline.
- Footer is quiet — two rows, small type, no wall of links.
- Grid is 12-col on desktop, 4-col on tablet, single-col on phone, with `--s-5` gutters.

---

## Iconography

**Stroke icons, Lucide-style.** The Garden uses a single icon family: **Lucide** (same lineage as Feather) at **1.5 px stroke, 20 px default size, currentColor.** Outlined only — no filled variants. We currently pull them from **the `lucide` CDN** (`https://unpkg.com/lucide@latest`) rather than a bundled icon font.

> **Substitution flag.** The attached codebase did not include a bundled icon set, so Lucide is an agent-chosen substitute matched to the brand's hairline-stroke aesthetic. If niik has a preferred icon family, swap it globally and I'll update the UI kits.

**Rules.**
- Icons sit on the optical baseline of body copy, not above.
- Icons follow text colour via `currentColor` — never paint them brand blue standalone. The blue is for the glow, not the glyph.
- Always pair icons with a text label on primary actions. Icon-only buttons are allowed only on toolbars and must carry `aria-label`.

**No emoji in UI.** (Repeated for emphasis — see Content Fundamentals.)

**Unicode glyphs used as ornament (not as icons):**
`—` em-dash · `·` middle-dot (between meta items) · `→` right-arrow (links forward in text) · `§` section · `❋` asterism (used once per page maximum) · `✺` rosette (reserved for the "featured" evergreen marker).

**Logomark.** A small hand-drawn `niik` wordmark + a tiny rosette `✺` ornament. See `assets/logomark.svg`. The lockup is always lowercase, Apple Garamond italic, with the rosette set at cap-height distance to the right.

---

*Last tended — 2026.*
