# Fusion Scanner
### An AI-powered browser extension that helps multilingual readers comprehend dense English text

**Role:** Product Designer & Researcher (Team of 5)
**Timeline:** 12 weeks · Academic project, CS3240 (Interaction Design)
**Tools:** Figma, Google Forms, Excel (heuristic audit)
**My contributions:** [CONFIRM — e.g., led usability testing, designed the Summarise panel flow, owned the heuristic evaluation, etc.]

---

## TL;DR

Multilingual readers — international students, immigrants, language learners — routinely abandon dense English articles because comprehension friction outweighs payoff. We designed **Fusion Scanner**, a browser extension that layers AI summarisation, in-context definitions, and exportable annotations onto any web page.

After two rounds of testing (5 usability participants + heuristic audit against Weinschenk's principles), we shipped **9 design changes** that resolved every major (severity 3) heuristic violation we identified. The strongest signal: all five testers completed all four core tasks, and three of five spontaneously asked when the tool would be available to use.

---

## The Problem

Reading is the primary on-ramp to knowledge — but for the [CONFIRM — e.g., 1.5B+ people who read English as a second language], it's also a tax. Dense vocabulary, unfamiliar idioms, and long-form structure compound into a comprehension barrier that pushes readers away from the content most likely to inform them.

Existing tools force a tradeoff:
- **Translation tools** flatten nuance and break flow.
- **Dictionary lookups** require leaving the page.
- **Summarisers** (TL;DR generators) replace the source instead of supporting it.

None of them respect the way real readers work: skimming, doubling back, defining a word, annotating a thought, and returning to the original text.

**The opportunity:** a tool that *augments* reading without replacing it.

---

## Who We Designed For

We ran contextual inquiry with 5 users spanning our two priority segments:

**Primary** — Multilingual readers (international students, new immigrants, language learners) who read English daily but encounter unfamiliar vocabulary "often" or "always."

**Secondary** — Power readers who'd benefit from comprehension scaffolding regardless of language background: academic researchers, language tutors, and (notably) one participant with ADHD whose adaptive reading strategies surfaced design insights we hadn't anticipated.

The CI sessions produced affinity diagrams, sequence models, and interaction models. Three patterns dominated:

1. **Selective reading is universal.** Readers skip, re-read, and triage — even fluent ones. Designing around linear consumption ignores how reading actually works.
2. **Distraction has two sources** — internal (unknown words pull attention) and external (page layout, images). A reading tool has to address both.
3. **Annotations are valued but rarely used** because existing tools make them clunky. Lower the friction and adoption follows.

These three insights drove our three core features.

---

## The Solution: Three Panels, One Extension

| Panel | What it does | Why it earned its place |
|---|---|---|
| **Summarise** | AI-generated key themes + quick summary, with selective regeneration and feedback loop | Addresses the "long article = abandon" failure mode |
| **Define** | Hover-to-define for unfamiliar words; AI explanations on demand; saves definitions back into the article | Removes the "leave the page to look up a word" interruption |
| **Annotate** | Rich-text annotations that drag-and-drop onto specific paragraphs; export the article + annotations as PDF | Turns reading from passive consumption into a knowledge-capture workflow |

### Why a browser extension, not a standalone app?

Two reasons. First, our CI showed that 4 of 5 participants did most of their reading inside a browser — research papers, news, blogs. Pulling them into a separate app would have introduced exactly the friction we were trying to remove. Second, an extension lets us layer *over* the source content rather than replace it, which preserved the "augment, don't replace" principle.

### Why AI for summarisation, given hallucination risk?

We debated this. The alternative — extractive summarisation (pulling existing sentences) — is safer but produces choppy results that don't help readers struggling with the original prose. We chose generative AI and mitigated the risk through three design decisions:

- **Granular regeneration** (Key Themes and Quick Summary refresh independently) so users aren't forced to discard a good output to fix a bad one.
- **Feedback-before-regenerate** flow that asks users *what* they didn't like before re-running the model, so the regeneration is targeted, not random.
- **"Where-Is" indicator** that highlights the source paragraph each key theme came from, so users can verify the summary against the source.

The third one is particularly worth flagging: heuristic evaluation flagged it as low-impact, but we kept it because *trust in AI output is the long-term moat*, not novelty.

---

## The Evaluation

We used two complementary methods because each catches what the other misses:

**Usability testing (n=5)** catches comprehension failures and emotional reactions but is expensive and noisy.
**Heuristic evaluation** (Weinschenk's psychological usability heuristics, Nielsen's 10) catches systematic violations but misses what real users actually feel.

### Recruitment

A 7-question screener (n=15 respondents) filtered for native language, English proficiency (1–5), reading frequency, encounters with unfamiliar vocabulary, and tolerance for long text. We deliberately picked 5 participants with **varied** profiles — native English speakers alongside Chinese, Korean, and Vietnamese speakers; proficiency scores from 2 to 3; preferences from "would prefer shorter text" to "doesn't mind long text" — so feedback wouldn't cluster around a single archetype.

### Tasks tested
1. Generate a summary, regenerate it, provide feedback (Key Task 1)
2. Define an unfamiliar word — "Solemnly" (Key Task 2)
3. Find and activate a less-prominent feature: Bionic Reading (placement test)
4. Write an annotation, attach it to the article, export the result (Key Task 3)

---

## What We Found, and What We Did About It

### Major issues fixed

**1. The "From Highlighted" toggle had no clear mental model** *(Nielsen H1 — Visibility of System Status)*
Users couldn't tell which summary they were looking at. We replaced the toggle dot with an explicit `Back to Full Summary` action button — the state is now in the label, not in a coloured indicator.

**2. Regeneration was irreversible without warning** *(H3 — User Control / H5 — Error Prevention)*
We added a destructive-action confirmation, *and* split regeneration into two independent buttons (Key Themes and Quick Summary) so users could keep the half they liked.

**3. Feedback came after regeneration, when it was too late to help** *(H1)*
Reordered the flow: feedback input now appears *before* regeneration, so the model has direction. Small change, large logical-flow improvement.

**4. No success/error states** *(H1, H9)*
Added confirmation toasts ("Added to Article!") and contextual error messages ("You haven't highlighted anything!") at the moment of action.

**5. Heavy under-documentation** *(H10 — Help & Documentation)*
Added a help button to all three panels (previously only on Define), plus inline microcopy ("Drag and drop annotations on the article") to reduce the need for documentation in the first place.

**6. Settings were buried per-panel** — moved to the top-level navigation so they apply to the whole extension, matching users' mental model.

**7. Inconsistent panel headers** — Define had one, Summarise and Annotate didn't. Standardised.

**8. Export flow was redundant** — "Save" and "Export as PDF" did roughly the same thing. Merged them and added a PDF preview so users know what they're getting before they commit.

**9. Pop-ups lacked close buttons.** Added them. Trivial fix, surprisingly impactful for perceived control.

### What we deliberately didn't fix

- **Dynamic article zoom-out** — Figma prototype limitation, not a design decision. Flagged for engineering.
- **"Where-Is" feature** — one participant called it unclear, but two others found it useful. We kept it because the cost of inclusion is low and the trust-in-AI payoff is high. *(This is the kind of tradeoff call I'd make again.)*
- **Drag-and-drop animation polish** — Figma can't render this faithfully. We documented it as a spec for handoff rather than over-investing in prototype fidelity.

---

## Outcomes

> **Caveat:** these are academic-project outcomes from a 5-person test, not production metrics. I report them as evidence of design improvement, not market validation.

- **Task completion: 4/4 across all 5 participants.** Every key task completed without facilitator intervention.
- **Heuristic violations: [CONFIRM — e.g., "all 4 severity-3 violations resolved; X of Y minor violations addressed"]** — based on re-running the audit after redesign.
- **Qualitative signal:** 3/5 participants described the tool as something they'd want to use, citing the AI integration and visual design. Praise clustered around three themes: design intuitiveness, visual restraint, and AI usefulness.
- **Negative feedback that drove iteration:** representation of mode states, lack of customisation, missing help/error messaging — all addressed in the v2 redesign.

---

## What I'd Do Differently

- **Define success metrics before testing, not after.** We evaluated against heuristics (good) but never set targets like "task completion ≥ 80%" or "SUS ≥ 70." That made our "did we succeed?" answer softer than it needed to be.
- **Test the AI quality, not just the AI UX.** We tested whether users could *use* the summariser. We didn't test whether the summaries were *good*. In a real ship, those are equally important.
- **Recruit one more participant from the primary segment.** Our n=5 leaned slightly toward power-readers; the multilingual learners we were primarily designing for were 3 of 5.
- **Wireframe before high-fidelity.** Several of the heuristic violations we caught (button affordances, mode confusion) would have been cheaper to find at a lower fidelity.

---

## What I Took Away

This project sharpened three instincts I now apply to every design problem:

1. **Two evaluation methods beat one.** Usability tests catch the felt experience; heuristics catch the structural debt. Skipping either leaves a blind spot.
2. **Mental model > visual cleverness.** The "From Highlighted" toggle was visually elegant and functionally confusing. Plain language ("Back to Full Summary") wins.
3. **AI features need trust scaffolding.** Granular controls, source citations, and feedback loops aren't nice-to-haves — they're the difference between an AI feature people use once and one they integrate into a workflow.

---

*Built with: Chin Jun An, Niik Seah, Ning Xinran, Zhewen Zachary Tao, Tang Weichun. Course: CS3240, NUS, supervised by Prof. Zhao Shengdong and TA Aakansha.*
