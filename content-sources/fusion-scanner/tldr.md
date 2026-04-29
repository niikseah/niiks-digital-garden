# Fusion Scanner — TL;DR

**An AI-powered browser extension that helps multilingual readers comprehend dense English text.**

**Role:** Product Designer & Researcher · **Team:** 5 · **Timeline:** 12 weeks · **Tools:** Figma

---

### Problem
Multilingual readers — international students, immigrants, language learners — abandon dense English content because comprehension friction outweighs payoff. Existing tools force a tradeoff: translators flatten nuance, dictionaries break flow, summarisers replace the source instead of supporting it.

### Solution
A browser extension with three panels that **augment** reading instead of replacing it:
- **Summarise** — AI-generated key themes + quick summary, with granular regeneration and a feedback loop
- **Define** — hover-to-define unfamiliar words, save definitions back into the article
- **Annotate** — rich-text notes that drag onto specific paragraphs, exportable as PDF

### Approach
Contextual inquiry with 5 users → affinity diagrams → mid-fidelity Figma prototype → **two-track evaluation**: usability testing (n=5, screened from 15) + heuristic audit against Weinschenk's principles → 9 design changes shipped.

### Key design decisions
- **Feedback before regeneration**, not after — so the AI has direction, not random retries
- **Granular regeneration** (Key Themes and Quick Summary refresh independently) — keeps the half users liked
- **"Back to Full Summary"** replaced an ambiguous toggle dot — state goes in the label, not a colour
- **Source-paragraph indicator** for AI summaries — trust in AI output is the long-term moat

### Outcomes
- **4/4 task completion** across all 5 usability participants
- **Every severity-3 heuristic violation resolved** in the v2 redesign
- 3 of 5 participants asked when the tool would ship
- Negative feedback (mode confusion, missing error states, sparse documentation) drove every major iteration

### What I'd do differently
Define success metrics *before* testing, evaluate AI quality (not just AI UX), and wireframe before going high-fidelity.

→ **[Read the full case study]**
