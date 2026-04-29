import React, { useState, useEffect, useCallback } from "react";
import { Users, Layers, Hand, MessageCircle, Calendar, AlertCircle } from "lucide-react";

/** Maps each numbered `<Section>` tile to which nav pill is highlighted while it is current. */
const SECTION_NAV_KEYS = ["problem", "approach", "approach", "decisions", "impact", "reflection"];
const SECTION_IDS = ["cs-section-1", "cs-section-2", "cs-section-3", "cs-section-4", "cs-section-5", "cs-section-6"];

const NAV_LINKS_FULL = [
  { key: "tldr-toggle", label: "TL;DR", modeSwitch: true },
  { key: "problem", label: "Problem" },
  { key: "approach", label: "Approach" },
  { key: "decisions", label: "Decisions" },
  { key: "impact", label: "Impact" },
  { key: "reflection", label: "Reflection" },
];

const SECTION_ANCHORS = {
  problem: "cs-section-1",
  approach: "cs-section-3",
  decisions: "cs-section-4",
  impact: "cs-section-5",
  reflection: "cs-section-6",
};

export default function FlexijioCaseStudy() {
  const [view, setView] = useState("full"); // "full" or "tldr"
  const [scrollY, setScrollY] = useState(0);
  /** Which section nav pill reflects scroll position (full view); in TL;DR-only state not used visually the same way. */
  const [scrollNavKey, setScrollNavKey] = useState("problem");

  useEffect(() => {
    const onScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (view !== "full") return undefined;

    const sectionEls = SECTION_IDS.map((id) => document.getElementById(id)).filter(Boolean);
    if (sectionEls.length === 0) return undefined;

    const navKeyById = Object.fromEntries(SECTION_IDS.map((id, idx) => [id, SECTION_NAV_KEYS[idx]]));

    const updateFromRects = () => {
      const viewportBand = Math.max(120, Math.min(window.innerHeight * 0.35, 280));
      let bestId = sectionEls[0].id;
      let bestScore = Number.POSITIVE_INFINITY;
      sectionEls.forEach((el) => {
        const rect = el.getBoundingClientRect();
        const score = Math.abs(rect.top - viewportBand);
        if (score < bestScore) {
          bestScore = score;
          bestId = el.id;
        }
      });
      setScrollNavKey(navKeyById[bestId] || "problem");
    };

    updateFromRects();

    const observer = new IntersectionObserver(
      () => {
        updateFromRects();
      },
      {
        root: null,
        threshold: [0, 0.1, 0.25, 0.5, 0.75, 1],
        rootMargin: "-15% 0px -55% 0px",
      },
    );
    sectionEls.forEach((el) => observer.observe(el));

    window.addEventListener("scroll", updateFromRects, { passive: true });
    window.addEventListener("resize", updateFromRects, { passive: true });

    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", updateFromRects);
      window.removeEventListener("resize", updateFromRects);
    };
  }, [view]);

  const scrollToAnchor = useCallback((id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }, []);

  const onNavClick = useCallback(
    (item) => {
      if (item.modeSwitch) {
        setView("tldr");
        window.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
      const id = SECTION_ANCHORS[item.key];
      if (!id) return;
      const goScroll = () => {
        scrollToAnchor(id);
      };
      if (view === "full") {
        goScroll();
        return;
      }
      setView("full");
      requestAnimationFrame(() => {
        requestAnimationFrame(goScroll);
      });
    },
    [scrollToAnchor, view],
  );

  /** Active pill style: TL;DR in tldr view, or scroll spy when full. */
  const isNavActive = (item) => {
    if (item.modeSwitch) return view === "tldr";
    if (view === "full") return scrollNavKey === item.key;
    return false;
  };

  // Brand palette (60-30-10)
  // 60% neutral: #FAFAF7 (paper), #FFFFFF, ink
  // 30% brand blues: #1E3A8A (deep), #3B82F6 (mid), #DBEAFE (mist)
  // 10% star/accent: #FCD34D (warm gold star)

  const Star4 = ({ className = "", size = 14, fill = "#FCD34D", style }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} style={style} aria-hidden="true">
      <path d="M12 0 L13.5 10.5 L24 12 L13.5 13.5 L12 24 L10.5 13.5 L0 12 L10.5 10.5 Z" fill={fill} />
    </svg>
  );

  return (
    <div className="min-h-screen" style={{ backgroundColor: "#FAFAF7", color: "#0A1428", fontFamily: "Georgia, 'Times New Roman', serif" }}>
      {/* Floating star easter eggs — sparse, appear on scroll */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 1 }}>
        <Star4 className="absolute" size={8} fill="#3B82F6" style={{ top: "12%", left: "6%", opacity: 0.4, transform: `translateY(${scrollY * 0.08}px)` }} />
        <Star4 className="absolute" size={6} fill="#FCD34D" style={{ top: "28%", right: "8%", opacity: 0.5, transform: `translateY(${scrollY * 0.12}px)` }} />
        <Star4 className="absolute" size={10} fill="#1E3A8A" style={{ top: "55%", left: "4%", opacity: 0.3, transform: `translateY(${scrollY * 0.06}px)` }} />
        <Star4 className="absolute" size={7} fill="#FCD34D" style={{ top: "78%", right: "5%", opacity: 0.45, transform: `translateY(${scrollY * 0.1}px)` }} />
      </div>

      {/* Sticky chrome + TL;DR / Full + scrollspy section rail */}
      <header
        className="sticky top-0 z-50 topbar backdrop-blur-md flex flex-col"
        style={{
          backgroundColor: "rgba(250, 250, 247, 0.9)",
          borderBottom: "1px solid #E5E7EB",
        }}
      >
        <div className="topbar-inner max-w-5xl mx-auto w-full px-6 py-4 flex items-center justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-2 min-w-0">
            <Star4 size={14} fill="#1E3A8A" />
            <span style={{ fontFamily: "Georgia, serif", fontSize: "15px", letterSpacing: "0.02em", color: "#1E3A8A" }}>
              <span style={{ fontWeight: 700 }}>Flexijio</span> · Case Study
            </span>
          </div>
          <div className="flex items-center gap-1 p-1 rounded-full shrink-0" style={{ backgroundColor: "#F3F4F6" }}>
            <button
              type="button"
              onClick={() => {
                setView("tldr");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className="px-4 py-1.5 rounded-full text-sm transition-all"
              style={{
                backgroundColor: view === "tldr" ? "#1E3A8A" : "transparent",
                color: view === "tldr" ? "#FFFFFF" : "#6B7280",
                fontFamily: "Georgia, serif",
              }}
            >
              TL;DR
            </button>
            <button
              type="button"
              onClick={() => setView("full")}
              className="px-4 py-1.5 rounded-full text-sm transition-all"
              style={{
                backgroundColor: view === "full" ? "#1E3A8A" : "transparent",
                color: view === "full" ? "#FFFFFF" : "#6B7280",
                fontFamily: "Georgia, serif",
              }}
            >
              Full Case Study
            </button>
          </div>
        </div>

        <div className="topbar-inner border-t max-w-5xl mx-auto w-full px-4 sm:px-6 pb-3 pt-1" style={{ borderColor: "rgba(229, 231, 235, 0.8)" }}>
          <nav aria-label="Case study sections">
            <ul className="flex flex-wrap items-center gap-0 gap-y-2 justify-end sm:justify-start text-[13px] sm:text-sm">
              {NAV_LINKS_FULL.map((item, idx) => (
                <li key={item.key} className="flex items-center">
                  {idx > 0 ? (
                    <span className="select-none px-2 text-neutral-400" aria-hidden style={{ fontFamily: "Georgia, serif" }}>
                      |
                    </span>
                  ) : null}
                  <button
                    type="button"
                    onClick={() => onNavClick(item)}
                    className="rounded-md px-2 py-1 transition-colors"
                    style={{
                      fontFamily: "Georgia, serif",
                      fontWeight: isNavActive(item) ? 600 : 400,
                      color: isNavActive(item) ? "#1E3A8A" : "#6B7280",
                      backgroundColor: isNavActive(item) ? "rgba(219, 234, 254, 0.85)" : "transparent",
                    }}
                  >
                    {item.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </header>

      {view === "tldr" ? <TldrView Star4={Star4} /> : <FullView Star4={Star4} />}

      {/* Footer */}
      <footer className="relative z-10 border-t mt-24" style={{ borderColor: "#E5E7EB", backgroundColor: "#FFFFFF" }}>
        <div className="max-w-5xl mx-auto px-6 py-12">
          <div className="flex items-start justify-between flex-wrap gap-6">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Star4 size={12} fill="#1E3A8A" />
                <span style={{ fontFamily: "Georgia, serif", fontWeight: 700, color: "#1E3A8A", fontSize: "14px" }}>Flexijio</span>
              </div>
              <p className="text-sm" style={{ color: "#6B7280", maxWidth: "400px", lineHeight: 1.6 }}>
                A social home-workout platform designed at NUS for the NM3243 User Experience Design course (AY23/24).
              </p>
            </div>
            <div className="text-sm" style={{ color: "#9CA3AF" }}>
              <p>Project Owner · Aung Khant Myat</p>
              <p className="mt-1">Team TW5-04 · 4 designers</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

// ============================================================================
// TL;DR VIEW — for recruiters with 60 seconds
// ============================================================================
function TldrView({ Star4 }) {
  return (
    <main className="relative z-10 max-w-5xl mx-auto px-6 pt-16 pb-12">
      {/* Eyebrow */}
      <div className="flex items-center gap-2 mb-6">
        <div style={{ width: "32px", height: "1px", backgroundColor: "#1E3A8A" }} />
        <span className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", fontFamily: "Georgia, serif", letterSpacing: "0.2em" }}>
          60-second read
        </span>
      </div>

      {/* Hero */}
      <h1 style={{ fontFamily: "Georgia, serif", fontSize: "clamp(40px, 6vw, 68px)", lineHeight: 1.05, fontWeight: 400, letterSpacing: "-0.02em", color: "#0A1428" }}>
        A home-workout platform that
        <br />
        <em style={{ color: "#1E3A8A", fontStyle: "italic" }}>turns isolation into community</em>
        <Star4 size={20} fill="#FCD34D" className="inline-block ml-3 -mt-8" />
      </h1>

      <p className="mt-8 text-xl" style={{ color: "#374151", lineHeight: 1.5, maxWidth: "720px", fontFamily: "Georgia, serif" }}>
        I led a 4-person team to design <strong style={{ color: "#1E3A8A" }}>Flexijio</strong> — a video-conferencing fitness app that lets friends work out together from anywhere, with personalized difficulty levels for mixed-ability groups.
      </p>

      {/* Quick stats grid */}
      <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-px" style={{ backgroundColor: "#E5E7EB" }}>
        {[
          { label: "Role", value: "Project Owner" },
          { label: "Team Size", value: "4 designers" },
          { label: "Timeline", value: "3 months, Feb 2024 - Apr 2024" },
          { label: "Method", value: "Double Diamond" },
        ].map((stat, i) => (
          <div key={i} className="p-6" style={{ backgroundColor: "#FAFAF7" }}>
            <div className="text-xs uppercase tracking-wider mb-2" style={{ color: "#9CA3AF", letterSpacing: "0.15em" }}>{stat.label}</div>
            <div style={{ fontFamily: "Georgia, serif", fontSize: "20px", color: "#0A1428", fontWeight: 500 }}>{stat.value}</div>
          </div>
        ))}
      </div>

      <div className="mt-16 max-w-4xl">
        <p className="text-base" style={{ color: "#374151", lineHeight: 1.7, fontFamily: "Georgia, serif" }}>
          FlexiJio is a fitness desktop video conferencing platform designed for office workers (18-63 years old) to engage in structured, community-driven workouts. It offers:
        </p>
        <ul className="mt-4 space-y-2 text-sm" style={{ color: "#4B5563", lineHeight: 1.7 }}>
          <li><strong style={{ color: "#1E3A8A" }}>Customizable Classes:</strong> Users can choose between expert or simplified exercise levels.</li>
          <li><strong style={{ color: "#1E3A8A" }}>Gamification & Engagement:</strong> Features like synced timers, music, and interactive elements enhance motivation.</li>
          <li><strong style={{ color: "#1E3A8A" }}>Community Support:</strong> Users can work out with friends or join public classes for accountability.</li>
        </ul>
      </div>

      {/* Problem · Solution · Impact — three columns */}
      <div className="mt-20 grid md:grid-cols-3 gap-12">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <div style={{ width: "24px", height: "24px", borderRadius: "50%", backgroundColor: "#DBEAFE", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ color: "#1E3A8A", fontWeight: 700, fontSize: "12px" }}>01</span>
            </div>
            <span className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>Problem</span>
          </div>
          <h3 style={{ fontFamily: "Georgia, serif", fontSize: "20px", lineHeight: 1.3, marginBottom: "12px", color: "#0A1428" }}>
            Home workouts are lonely, uncertain, and overwhelming.
          </h3>
          <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.6 }}>
            Users second-guess their form, drown in YouTube's endless choices, and lose motivation without social accountability. Existing tools like Zoom and Peloton each solve <em>part</em> of the problem — never all of it.
          </p>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-4">
            <div style={{ width: "24px", height: "24px", borderRadius: "50%", backgroundColor: "#DBEAFE", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ color: "#1E3A8A", fontWeight: 700, fontSize: "12px" }}>02</span>
            </div>
            <span className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>Solution</span>
          </div>
          <h3 style={{ fontFamily: "Georgia, serif", fontSize: "20px", lineHeight: 1.3, marginBottom: "12px", color: "#0A1428" }}>
            A "home studio" where friends co-train at their own level.
          </h3>
          <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.6 }}>
            Schedulable group sessions, instructor controls, raise-hand interactions, and — the USP I'm proudest of — <strong style={{ color: "#1E3A8A" }}>per-user difficulty scaling</strong> so beginners and athletes can train side-by-side.
          </p>
        </div>

        <div>
          <div className="flex items-center gap-2 mb-4">
            <div style={{ width: "24px", height: "24px", borderRadius: "50%", backgroundColor: "#FEF3C7", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Star4 size={10} fill="#1E3A8A" />
            </div>
            <span className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>Impact</span>
          </div>
          <h3 style={{ fontFamily: "Georgia, serif", fontSize: "20px", lineHeight: 1.3, marginBottom: "12px", color: "#0A1428" }}>
            Validated through 2 testing rounds and 10 heuristics.
          </h3>
          <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.6 }}>
            Iterated from lo-fi to hi-fi based on contextual inquiries, semi-structured interviews, controlled user testing, and Nielsen's heuristic evaluation — resolving <strong style={{ color: "#1E3A8A" }}>11 distinct usability issues</strong> across 5 priority categories.
          </p>
        </div>
      </div>

      {/* Skills demonstrated */}
      <div className="mt-20 p-10" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB", borderRadius: "2px" }}>
        <div className="text-xs uppercase tracking-widest mb-6" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>
          What this project demonstrates
        </div>
        <div className="grid md:grid-cols-2 gap-x-12 gap-y-4">
          {[
            { skill: "End-to-end UX process ownership", detail: "Research → synthesis → prototype → eval" },
            { skill: "Mixed-method user research", detail: "Contextual inquiry + semi-structured interviews + affinity mapping" },
            { skill: "Strategic product thinking", detail: "Identified inclusive-design extension as competitive moat" },
            { skill: "Iterative design discipline", detail: "Two prototype rounds, 11 heuristic-validated fixes" },
            { skill: "Stakeholder synthesis", detail: "Translated qualitative findings into 2 personas and use scenarios" },
            { skill: "Self-aware critique", detail: "Identified team's own bias toward aesthetics over interaction" },
          ].map((item, i) => (
            <div key={i} className="flex items-start gap-3 py-2">
              <Star4 size={10} fill="#FCD34D" className="mt-2 flex-shrink-0" />
              <div>
                <div style={{ fontFamily: "Georgia, serif", fontSize: "15px", color: "#0A1428", fontWeight: 600 }}>{item.skill}</div>
                <div className="text-sm mt-0.5" style={{ color: "#6B7280" }}>{item.detail}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Pull quote */}
      <div className="mt-20 max-w-3xl mx-auto text-center">
        <div className="text-5xl mb-4" style={{ color: "#DBEAFE", fontFamily: "Georgia, serif", lineHeight: 1 }}>"</div>
        <p style={{ fontFamily: "Georgia, serif", fontSize: "24px", lineHeight: 1.4, color: "#0A1428", fontStyle: "italic" }}>
          The biggest lesson: our first prototype over-indexed on aesthetics at the expense of interactions. The redesign forced me to lead with behavior, not visuals — a discipline I now bring to every brief.
        </p>
        <div className="mt-6 text-sm uppercase tracking-widest" style={{ color: "#9CA3AF", letterSpacing: "0.2em" }}>
          — Reflection, Week 13
        </div>
      </div>
    </main>
  );
}

// ============================================================================
// FULL VIEW — the in-depth read
// ============================================================================
function FullView({ Star4 }) {
  return (
    <main className="relative z-10 max-w-5xl mx-auto px-6 pt-12 pb-12">
      {/* Hero */}
      <Hero Star4={Star4} />

      {/* TOC */}
      <TableOfContents />

      {/* Section 1: Situation */}
      <Section sectionId="cs-section-1" number="01" label="Situation" title="At-home workouts solved one problem and created three new ones.">
        <p>
          When I joined the project, the at-home fitness market looked saturated — but the closer my team looked, the clearer the gaps became. <strong>YouTube</strong> offers infinite content with no live feedback. <strong>Zoom</strong> enables synchronous classes but provides no way to discover them. <strong>Peloton</strong> nails the experience but locks it behind a US$44/month subscription and proprietary hardware.
        </p>
        <p>
          The category had three unsolved problems: <em>users couldn't tell if their form was correct</em>, <em>they were paralyzed by content overload</em>, and <em>working out alone eroded long-term motivation</em>. This created our brief — design a system that fuses video-conferencing with a fitness platform, without inheriting the limitations of either.
        </p>
        <CompetitiveTable />
      </Section>

      {/* Section 2: Task */}
      <Section sectionId="cs-section-2" number="02" label="Task" title="Lead a four-person team from blank brief to validated hi-fi prototype in 13 weeks.">
        <p>
          As <strong>Project Owner</strong>, I owned the end-to-end design process: shaping the research plan, facilitating synthesis sessions, driving design critique, and ensuring our prototype answered every research insight. Specifically, I was accountable for:
        </p>
        <ul className="space-y-3 mt-6">
          {[
            "Defining the target user group and the boundaries of the problem space",
            "Designing a mixed-method research plan (qualitative-first, ethically scoped)",
            "Translating raw interview data into personas, scenarios, and design requirements",
            "Leading two prototype iterations — lo-fi → hi-fi — with structured user testing between",
            "Coordinating heuristic evaluation across all four team members",
          ].map((item, i) => (
            <li key={i} className="flex items-start gap-3">
              <Star4 size={10} fill="#1E3A8A" className="mt-2 flex-shrink-0" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </Section>

      {/* Section 3: Action — research */}
      <Section sectionId="cs-section-3" number="03" label="Action · Research" title="I chose qualitative depth over quantitative breadth — and it changed our thesis.">
        <p>
          We ran <strong>semi-structured interviews</strong> and a <strong>group contextual inquiry</strong>. Both methods sacrifice statistical generalizability for ecological validity — and I argued for that trade-off because we needed to understand <em>why</em> people work out alone, not <em>how often</em>.
        </p>

        <WhyCallout title="Why semi-structured interviews?">
          A structured survey would have confirmed what we already suspected (people get bored alone). A semi-structured format gave participants room to reveal what they hadn't been asked — including the insight that reframed our entire product.
        </WhyCallout>

        <div className="mt-12 p-8" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB" }}>
          <div className="text-xs uppercase tracking-widest mb-4" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>
            The pivot
          </div>
          <p style={{ fontFamily: "Georgia, serif", fontSize: "22px", lineHeight: 1.4, color: "#0A1428" }}>
            We started believing the problem was <em>video conferencing capability</em>. Users told us the problem was <em>community</em>.
          </p>
          <p className="mt-4 text-sm" style={{ color: "#6B7280", lineHeight: 1.6 }}>
            Affinity-mapping our interview transcripts surfaced six themes — <span style={{ color: "#1E3A8A" }}>fitness purposes, social aspect, uncertainty about move accuracy, engagement, energy, and physical limitations</span>. The "social aspect" cluster was the densest. Participants didn't just want better video calls — they wanted a <em>safe space to fail without judgment</em>.
          </p>
        </div>

        <h4 className="mt-12 mb-4" style={{ fontFamily: "Georgia, serif", fontSize: "20px", color: "#0A1428" }}>
          Two personas, two pain profiles
        </h4>
        <div className="grid md:grid-cols-2 gap-6">
          <PersonaCard
            name="Claire, 21"
            role="Beginner · Sociology undergrad"
            goal="Wants to work out with friends to stay motivated"
            pain="Can't tell if her form is correct; intimidated by 'beginner' videos that aren't actually beginner"
            color="#3B82F6"
          />
          <PersonaCard
            name="Tanya, 23"
            role="Athlete · Architecture undergrad"
            goal="Wants to coach friends and track her own progress"
            pain="Can't find workouts at her level; finds gym memberships overpriced for solo training"
            color="#1E3A8A"
          />
        </div>

        <p className="mt-8">
          Designing for <em>both</em> profiles in the same session became the hardest constraint — and the most rewarding one. It's what eventually produced our USP.
        </p>
      </Section>

      {/* Section 4: Action — design decisions */}
      <Section sectionId="cs-section-4" number="04" label="Action · Design" title="Five decisions that shaped the product.">
        <DesignDecision
          icon={<Layers size={20} style={{ color: "#1E3A8A" }} />}
          title="Metaphor: 'Studio,' not 'app'"
          decision="We anchored the entire IA in the metaphor of a personal home studio — culminating in a 'My Studio' tab that houses favorited routines."
          why="A studio implies dedication, ownership, and craft. It frames working out as something you build over time, not something you consume. This metaphor made information architecture decisions almost trivial — anything that didn't belong in a studio didn't belong in the app."
        />
        <DesignDecision
          icon={<Users size={20} style={{ color: "#1E3A8A" }} />}
          title="Per-user difficulty scaling (the USP)"
          decision="The same scheduled session can show different exercise variants to different participants based on their fitness profile."
          why="This was the single decision that resolved the core tension between Claire and Tanya. Beginners aren't held back; athletes aren't bored. Every other competitor forces one-size-fits-all classes — we shipped the inverse."
        />
        <DesignDecision
          icon={<Hand size={20} style={{ color: "#1E3A8A" }} />}
          title="Raise-hand over chat during sessions"
          decision="Mid-workout, normal participants can't pause the video — they raise a hand to flag the instructor."
          why="Mid-pose, no one wants to type. Concentration is the whole point of the activity. Raise-hand respects the physical context of use; chat would have broken it. (We flagged in heuristic eval that gesture or voice input would be a stronger v2.)"
        />
        <DesignDecision
          icon={<MessageCircle size={20} style={{ color: "#1E3A8A" }} />}
          title="Auto-generated group chats per session"
          decision="Creating a session creates a chat. Joining a session joins the chat. The chat persists after the session ends."
          why="In testing, group chats hidden inside a separate 'Messages' tab were never used. Auto-generating them at session creation — and surfacing them on the Home tab — turned coordination from a feature into a default behavior."
        />
        <DesignDecision
          icon={<Calendar size={20} style={{ color: "#1E3A8A" }} />}
          title="Optional instructor role"
          decision="Any session creator can designate themselves or a friend as 'instructor,' unlocking pause control and routine editing."
          why="This was missing in v1 and surfaced when I revisited Tanya's persona. She wanted to coach, not just attend. A binary 'host' role would have felt corporate; a togglable instructor role respects that fitness expertise is fluid in friend groups."
        />
      </Section>

      {/* Section 5: Result */}
      <Section sectionId="cs-section-5" number="05" label="Result" title="Two test rounds, eleven validated fixes, one shipped concept.">
        <p>
          The hi-fi prototype was tested against <strong>seven scripted tasks</strong> with the same participants from our research phase — a deliberate choice to leverage their existing context. Following Nielsen's heuristics, four evaluators independently ranked usability issues on a 0–4 severity scale.
        </p>

        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <MetricCard number="11" label="Distinct usability issues identified and resolved across 2 prototype iterations" />
          <MetricCard number="7" label="End-to-end task flows scripted, recorded, and analyzed during user testing" />
          <MetricCard number="6" label="Themes synthesized from raw qualitative data via affinity mapping" />
        </div>

        <h4 className="mt-16 mb-6" style={{ fontFamily: "Georgia, serif", fontSize: "20px", color: "#0A1428" }}>
          Five problem categories, five redesigns
        </h4>
        <div className="space-y-px" style={{ backgroundColor: "#E5E7EB", border: "1px solid #E5E7EB" }}>
          {[
            { problem: "Indistinct screen layouts; right-to-left drag direction felt unintuitive", fix: "Renamed tabs ('Home', 'My Studio', 'Discover'); flipped routine-builder to LTR" },
            { problem: "Editing profile and saving exercises lacked visible affordances", fix: "Added explicit edit icons and a star-based 'Favourite' system replacing implicit 'Save'" },
            { problem: "Custom tag input was inefficient and limited in description", fix: "Replaced with structured dropdowns: 'Type of Exercise' + 'Difficulty'" },
            { problem: "Video guide assumed device flexibility most users don't have", fix: "Added pre-session disclaimer screen showing optimal physical setup" },
            { problem: "Per-session chats were buried in a separate Messages tab", fix: "Auto-generated chats on session creation; persistent chat dock on every screen" },
          ].map((row, i) => (
            <div key={i} className="grid md:grid-cols-2 gap-px">
              <div className="p-6" style={{ backgroundColor: "#FAFAF7" }}>
                <div className="text-xs uppercase tracking-widest mb-2" style={{ color: "#9CA3AF", letterSpacing: "0.2em" }}>Problem</div>
                <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.5 }}>{row.problem}</p>
              </div>
              <div className="p-6" style={{ backgroundColor: "#FFFFFF" }}>
                <div className="text-xs uppercase tracking-widest mb-2" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>Resolution</div>
                <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.5 }}>{row.fix}</p>
              </div>
            </div>
          ))}
        </div>
      </Section>

      {/* Section 6: Reflection */}
      <Section sectionId="cs-section-6" number="06" label="Reflection" title="What I'd do differently — and what I'm proud of.">
        <p>
          The reflection that matters most to me isn't about the artifact. It's about how I worked.
        </p>

        <div className="mt-10 grid md:grid-cols-2 gap-8">
          <div className="p-8" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB" }}>
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle size={16} style={{ color: "#1E3A8A" }} />
              <div className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>What I'd change</div>
            </div>
            <h4 style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "12px" }}>
              Lead with interaction, then aesthetic.
            </h4>
            <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.6 }}>
              Our first lo-fi prototype over-invested in visual polish. The result — predictably — was that user testing surfaced surface-level critique while deeper interaction problems went unspoken. I now sketch the interaction model on paper before opening Figma.
            </p>
          </div>

          <div className="p-8" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB" }}>
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle size={16} style={{ color: "#1E3A8A" }} />
              <div className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>What I'd extend</div>
            </div>
            <h4 style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "12px" }}>
              Design for users with mobility limitations.
            </h4>
            <p className="text-sm" style={{ color: "#4B5563", lineHeight: 1.6 }}>
              The same per-user difficulty scaling that lets Claire and Tanya train together could let users with mobility differences join the same class as their friends. That's not a feature — that's a market position. It would be my v3 priority.
            </p>
          </div>
        </div>

        <div className="mt-10 p-8" style={{ backgroundColor: "#1E3A8A", color: "#FAFAF7" }}>
          <div className="flex items-center gap-2 mb-4">
            <Star4 size={12} fill="#FCD34D" />
            <div className="text-xs uppercase tracking-widest" style={{ color: "#FCD34D", letterSpacing: "0.2em" }}>What I'm proudest of</div>
          </div>
          <p style={{ fontFamily: "Georgia, serif", fontSize: "20px", lineHeight: 1.4 }}>
            We built a system that addresses both the <em>short-term</em> motivation gap (gamifying the start) and the <em>long-term</em> retention gap (community accountability). Most fitness products solve one. Solving both is the whole game.
          </p>
        </div>

        <h4 className="mt-16 mb-4" style={{ fontFamily: "Georgia, serif", fontSize: "20px", color: "#0A1428" }}>
          Honest limitations
        </h4>
        <ul className="space-y-3">
          {[
            "Our research participants were drawn from our personal networks — sample bias likely softened the criticism we heard.",
            "We did not test the per-user difficulty scaling end-to-end; the interaction was prototyped but the algorithm that maps profile → variant remains an open design question.",
            "Sustainability requires a two-sided market (instructors + participants). We did not validate the instructor side of the marketplace.",
          ].map((item, i) => (
            <li key={i} className="flex items-start gap-3 text-sm" style={{ color: "#6B7280", lineHeight: 1.6 }}>
              <span style={{ color: "#1E3A8A", marginTop: "2px" }}>—</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </Section>

      <LegacyFlexijioWriteup />

      {/* Closing */}
      <div className="mt-32 pt-16 border-t text-center" style={{ borderColor: "#E5E7EB" }}>
        <Star4 size={16} fill="#FCD34D" className="inline-block mb-6" />
        <p style={{ fontFamily: "Georgia, serif", fontSize: "22px", lineHeight: 1.5, color: "#0A1428", maxWidth: "640px", margin: "0 auto" }}>
          Flexijio taught me that the best UX work happens at the intersection of <em style={{ color: "#1E3A8A" }}>research humility</em> and <em style={{ color: "#1E3A8A" }}>strategic conviction</em>.
        </p>
        <p className="mt-6 text-sm" style={{ color: "#9CA3AF" }}>
          Want to discuss this project in detail? <span style={{ color: "#1E3A8A", textDecoration: "underline", cursor: "pointer" }}>Get in touch</span>.
        </p>
      </div>
    </main>
  );
}

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

function Hero({ Star4 }) {
  return (
    <div className="pt-8 pb-16">
      <div className="flex items-center gap-2 mb-8">
        <div style={{ width: "32px", height: "1px", backgroundColor: "#1E3A8A" }} />
        <span className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>
          Case Study · 2024
        </span>
      </div>

      <h1 style={{ fontFamily: "Georgia, serif", fontSize: "clamp(44px, 7vw, 84px)", lineHeight: 1.02, fontWeight: 400, letterSpacing: "-0.025em", color: "#0A1428" }}>
        Flexijio
        <Star4 size={24} fill="#FCD34D" className="inline-block ml-4 -mt-12" />
      </h1>

      <p className="mt-6" style={{ fontFamily: "Georgia, serif", fontSize: "clamp(20px, 2.4vw, 28px)", lineHeight: 1.4, color: "#4B5563", maxWidth: "780px", fontStyle: "italic" }}>
        Desktop Video Conferencing Platform for Fitness. A social home-workout platform where friends train together — even when they're apart, and even when they're not at the same fitness level.
      </p>

      <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-8">
        <HeroStat label="Role" value="UX Researcher, UI Designer" />
        <HeroStat label="Team" value="4 designers" />
        <HeroStat label="Duration" value="3 months, Feb 2024 - Apr 2024" />
        <HeroStat label="Course" value="NM3243 · NUS" />
      </div>
    </div>
  );
}

function HeroStat({ label, value }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-widest mb-2" style={{ color: "#9CA3AF", letterSpacing: "0.2em" }}>{label}</div>
      <div style={{ fontFamily: "Georgia, serif", fontSize: "17px", color: "#0A1428", fontWeight: 500 }}>{value}</div>
    </div>
  );
}

function TableOfContents() {
  const items = [
    { num: "01", label: "The Situation", id: "cs-section-1" },
    { num: "02", label: "The Task", id: "cs-section-2" },
    { num: "03", label: "Research", id: "cs-section-3" },
    { num: "04", label: "Design Decisions", id: "cs-section-4" },
    { num: "05", label: "Outcomes", id: "cs-section-5" },
    { num: "06", label: "Reflection", id: "cs-section-6" },
  ];

  function jump(e, hash) {
    e.preventDefault();
    const el = document.getElementById(hash);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <div className="mb-16 pb-12 border-b" style={{ borderColor: "#E5E7EB" }}>
      <div className="text-xs uppercase tracking-widest mb-6" style={{ color: "#1E3A8A", letterSpacing: "0.2em" }}>
        Contents
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-y-3 gap-x-8">
        {items.map((item, i) => (
          <a
            key={i}
            href={`#${item.id}`}
            onClick={(e) => jump(e, item.id)}
            className="flex items-baseline gap-3 text-left hover:opacity-80 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-700 rounded-sm"
          >
            <span style={{ fontFamily: "Georgia, serif", fontSize: "13px", color: "#9CA3AF", fontVariantNumeric: "tabular-nums" }}>{item.num}</span>
            <span style={{ fontFamily: "Georgia, serif", fontSize: "16px", color: "#0A1428", textDecoration: "underline", textUnderlineOffset: "3px", textDecorationColor: "rgba(30,58,138,0.25)" }}>
              {item.label}
            </span>
          </a>
        ))}
      </div>
    </div>
  );
}

function Section({ sectionId, number, label, title, children }) {
  return (
    <section id={sectionId} className="mt-24 mb-12 scroll-mt-28 md:scroll-mt-[7.75rem]">
      <div className="flex items-center gap-3 mb-6">
        <span style={{ fontFamily: "Georgia, serif", fontSize: "14px", color: "#1E3A8A", fontVariantNumeric: "tabular-nums", fontWeight: 600 }}>{number}</span>
        <div style={{ width: "20px", height: "1px", backgroundColor: "#1E3A8A" }} />
        <span className="text-xs uppercase tracking-widest" style={{ color: "#1E3A8A", letterSpacing: "0.25em" }}>{label}</span>
      </div>
      <h2 style={{ fontFamily: "Georgia, serif", fontSize: "clamp(28px, 4vw, 42px)", lineHeight: 1.15, fontWeight: 400, letterSpacing: "-0.015em", color: "#0A1428", marginBottom: "32px", maxWidth: "880px" }}>
        {title}
      </h2>
      <div style={{ fontFamily: "Georgia, serif", fontSize: "17px", lineHeight: 1.7, color: "#374151", maxWidth: "720px" }}>
        {children}
      </div>
    </section>
  );
}

function CompetitiveTable() {
  const rows = [
    { tool: "YouTube", strength: "Infinite content, free", gap: "No live feedback, paralyzing choice overload" },
    { tool: "Zoom", strength: "Synchronous + social", gap: "No discovery layer, no fitness context" },
    { tool: "Peloton", strength: "Premium experience", gap: "US$44/mo + hardware lock-in" },
  ];
  return (
    <div className="mt-12 mb-4" style={{ border: "1px solid #E5E7EB" }}>
      <div className="grid grid-cols-3 gap-px" style={{ backgroundColor: "#E5E7EB" }}>
        <div className="p-4 text-xs uppercase tracking-widest" style={{ backgroundColor: "#1E3A8A", color: "#FAFAF7", letterSpacing: "0.2em" }}>Tool</div>
        <div className="p-4 text-xs uppercase tracking-widest" style={{ backgroundColor: "#1E3A8A", color: "#FAFAF7", letterSpacing: "0.2em" }}>Strength</div>
        <div className="p-4 text-xs uppercase tracking-widest" style={{ backgroundColor: "#1E3A8A", color: "#FAFAF7", letterSpacing: "0.2em" }}>Gap</div>
        {rows.map((row, i) => (
          <React.Fragment key={i}>
            <div className="p-4" style={{ backgroundColor: "#FAFAF7", fontFamily: "Georgia, serif", fontWeight: 600, color: "#0A1428" }}>{row.tool}</div>
            <div className="p-4 text-sm" style={{ backgroundColor: "#FAFAF7", color: "#4B5563" }}>{row.strength}</div>
            <div className="p-4 text-sm" style={{ backgroundColor: "#FAFAF7", color: "#4B5563" }}>{row.gap}</div>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

function WhyCallout({ title, children }) {
  return (
    <div className="my-10 p-6 relative" style={{ backgroundColor: "#DBEAFE", borderLeft: "3px solid #1E3A8A" }}>
      <div className="text-xs uppercase tracking-widest mb-2" style={{ color: "#1E3A8A", letterSpacing: "0.2em", fontWeight: 700 }}>{title}</div>
      <p className="text-sm" style={{ color: "#1E3A8A", lineHeight: 1.6, fontFamily: "Georgia, serif" }}>{children}</p>
    </div>
  );
}

function EmbeddedImage({ src, alt }) {
  return (
    <figure className="mt-6 mb-8">
      <img src={src} alt={alt} style={{ width: "100%", border: "1px solid #E5E7EB", backgroundColor: "#FFFFFF" }} />
      <figcaption className="mt-2 text-xs" style={{ color: "#6B7280" }}>{alt}</figcaption>
    </figure>
  );
}

function LegacyFlexijioWriteup() {
  return (
    <section className="mt-24 mb-12" style={{ maxWidth: "900px" }}>
      <h2 style={{ fontFamily: "Georgia, serif", fontSize: "clamp(28px, 4vw, 42px)", lineHeight: 1.15, fontWeight: 400, letterSpacing: "-0.015em", color: "#0A1428", marginBottom: "24px" }}>
        Extended Project Write-up
      </h2>

      <h3 style={{ fontFamily: "Georgia, serif", fontSize: "28px", color: "#0A1428", marginBottom: "16px" }}>Introduction</h3>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        The project was done in a group of 4 for the course <a href="https://nusmods.com/courses/NM3243/user-experience-design" target="_blank" rel="noreferrer" style={{ color: "#1E3A8A", textDecoration: "underline" }}>NM3243: User Experience Design</a> taken in National University of Singapore (NUS), up to the 1st redesign of the lo-fi design.
      </p>

      <h3 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "28px", color: "#0A1428", marginBottom: "16px" }}>Problem</h3>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        Remote work has increased the demand for <strong>at-home fitness solutions</strong>, but existing options often fall short in supporting users to achieve their fitness goals:
      </p>
      <ul className="mt-4 space-y-3" style={{ color: "#374151", lineHeight: 1.8 }}>
        <li>Online personal training software, such as EverFit and iFit, lacks long-term accountability, focusing on individual classes as opposed to supporting users throughout their fitness journeys.</li>
        <li>Live streaming and video conferencing platforms like Facebook Live and Zoom are not designed specifically for fitness, missing critical features that could enhance user experience.</li>
        <li>Online workout videos on platforms like YouTube require significant self-discipline and fail to provide personalised guidance, making them less suitable for beginners.</li>
      </ul>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}>
        These design problems underscore the need for a fitness desktop video conferencing platform that addresses both the short-term needs and long-term goals of individuals with busy lifestyles.
      </p>

      <h4 className="mt-8" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Target User Group</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>Office workers aged 18 to 63.</p>
      <p className="mt-3" style={{ color: "#374151", lineHeight: 1.8 }}>
        We decided to design for office workers because they form the bulk of our potential users: people with remote work who want to exercise at home but with others, and with professional help.
      </p>

      <h3 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "28px", color: "#0A1428", marginBottom: "16px" }}>Solution</h3>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>The following features set FlexiJio apart from existing alternatives in the market:</p>
      <ul className="mt-4 space-y-4" style={{ color: "#374151", lineHeight: 1.8 }}>
        <li><strong>Community-driven engagement</strong><br />FlexiJio aims to keep users <strong>accountable</strong> for their fitness journeys, helping them achieve long-term goals while providing a more comprehensive and enjoyable workout experience.</li>
        <li><strong>Gamification of fitness</strong><br />FlexiJio incorporates elements of gamification, such as rewards, leaderboards, and progress tracking, to make fitness engaging and motivating for users. These features encourage <strong>consistency</strong> and add a <strong>fun, competitive</strong> element to workouts.</li>
        <li><strong>Personalised exercises</strong><br />Taking into account users' varying fitness levels and their desire to work out with friends, our platform offers two customisation options for the same lessons: expert and simplified. This feature allows users to challenge themselves within their own limits while still enjoying workouts alongside their friends, recognising that everyone's capabilities are unique.</li>
      </ul>

      <div className="mt-8 p-6" style={{ backgroundColor: "#DBEAFE", borderLeft: "3px solid #1E3A8A" }}>
        <h4 style={{ fontFamily: "Georgia, serif", fontSize: "20px", color: "#0A1428", marginBottom: "8px" }}>Disclaimer:</h4>
        <p style={{ color: "#1E3A8A", lineHeight: 1.7 }}>
          FlexiJio is designed for users who want to exercise with others in the comfort of their home. However, it does not cater to situations where users prefer to exercise alone or when class timings do not align with their schedules. Instead, FlexiJio serves as a <strong>complementary workout option</strong> that supports users' fitness journeys without replacing traditional alternatives such as gyms or in-person classes.
        </p>
      </div>

      <h3 className="mt-12" style={{ fontFamily: "Georgia, serif", fontSize: "28px", color: "#0A1428", marginBottom: "16px" }}>Design Process</h3>
      <h4 style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>User Research</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        We conducted semi-structured interviews and indirect observation through written diary logs to capture insights on individual needs in users' fitness journeys, and to track behavioural patterns in exercise to understand long-term behaviour.
      </p>
      <h5 className="mt-6" style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "8px" }}>Key Discoveries</h5>
      <ol className="pl-6 space-y-2" style={{ color: "#374151", lineHeight: 1.8 }}>
        <li>Users want virtual fitness to be as <strong>personal</strong> and <strong>responsive</strong> as in-person training.</li>
        <li>While motivation can come from within, <strong>external support through community</strong> features is crucial for sustained engagement, where users experience a greater sense of achievement and motivation.</li>
      </ol>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}>
        We concluded that for sustained user engagement, our platform needed to prioritise <strong>personalisation</strong>, <strong>customisation</strong>, <strong>smart integration</strong>, and <strong>community-driven</strong> features.
      </p>
      <div className="mt-6 p-6" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB" }}>
        <p style={{ color: "#4B5563", lineHeight: 1.8 }}>
          Personalisation comes in the form of personalised workout plans for users, and is dependent on users' fitness goals, fitness levels, and how fast they want to achieve their goals.
        </p>
        <p className="mt-3" style={{ color: "#4B5563", lineHeight: 1.8 }}>
          Customisation, on the other hand, comes in the form of providing options for users to pick from. In Flexijio, the option to pick classes is given to users, where users can work out more intensely or take it easy depending on their mood. They can also choose which exercise, the expert one or the simple one, to do during the workout class.
        </p>
      </div>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Requirements Definition</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        Based on our data analysis, we concluded that <strong>fitness competency</strong> is an influential factor in our design. We developed two personas based on this characteristic to capture and communicate our users' requirements. This allows us to better understand who we are designing for so that we can focus on making our design more user-friendly.
      </p>

      <h5 className="mt-6" style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "8px" }}>Persona 1: Melina Ching</h5>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>• <strong>Age:</strong> 50<br />• <strong>Gender:</strong> Female<br />• <strong>Occupation:</strong> Director of Communications<br />• <strong>Family:</strong> Mother of two, Wife<br />• <strong>Fitness Level:</strong> Fitness-Competent</p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}><strong>Motivations and Goals</strong><br />1. To remain healthy and fit to prevent suffering or burdening her family in the future.<br />2. To ensure her form is proper for more effective workouts.<br />3. To work out with her friends, allowing her to meet them more often while maintaining consistency in her workout routine.<br />4. To increase the intensity of her workouts to improve her fitness level.</p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}><strong>Frustrations</strong><br />1. She does not meet her friends as often as she wishes.<br />2. Her friends are not as fit, so exercising with them requires attending beginner fitness classes, compromising the intensity of her workout.<br />3. Exercising alone allows her to maintain intensity but has become boring, requiring more motivation and discipline.<br />4. There is no one to check her form when exercising alone, making her doubt the effectiveness of her routines.<br />5. She has reached a fitness plateau and is unsure how to progress further.</p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}><strong>Current Practices</strong><br />1. Exercises alone at home every day.<br />2. Meets her friends twice a month.<br />3. Watches the same workout videos repeatedly because she is familiar with them.</p>

      <h5 className="mt-8" style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "8px" }}>Persona 2: Ryan Tan</h5>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>• <strong>Age:</strong> 35<br />• <strong>Gender:</strong> Male<br />• <strong>Occupation:</strong> Software Engineer<br />• <strong>Marital Status:</strong> Single<br />• <strong>Fitness Level:</strong> Fitness-Incompetent</p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}><strong>Motivations and Goals</strong><br />1. To start and maintain a fitness routine to improve his health and fitness.<br />2. To find a flexible workout solution that fits into his busy schedule.<br />3. To track his fitness journey and use his progress as motivation to continue.<br />4. To have someone hold him accountable and assist with his self-discipline.<br />5. To set clear and achievable fitness goals to stay motivated and committed.</p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}><strong>Frustrations</strong><br />1. Fitness classes and working out with friends are often too intense for his current fitness level.<br />2. Working from home makes him less inclined to leave the house to exercise.<br />3. Exercising at home is also challenging due to his lack of discipline to complete a workout.<br />4. He doesn't track his progress, leaving him unable to see or feel any improvement, which demotivates him further.<br />5. He frequently skips workouts due to a lack of goal-setting and structure in his fitness routine.</p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}><strong>Current Practices</strong><br />1. Works out sporadically based on his mood.<br />2. Plays workout videos on YouTube but rarely completes them.</p>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Current Use Scenario</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        Melina Ching reaches home from her 9-6 job as Director of Communications. She hurriedly lays out her fitness mat and turns on her TV to play her workout videos. <strong>Melina is in a rush because she has dinner plans with her friends at 8 pm, and she has to show up because she has already cancelled on her friends multiple times before.</strong> Melina has not met her friends for months and wants to meet her friends more regularly, but she struggles to balance between her conflicting priorities: family, work, friends, and working out. <strong>Melina has tried working out with her friends in the past as an attempt to combine her priorities, but her friends are not active like her and could not keep up with the fitness class they attended.</strong> However, Melina does not want to compromise on the intensity of her workouts by attending beginner classes with her friends. Thus, they have decided not to proceed with working out together. Melina takes exercising seriously because she wants to maintain her fitness level and health, not wanting to suffer or burden her family with poor health in the future. <strong>However, exercising alone has become monotonous, and she is slowly losing motivation and discipline to complete her workouts properly.</strong> Furthermore, <strong>Melina is frustrated at the lack of progress she is making and has not found a way to become fitter.</strong> As a result, Melina rushes through her workout, failing to ensure her form. She then prepares to leave for her dinner plans with her friends.
      </p>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Proposed Use Scenario</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        Melina Ching reaches home and does a bit of household chores. <strong>At 7:20, she receives a notification that her virtual fitness class at 7:30 is starting soon.</strong> Melina then lays out her fitness mat and switches on her desktop to access FlexiJio. Upon entering the class, <strong>Melina sees her friends and happily greets them. She and her friends have been attending virtual fitness classes together, allowing them to maintain social connections more frequently than in the past through exercising together.</strong> More people start joining, and Melina sees some friends she made through Flexijio. When everyone has entered, the fitness instructor starts punctually by checking everyone's wellbeing. <strong>He then goes through the exercises they will be doing, providing pointers to common mistakes.</strong> These exercises are split into beginner, intermediate, and advanced, with each difficulty level differing by the number of reps or the type of exercise done. <strong>The workout starts, and Melina follows the advanced exercises shown on her screen, while her friends follow beginner exercises shown on their screens.</strong> This allows them to work out together but at their own fitness levels. <strong>The fitness instructor encourages all his students, and mid-exercise, he notices that Melina has started to lose her proper form, so he informs her through the group voice chat.</strong> Melina is happy to be working out with her friends, and she is proud that her less fitness-competent friends have kick-started their fitness journey. <strong>Her group of friends keeps each other accountable, ensuring they exercise regularly and stay healthy together.</strong> Furthermore, <strong>her fitness instructor has helped her become fitter through guidance and more intense workout routines.</strong> With the help of Flexijio and her friends, <strong>Melina has rekindled her relationship with exercise and now looks forward to fun and fulfilling workout sessions after work every day.</strong>
      </p>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Conceptual Design</h4>
      <h5 style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "8px" }}>Metaphors</h5>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        FlexiJio has adopted the conceptual metaphor of a <strong>virtual studio</strong>, where users can access various fitness classes led by instructors in the community. Each class mimics the experience of a physical studio session, allowing real-time participation through live video conferencing.
      </p>
      <p className="mt-3" style={{ color: "#374151", lineHeight: 1.8 }}>
        The key functions of FlexiJio have been broken down into metaphors to enhance user understanding and engagement:
      </p>
      <ul className="mt-4 space-y-5" style={{ color: "#374151", lineHeight: 1.8 }}>
        <li><strong>Home</strong><br />"Home" is akin to the reception area of a studio, allowing users to "check in" to their virtual fitness experience. It involves a mini-game where users can purchase furniture with their calories burnt or hours clocked in during workout classes. Users can customise their room by manipulating the virtual room as they would in real life. The <strong>gamification</strong> of FlexiJio through this feature incentivises users to exercise more to purchase more items to decorate their room with.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-04_at_11.49.05.png" alt="Mini-game in Flexijio" /></li>
        <li><strong>Discussion</strong><br />"Discussion" is a <strong>forum</strong> and an <strong>enthusiast zone</strong> that facilitates interactions between users, mirroring the communal space within the studio where fitness enthusiasts gather to share fitness tips, or just to have conversations in general. The user can explore the many different posts on the forum to learn more about fitness.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-04_at_11.51.47.png" alt="Discussion Forum" /></li>
        <li><strong>Leaderboard</strong><br />"Leaderboard" serves as a <strong>virtual challenge board</strong>, displaying achievements and milestones reached by friends. Through this competitive edge, users are driven by a friendly sense of rivalry to keep up with their efforts whilst feeling in-group in the FlexiJio community.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-04_at_11.53.35.png" alt="Leaderboard" /></li>
        <li><strong>My Groups</strong><br />"My Groups" consists of communities, with private and group chat functions between users, and with instructors. As such, it is similar to a "WhatsApp group chat" for community engagement, coordination of classes and a way to build connections.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-04_at_11.54.49.png" alt="My Groups" /></li>
        <li><strong>My Classes</strong><br />At "My Class", users can discover new classes and track existing classes in a board-like format, therein, linked as a <strong>personal training planner</strong>.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-09_at_10.44.39.png" alt="My Classes" /></li>
        <li><strong>Health Tracker</strong><br />"Health Tracker" offers progress monitoring, agenda setting, and valuable insights within a customised fitness journey, acting as a <strong>virtual personal trainer</strong>.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-09_at_10.44.39.png" alt="Health Tracker" /></li>
        <li><strong>FAQ</strong><br />Users can find answers to queries on this page. Apart from scrolling through the list of FAQs, users can also use the AI-powered chatbot, which is personified by our own FlexiJio mascot. Anthropomorphism and the conversing interaction type it utilises make it more intuitive and comfortable for users to use, akin to a <strong>friendly staff working at the fitness studio</strong>.<EmbeddedImage src="/design-assets/project-media/flexijio/Screenshot_2025-02-04_at_12.03.46.png" alt="FAQ" /></li>
      </ul>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Storyboarding</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>The following <strong>storyboard</strong> shows FlexiJio's proposed interaction flow:</p>
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXcwv6ENAjEvrhhr0l_DmyhbRaDIiz1QLnQHXOJJhl7XGNjtzcvBtWUoCxy_cV8OelYv3nv6zIW70sSCJhiYzpfua6bqZh2BcQ-O-MxgvHc33TZtmPEvrFa5K7Ld9hKqSpD2bUcGGtv8WzFjDR32_JSawEs_?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Storyboard of features: Customising Profile, Community-Based Features and User Centric Features" />

      <h4 className="mt-8" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Wireframe</h4>
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXeFYWfJlFeLmVOmLu-D5fzueiQRPcbuLl0hMsWT6WMSQf1tqgxsb3HiVShXMskdQm2dD43ivg8AegVouOO77Mrq8PCxXqkmCB2iEl-5JBLqa8hSuWAfAx_fUMokvoeBjjtxck26DJ3Si8dt601b2KPbJjbH?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Legend (1)" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXfXSeMQN8mJkgBmPBI008-Ilsd5YNfdQzPsg66zbsV6OkiFbMw79g2QjOBH1wlsYoPFF-3r9nTrwxAFHD3j71FgjGRScxDkrTijXnvdvkrah7fw2DIRTrTY03S-ksbvWEeSh8RIE1cMa7Ws6KfoKm7T-Uc?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Legend (2)" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXcsAIBYJCajEFCrSPEtJDh-APvQmKr8gfKwpGWtagscVLtDI93aANxpbirdw85f09OjIvyo8QM1QKRwHDMdCQ13clUi1eDwdWt30A8ogX3UTChvTVYVFXnsDhyAEtbiZY6XuikS4cXfgt_cm1GJvqlpUqRm?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Virtual Fitness Class Wireframe" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXev1dst9JJ6yEt1dM5qj3iSb4XwTKARg1SUAGql6gwXOMQKZVuFIg4wUwDou5Al3pExc1SttVkdJVQM9Kz-zfk8WNg3NoBHDPNKdj0AO6aMjdLkhI5663hCP-B7ApxblrCfPG3s5xA43fQTtOxK9bzQF-I?key=5pTX_R5-ClyrMv_jWGc_yA" alt="List of Features" />

      <h4 className="mt-8" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Lo-Fi Prototype</h4>
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXeWVLArG-RDRmjGpLGGnyUSPISeKpr61AhP2IRbTYYGmviPOG-dA4yyYCMpNvcguGGiB7ihWrVz75MI6zMqQp1oUnbzGHjlFTlf2wL7J5n3v-kAu14VFtSeXkXJulLQoEoljAplYBhytdMGLWfrwujkOHp4?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Customising Profile (Age, Agenda, Finalised Profile)" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXe4if-oIdTpP10nmWSHcPdsJpZI_-v3-zbPq2j7VKnG2UjxZA3KWSCes7wa_X2PxOBuJXZtc5ChYEZlBrXLTJ4ACcfCGQsE3KSbs-1GW9UzMFDpfLV28o5PYImSQKl2k__9zw15hbDthp5fnLobTwHlqq9b?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Community-Based Features (Home, Discussion, Leaderboard)" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXfimhmz5INp7O--7_g4utOkEMPYqAWZb5v0YpFvSI96kTeqTUC2RhkYgJD1oz-gpy28EXF1D_Eqk5l7ZrZ5euwcd-dpQ67CbqqS5r5bPsB30N5-nKk3g10HmdKn_rJxGKKDEGA9cTT2Zd1erKiidssG7ck?key=5pTX_R5-ClyrMv_jWGc_yA" alt="User-Centric Features (My Groups, My Classes, Health Tracker)" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXcpAxZsG72mrmI0awfGR6VrTvPHpT8CBJLYcVyJdmftZXIwjtMuBrRCn5iih83EuZX7hyY0TQne7t7Pm5Ldt9GAaDQwP5ZWkiREG_LO5SIqiJebOmVMrdQw_xDpPqDEs4GgqtdOZ74mZM3SpqQ4AKFLnHf0?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Virtual Fitness Class" />

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>User Testing Results</h4>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>Feedback</strong></p>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>Signing Up</strong><br />Our participants noted that once they had signed up for their accounts and created their profiles and fitness, there were no options for them to navigate back to edit their profiles.</p>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>My Groups</strong><br />For My Groups, users mentioned that it was not necessary to add the feature to schedule classes and to allow users to view other participants' interests.</p>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>My Classes</strong><br />The Bluetooth symbol shown during the calls (that would control the music for the users) confused users, as they had interpreted this feature to be something that anyone could use during the call, and not just for the instructors to control the music. It was also not made clear to the users how to enter the call and leave, which caused misleading navigation through the call interface.</p>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>Forum</strong><br />Users had given feedback that "challenges" where fitness challenges for users to join can be found, should be located in another section for easy access.</p>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>Leaderboard</strong><br />The statistics and information given on the leaderboard were rather confusing and needed to be better visualised.</p>
      <p style={{ color: "#374151", lineHeight: 1.8 }}><strong>General</strong><br />On the interface and design, two out of four participants mentioned the overwhelming choices of colours and felt it was distracting when they were trying to navigate within FlexiJio. However, the other two participants mentioned it was not a big issue, but still suggested that the number of choices should be cut down. The buttons throughout the interface were also rather confusing and difficult to differentiate from other features on the interface, and the participants suggested that we could differentiate them by using darker colours.<br /><br />There were also severe inconsistencies in font-weight and typography, and a participant mentioned that the cursive font we had used throughout our prototype made it confusing to read. Lastly, there was a lack of error recovery throughout the prototype, and many of our prototype's features clashed with our participants' existing mental models.</p>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Proposal for Redesign</h4>
      <h5 style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "8px" }}>Incorporated Feedback</h5>
      <ul className="space-y-3" style={{ color: "#374151", lineHeight: 1.8 }}>
        <li>Interface freshened up, clutter decreased.<br />- Colour-coding different navigation pages and using a variety of hues for each page.<br />- Standardising the font type and size throughout the prototype.</li>
        <li>Local and Global navigation improved<br />- Clearly displaying the navigation page on the left of the screen and highlighting the section the user is on<br />- When users are in the call, they can only "leave" through the "Leave" button if they wish to exit the class.</li>
        <li>Lack of inclusivity for users without personal health tracking devices addressed<br />- Two distinct interfaces to accommodate both types of users<br />- For users with health tracking devices, the interface provides a comprehensive overview of their fitness progress, including calories burned during FlexiJio classes, daily step counts, and additional workouts logged from external devices.<br />- For users without health tracking devices, the interface displays simpler metrics, such as the hours completed and estimated calories burned from FlexiJio classes.</li>
      </ul>
      <h5 className="mt-6" style={{ fontFamily: "Georgia, serif", fontSize: "18px", color: "#0A1428", marginBottom: "8px" }}>Unincorporated Feedback</h5>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        Ability to schedule classes in "My Groups" was not removed because we felt the convenience of being able to see the classes that the group hosts in its own page is not confusing.
      </p>

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Final Prototype</h4>
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXdXB1_QfezSrzj_ipskn0F6w9w0Ts37715AsweeAfYsnMKObFuW62ziRglHoABp9rKR7QBWtodrV8RNr1iZ8k6RV54vlIR18pQKm26ILwVyb0tG6hrv2OE1QpqKPRb_lIGuzyGrmYYEMvPkZ7VC_2wSncU9?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Sign Up, Customising Profile" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXfI4RhNcGvvZiM-b4koCuZVK87FJtIe8sATB5PvNb8rJxbeVWXicT6vy9gNRR1oF5RH80uljZ8P0dgi_ADslaofm0cu9-93zXVVQVTAfiB7dQMl4G1VkkWPrND-ChcMWKomI7sSBDfTvLY-GiYY9DGLoy83?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Home Page, My Room, Health Trackers for users with personal tracking devices and users without" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXc3i7BpofXqzOJXYCzX1tVavHkofLRD90Duv0kX3JrDuGB77sqortC1nYAUPXk4pL4GZkdy2dhU1KrvNR8ucBxxJ939oZVwPv9Y49J1o7LSErnDSbP5AdUPt2HE29YvC8mcmqM-Zfyfa67RwY6G9XOQY5rb?key=5pTX_R5-ClyrMv_jWGc_yA" alt="My Groups, My Groups: Scheduling A Class, My Groups: Chats, Leaderboard" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXczxSUvdHyyGKH65iIi3W_TUMSw5Aap3XWCOgNDwJdLxNqvzLCDt5_TN_rejaN_aM9H_2d5xphXEHlNLhlwvlDR-jKWTc2TOlGcm1I9m2yL2A_GJIgcTQVvsbE-r2efYm5-wSs40dEcOsSGGY5dtj9xqdDM?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Forum: Feed, Forum, Noticeboard, Help" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXdYlIK3a8UtQJ_e7NHKltAZ7SgnD53hU_EwrCAgIRawxAv6rHDEyYxcAb1ktKi4DWDaARdKFsHnfPGmwk_hK7SRIhtNSBH4LOb3zg4mtoanBDEcJuO9yrEn6eU_su5MmjAnb0tD-lxLY29UPKFgm29U-6CM?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Classes: My Classes" />
      <EmbeddedImage src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXeRxW02dWQ8Nc4KbTge28ZDUtlBjx8zjbMpPyD_O5ocuMMNr1kUSVGAvafZ-iPhl_lhEcGogf-T7dPDA-2m-GRlr-GbTprGTS0vs5tehTyr95i9Z-RXrpYTl4XHYL-q8lBJAnQoxvur4AXt_LbJ3OKe0_V9?key=5pTX_R5-ClyrMv_jWGc_yA" alt="Call, Call Has Ended" />

      <h4 className="mt-10" style={{ fontFamily: "Georgia, serif", fontSize: "22px", color: "#0A1428", marginBottom: "8px" }}>Heuristic Evaluation</h4>
      <div className="overflow-x-auto" style={{ border: "1px solid #E5E7EB" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", minWidth: "1100px" }}>
          <thead style={{ backgroundColor: "#1E3A8A", color: "#FAFAF7" }}>
            <tr>
              {["Usability Heuristics", "How Common? (rating)", "On-Off / Persistent? (rating)", "Perceived Seriousness (rating)", "Hard to Overcome? (rating)", "Overall Severity", "Description of Violation", "Proposed Solution"].map((h) => (
                <th key={h} style={{ border: "1px solid #E5E7EB", padding: "10px", textAlign: "left", fontSize: "12px", letterSpacing: "0.02em" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody style={{ color: "#374151", backgroundColor: "#FFFFFF" }}>
            <tr><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>1. Visibility of System Status</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Bluetooth Function: Whether or not Bluetooth is connected to Flexijio, and how to connect it, is missing from our prototype. This is a crucial feature of Flexijio that we missed out on.</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Display the device name if a device has been connected, or leave the field blank if there is none connected. Allow the user to click on this symbol to connect their devices. This will give the users the ability to see system status easily when necessary, which is during fitness classes. The ability to connect it through the icon allows users to do it quickly too in situations with time constraints, like just before class when they realise their trackers are not connected.</td></tr>
            <tr><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>2. Match between system and the real world</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>1</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>1</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>2</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Home: "XP" was used to represent currency in-game. This does not match the metaphor of a fitness studio well since "XP" is mostly used in video games and not in fitness. Also, spending experience on furniture in "Home" and decreasing does not fit well with the metaphor, since it does not make sense for users to lose experience this way.</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Changing the currency to "Calories". The calories lost in fitness classes are added to the user's in-game currency, which can be used to spend on items. This matches the metaphor of fitness more than "XP".</td></tr>
            <tr><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3. User control and freedom</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>2</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>1</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>2</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Sign Up Page: Sign-up pages still lacking in backward navigation, do not grant users the flexibility of changing their personal details in that interface.</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Add in a back button, and also a progress button that allows users to click on any page of the signup interface. This will allow users to easily jump to any specific part.</td></tr>
            <tr><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>6. Recognition rather than Recall</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>2</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>2</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Search Bar on My Groups and Forum: users are unable to see what they have searched, unable to save pages for future references, unable to quickly access specific groups or users in the chat function.</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Add a search history and bookmark function on the search bar of "My Groups" and "Forum". Add in the ability to pin users for quick access in "My Groups" chat feature. The search history will be shown as a list under the search bar, seen in Google's search bar. The bookmark function will add a new tab for users to quickly access posts pinned.</td></tr>
            <tr><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>9. Help users recognise, diagnose, and recover from errors</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>There is no support system to help in user error recognition, no error messages, no descriptions on what users can do to proceed with the task or how to reverse destructive actions.</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Introduce contextual tooltips that provide hints/reminders when users hover over or engage with features that are frequently associated with errors. Implement an "Undo" feature, accompanied by a brief instructional message, allowing users to easily revert actions they have mistakenly performed.</td></tr>
            <tr><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>9. Help users recognise, diagnose, and recover from errors</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>3</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>4</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>FAQ, Forum, Noticeboard, Group's Chat: Limited pop-up messages, users are unable to draft and delete posts with no visible signal to show if something is posted.</td><td style={{ border: "1px solid #E5E7EB", padding: "10px" }}>Include first-time user pop-up messages with instructions on how to navigate these pages. Add an icon with a '?' at the bottom right of every page, for users to click on if they need help.</td></tr>
          </tbody>
        </table>
      </div>

      <h3 className="mt-12" style={{ fontFamily: "Georgia, serif", fontSize: "28px", color: "#0A1428", marginBottom: "16px" }}>Reflection and Future Implications</h3>
      <p style={{ color: "#374151", lineHeight: 1.8 }}>
        I believe my group's understanding of the problem space clarified over time. This improvement resulted from data gathered from our target users and Professor Dennis' comments. The qualitative data methods were useful for in-depth insights into our target users. However, I acknowledge that more data is required to gather a consensus more reflective of our target users. Also, we collected data from people we know, this may skew our data and lead to it being less critical. Though the insights we gathered may be useful, the overall use for this system is uncertain.
      </p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}>
        A foreseeable challenge is how Flexijio will sustain; it needs a large user base of instructors and students. I feel we have not fully answered why users would use our system instead of existing alternatives. The community aspect of Flexijio is supposed to attract users but this could emphasised and justified more, explaining how we would appeal to users to see the value in community workouts. To address this issue, I believe the design problem can be extended to those with mobility issues. Through our system, these users can exercise at home without the trouble of commuting, and they can attend the same class as their friends because our system can show different exercises to different users depending on their fitness abilities. If I had another round of iteration, I would have focused on designing for this secondary group of users.
      </p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}>
        In terms of actual design, our first lo-fi prototype was one I had reservations over. I believe that our group focused too much on aesthetics as opposed to actual interactions. Consequently, our findings focused on distracting aesthetics, taking attention away from actual interactions. With more time, I would focus more on the interactions of the system. I realise now that my group has focused more on the interface in terms of how it looks and how information is placed. Though crucial, the lack of focus on how the features will work and what interactions can be implemented may have led to a less effective overall design. I am most proud of the feature of showing different exercises of varying difficulty, and I believe this is Flexijio's unique selling point. I am also happy that we fulfilled the short-term goal of users to start working out by gamifying the fitness journey, and the long-term goal of users to maintain consistency by having Flexijio's community hold each other accountable. Lastly, in evaluating our design, Norman's 10 Usability Heuristics was beneficial. However, I believe more practice is needed for me to use it effectively. For now, this template is not intuitive because I had to consider each interaction and design aspect of the interface individually using the ten heuristics. Thus, I would appreciate it if more focus was placed on it since I believe it is useful.
      </p>
      <p className="mt-4" style={{ color: "#374151", lineHeight: 1.8 }}>
        This module taught me more about designing for others, the design process, and the importance of user testing and prototyping. This module showed another aspect of design, contrasting with NM3217: Principles of Visual Communication Design's focus on aesthetics.
      </p>
    </section>
  );
}

function PersonaCard({ name, role, goal, pain, color }) {
  return (
    <div className="p-6" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB" }}>
      <div className="flex items-center gap-3 mb-4">
        <div style={{ width: "40px", height: "40px", borderRadius: "50%", backgroundColor: color, display: "flex", alignItems: "center", justifyContent: "center", color: "#FFFFFF", fontFamily: "Georgia, serif", fontSize: "16px", fontWeight: 600 }}>
          {name.charAt(0)}
        </div>
        <div>
          <div style={{ fontFamily: "Georgia, serif", fontSize: "17px", fontWeight: 600, color: "#0A1428" }}>{name}</div>
          <div className="text-xs" style={{ color: "#6B7280" }}>{role}</div>
        </div>
      </div>
      <div className="space-y-3 text-sm">
        <div>
          <div className="text-xs uppercase tracking-widest mb-1" style={{ color: "#9CA3AF", letterSpacing: "0.15em" }}>Goal</div>
          <div style={{ color: "#374151", lineHeight: 1.5 }}>{goal}</div>
        </div>
        <div>
          <div className="text-xs uppercase tracking-widest mb-1" style={{ color: "#9CA3AF", letterSpacing: "0.15em" }}>Pain</div>
          <div style={{ color: "#374151", lineHeight: 1.5 }}>{pain}</div>
        </div>
      </div>
    </div>
  );
}

function DesignDecision({ icon, title, decision, why }) {
  return (
    <div className="mt-10 pt-10 border-t first:border-t-0 first:pt-0 first:mt-0" style={{ borderColor: "#E5E7EB" }}>
      <div className="flex items-center gap-3 mb-4">
        <div className="flex items-center justify-center" style={{ width: "36px", height: "36px", backgroundColor: "#DBEAFE", borderRadius: "2px" }}>
          {icon}
        </div>
        <h3 style={{ fontFamily: "Georgia, serif", fontSize: "22px", fontWeight: 500, color: "#0A1428", letterSpacing: "-0.01em" }}>
          {title}
        </h3>
      </div>
      <p className="mb-4" style={{ fontFamily: "Georgia, serif", fontSize: "17px", lineHeight: 1.6, color: "#374151" }}>
        {decision}
      </p>
      <div className="pl-4" style={{ borderLeft: "2px solid #FCD34D" }}>
        <div className="text-xs uppercase tracking-widest mb-1" style={{ color: "#1E3A8A", letterSpacing: "0.2em", fontWeight: 700 }}>Why</div>
        <p className="text-sm" style={{ color: "#6B7280", lineHeight: 1.6, fontFamily: "Georgia, serif" }}>{why}</p>
      </div>
    </div>
  );
}

function MetricCard({ number, label }) {
  return (
    <div className="p-8 text-center" style={{ backgroundColor: "#FFFFFF", border: "1px solid #E5E7EB" }}>
      <div style={{ fontFamily: "Georgia, serif", fontSize: "56px", fontWeight: 400, color: "#1E3A8A", lineHeight: 1, letterSpacing: "-0.03em" }}>
        {number}
      </div>
      <div className="mt-4 text-sm" style={{ color: "#6B7280", lineHeight: 1.5 }}>
        {label}
      </div>
    </div>
  );
}
