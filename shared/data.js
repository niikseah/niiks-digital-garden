// Portfolio data modeled from exported Notion content.
window.PROJECTS = [
  {
    slug: 'pantry-pal',
    title: 'Pantry Pal',
    kind: 'uiux',
    kindLabel: 'ui/ux',
    year: '2024',
    role: 'UI Designer, UX Researcher',
    excerpt:
      'Mobile app concept tackling food waste by simplifying pantry management and meal planning.',
    tags: ['figma', 'foodtech', 'mobile'],
    href: 'case-studies/project.html?slug=pantry-pal',
    thumbLabel: 'pantry pal',
    thumb: 'public/project-media/pantry-pal/Screenshot_2025-02-09_at_10.29.48.png',
  },
  {
    slug: 'telegram-bot-heymax',
    title: 'Telegram Bot for Trip Planning | NUS Fintech Society × HeyMax',
    kind: 'code',
    kindLabel: 'code',
    year: '2025',
    role: 'Product Builder',
    excerpt:
      'Trip-planning Telegram bot project built for NUS Fintech Society in collaboration with HeyMax.',
    tags: ['telegram', 'automation', 'fintech'],
    href: 'case-studies/project.html?slug=telegram-bot-heymax',
    thumbLabel: 'telegram bot',
    thumb: 'public/project-media/telegram-bot-heymax/image.png',
  },
  {
    slug: 'nusmart-dining-revamp',
    title: 'NUSMart Dining Revamp',
    kind: 'uiux',
    kindLabel: 'ui/ux',
    year: '2024',
    role: 'UI Designer, UX Researcher',
    excerpt: 'Revamped mobile app experience for NUSMart Dining.',
    tags: ['miro', 'mobile', 'service design'],
    href: 'case-studies/project.html?slug=nusmart-dining-revamp',
    thumb: 'public/project-media/nusmart-dining-revamp/Screenshot_2025-02-09_at_10.16.15.png',
  },
  {
    slug: 'flexijio',
    title: 'FlexiJio',
    kind: 'uiux',
    kindLabel: 'ui/ux',
    year: '2024',
    role: 'UX Researcher, UI Designer',
    excerpt: 'Desktop video conferencing platform for fitness classes and remote coaching.',
    tags: ['ux research', 'desktop', 'fitness'],
    href: 'case-studies/project.html?slug=flexijio',
    thumb: 'public/project-media/flexijio/Screenshot_2025-02-09_at_10.44.39.png',
  },
  {
    slug: 'fusion-scanner',
    title: 'Fusion Scanner',
    kind: 'uiux',
    kindLabel: 'ui/ux',
    year: '2023',
    role: 'UX Researcher, UI Designer',
    excerpt:
      'Browser extension concept to improve reading accessibility for language barriers and reading disabilities.',
    tags: ['balsamiq', 'figma', 'accessibility'],
    href: 'case-studies/project.html?slug=fusion-scanner',
    thumb: 'public/project-media/fusion-scanner/Screenshot_2025-02-08_at_11.47.11.png',
  },
  {
    slug: 'kita-communication-intervention',
    title: 'From Blind Box to Brochure, A Communication Intervention for Kita',
    kind: 'uiux',
    kindLabel: 'ui/ux',
    year: '2024',
    role: 'Designer',
    excerpt:
      'Communication intervention project focused on clarifying brand and messaging touchpoints for Kita.',
    tags: ['communication', 'intervention', 'branding'],
    href: 'case-studies/project.html?slug=kita-communication-intervention',
  },
  {
    slug: 'brand-style-guide',
    title: 'Brand Style Guide',
    kind: 'uiux',
    kindLabel: 'graphic',
    year: '2023',
    role: 'Graphic Designer',
    excerpt: 'Comprehensive brand identity guideline built across print and digital assets.',
    tags: ['illustrator', 'indesign', 'photoshop'],
    href: 'case-studies/project.html?slug=brand-style-guide',
    thumb: 'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-01.png',
  },
  {
    slug: 'miscellaneous-works',
    title: 'Miscellaneous Works',
    kind: 'uiux',
    kindLabel: 'graphic',
    year: '2023',
    role: 'Graphic Designer',
    excerpt: 'Curated selection of graphic design experiments and production-ready pieces.',
    tags: ['illustrator', 'indesign', 'graphic design'],
    href: 'case-studies/project.html?slug=miscellaneous-works',
    thumb: 'public/project-media/miscellaneous-works/33cb6212-d8d0-43b1-b534-acbaab4666b1.png',
  },
  {
    slug: 'magic-of-resilience',
    title: 'Magic of Resilience',
    kind: 'code',
    kindLabel: 'video',
    year: '2023',
    role: 'Director of Photography',
    excerpt: 'Non-fiction short documentary spotlighting local business Meta Illusions.',
    tags: ['videography', 'premiere pro', 'documentary'],
    href: 'case-studies/project.html?slug=magic-of-resilience',
    thumb: 'public/project-media/magic-of-resilience/Screenshot_2025-01-24_at_15.47.19.png',
  },
];

window.FEATURED = ['pantry-pal', 'telegram-bot-heymax', 'fusion-scanner'];

window.CASE_STUDIES = {
  'pantry-pal': {
    subtitle: 'Mobile app concept for reducing household food waste through smarter pantry workflows.',
    timeline: 'Oct-Nov 2024',
    tools: 'Figma',
    heroImage: 'public/project-media/pantry-pal/Screenshot_2025-02-09_at_10.29.48.png',
    gallery: [
      'public/project-media/pantry-pal/Screenshot_2025-04-09_at_09.15.11.png',
      'public/project-media/pantry-pal/Screenshot_2025-04-09_at_09.15.42.png',
      'public/project-media/pantry-pal/Screenshot_2025-04-09_at_09.23.09.png',
      'public/project-media/pantry-pal/8fea386d-f56f-4252-96e0-98efbbb2fbfe.png',
      'public/project-media/pantry-pal/39b9c882-e150-425e-8bb1-80b897ed7aed.png',
    ],
    sections: [
      {
        header: 'Background & Problem Framing',
        body: [
          'Pantry Pal is a mobile UI/UX concept designed to tackle food waste by simplifying pantry management and meal planning.',
          'The project began with a clear behavior gap: users cared about waste but still overbought and forgot existing items, which led to duplication and expiry.',
        ],
      },
      {
        header: 'Research Insights',
        bullets: [
          'Awareness of food waste did not reliably translate to daily action.',
          'Users prioritized convenience over sustainability when shopping under time pressure.',
          'Waste-reducing behaviors were perceived as tedious without strong in-app support.',
          'Participants preferred low-friction capture methods (voice, barcode scan, quick add).',
        ],
      },
      {
        header: 'Existing User Flow',
        body: [
          'The baseline grocery journey was mapped from purchase to unpacking to identify where duplication, forgotten inventory, and expiry risk occur.',
          'This revealed that most breakdowns happened before planning (during shopping decisions) and after purchase (during pantry organization).',
        ],
      },
      {
        header: 'Lo-Fi Prototype',
        body: [
          'A low-fidelity prototype was created to test core workflows: onboarding, pantry setup, grocery input, expiry tracking, and recipe/meal planning loops.',
          'The focus at this stage was information clarity and step-by-step usability rather than visual polish.',
        ],
      },
      {
        header: 'User Testing Results',
        bullets: [
          'Navigation hierarchy was validated, with Pantry positioned for faster repeated access.',
          'Grid-style visual treatment for expired items performed better than list-style alternatives.',
          'Recipe portion controls were seen as highly useful for reducing over-cooking and over-buying.',
          'Users requested stronger persistence of previously entered groceries for faster repeat actions.',
        ],
      },
      {
        header: 'Mid-Fi Prototype & Design Considerations',
        body: [
          'Mid-fidelity iterations incorporated tested navigation patterns, clearer interaction labels, and more practical pantry/meal planning flows.',
          'Color, accessibility contrast, and action naming were refined to support both first-time and repeat usage.',
        ],
      },
      {
        header: 'Outcome & Skills Developed',
        bullets: [
          'Delivered a complete prototype and validated interaction model for pantry and meal workflows.',
          'Strengthened user research, interview synthesis, empathy mapping, and interaction design execution.',
          'Produced a concept with clear potential to reduce avoidable food waste through daily behavioral nudges.',
        ],
      },
    ],
  },
  'telegram-bot-heymax': {
    subtitle: 'Trip-planning Telegram bot built for NUS Fintech Society in collaboration with HeyMax.',
    timeline: '2025',
    tools: 'Telegram APIs, workflow automation',
    heroImage: 'public/project-media/telegram-bot-heymax/image.png',
    gallery: ['public/project-media/telegram-bot-heymax/image.png'],
    sections: [
      {
        header: 'Project Overview',
        body: [
          'This coding project explored how conversational interfaces can simplify trip planning and recommendation workflows.',
          'The Telegram bot focused on quick user inputs and actionable trip suggestions without requiring a heavy app experience.',
        ],
      },
      {
        header: 'Problem & Opportunity',
        body: [
          'Students and young travelers often bounce between multiple tools while planning trips, leading to fragmented decisions.',
          'A bot-native flow offered a lightweight way to centralize planning prompts and recommendations in one channel.',
        ],
      },
      {
        header: 'Implementation',
        bullets: [
          'Structured conversational decision trees for destination and preference capture.',
          'Built bot responses to guide users through planning checkpoints and next actions.',
          'Iterated interaction logic for clearer prompts and lower response friction.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Delivered a working concept demonstrating the viability of chat-based trip planning for a student user segment.',
        ],
      },
    ],
  },
  'nusmart-dining-revamp': {
    subtitle: 'Revamped mobile dining journey for NUSMart with clearer navigation and decision support.',
    timeline: 'Sep 2024',
    tools: 'Miro',
    heroImage: 'public/project-media/nusmart-dining-revamp/Screenshot_2025-02-09_at_10.16.15.png',
    gallery: ['public/project-media/nusmart-dining-revamp/Screenshot_2025-02-09_at_10.16.15.png'],
    sections: [
      {
        header: 'Project Overview',
        body: [
          'NUSMart Dining Revamp reimagined the mobile dining experience to make exploration, selection, and ordering more intuitive.',
        ],
      },
      {
        header: 'Research & Insight',
        body: [
          'Mapped current pain points in the dining flow and identified moments where users felt uncertainty or unnecessary friction.',
        ],
      },
      {
        header: 'Design Direction',
        bullets: [
          'Simplified navigation hierarchy for quicker menu and option discovery.',
          'Prioritized clearer information architecture to support faster user decisions.',
          'Refined interaction cues so primary actions were easier to locate at each step.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Produced a revamped experience framework with improved usability and clearer journey continuity.',
        ],
      },
    ],
  },
  flexijio: {
    subtitle: 'Desktop video conferencing concept tailored for fitness instruction and participation.',
    timeline: 'Feb-Apr 2024',
    tools: 'Miro',
    heroImage: 'public/project-media/flexijio/Screenshot_2025-02-09_at_10.44.39.png',
    gallery: [
      'public/project-media/flexijio/Screenshot_2025-02-04_at_11.49.05.png',
      'public/project-media/flexijio/Screenshot_2025-02-04_at_11.51.47.png',
      'public/project-media/flexijio/Screenshot_2025-02-04_at_11.53.35.png',
      'public/project-media/flexijio/Screenshot_2025-02-04_at_11.54.49.png',
      'public/project-media/flexijio/Screenshot_2025-02-04_at_12.03.46.png',
    ],
    sections: [
      {
        header: 'Project Scope',
        body: [
          'FlexiJio is a desktop video conferencing platform concept specifically designed for fitness sessions.',
          'The solution was positioned as a complementary option for users who want social, guided workouts at home.',
        ],
      },
      {
        header: 'Disclaimer & Product Boundaries',
        body: [
          'FlexiJio is not meant to replace in-person gyms or users who prefer solo workouts.',
          'It is designed for users seeking flexible, community-supported virtual fitness experiences.',
        ],
      },
      {
        header: 'Key Discoveries',
        bullets: [
          'Users wanted virtual training to feel personal and responsive, not generic.',
          'Community and social accountability improved motivation consistency.',
          'Sustained engagement depended on personalization, customization, and integrated tracking.',
        ],
      },
      {
        header: 'Personas & Proposed Use Scenario',
        body: [
          'Personas were developed to represent real scheduling, motivation, and family/work constraints.',
          'Use-scenario mapping validated notification timing, class entry flow, and social touchpoints as key retention moments.',
        ],
      },
      {
        header: 'Prototype Direction',
        bullets: [
          'Defined workflows for class discovery, session participation, and post-session follow-through.',
          'Integrated health tracking and FAQ/help touchpoints to reduce session friction.',
          'Storyboarded multi-step feature use to align instructor and participant expectations.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Delivered a UX concept focused on fitness-centric video interaction design and session management clarity.',
        ],
      },
    ],
  },
  'fusion-scanner': {
    subtitle: 'Accessibility-oriented browser extension concept to improve reading comprehension and comfort.',
    timeline: 'Sep-Nov 2023',
    tools: 'Balsamiq, Figma',
    heroImage: 'public/project-media/fusion-scanner/Screenshot_2025-02-08_at_11.47.11.png',
    gallery: [
      'public/project-media/fusion-scanner/Screenshot_2025-02-08_at_11.45.38.png',
      'public/project-media/fusion-scanner/Screenshot_2025-02-08_at_11.47.50.png',
      'public/project-media/fusion-scanner/Screenshot_2025-02-08_at_12.27.32.png',
      'public/project-media/fusion-scanner/Screenshot_2025-02-08_at_20.43.27.png',
      'public/project-media/fusion-scanner/Screenshot_2025-02-09_at_10.50.15.png',
    ],
    sections: [
      {
        header: 'Project Context',
        body: [
          'Fusion Scanner is a browser extension concept created to support users facing language barriers and reading disabilities.',
          'The work addressed comprehension friction in everyday long-form digital reading.',
        ],
      },
      {
        header: 'Limitations of Current Solutions',
        body: [
          'Existing tools either lacked structured editing/regeneration controls or omitted summarization capabilities.',
          'Users needed in-context support with clearer control over output quality and format.',
        ],
      },
      {
        header: 'Target User Groups',
        body: [
          'Primary users included non-native English readers and users with reading-comprehension constraints.',
          'Secondary users included academic professionals, tutors, and heavy digital readers who benefit from reading acceleration.',
        ],
      },
      {
        header: 'User Interviews, Affinity Diagram & Personas',
        body: [
          'Interviews with target users were synthesized into affinity clusters and translated into personas.',
          'This process surfaced recurring needs around controllable summaries, transparent feedback, and recovery from weak AI outputs.',
        ],
      },
      {
        header: 'Wireframes & Interactive Prototype',
        body: [
          'The design evolved from structure-first wireframes to interactive prototype states focused on summarization workflows.',
          'Interaction emphasis was placed on clarity, user control, and minimizing context switches while reading.',
        ],
      },
      {
        header: 'Evaluation & Analysis',
        bullets: [
          'Usability tests and heuristics identified gaps in error prevention, status visibility, and guidance.',
          'Regeneration needed more granularity so users could refine specific summary sections rather than entire outputs.',
          'Help and documentation had to be explicit for first-time feature discoverability.',
        ],
      },
      {
        header: 'Redesign Iterations',
        bullets: [
          'Added feedback collection before summary regeneration to steer AI output quality.',
          'Separated regeneration controls across summary sections for better user control.',
          'Introduced high-risk action warnings, clearer success/error states, and richer help documentation.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Shaped an extension concept that demonstrates practical assistive reading support in everyday web experiences.',
        ],
      },
    ],
  },
  'kita-communication-intervention': {
    subtitle: 'Communication intervention from blind box concept to brochure for Kita.',
    timeline: '2024',
    tools: 'Design strategy, communication design',
    gallery: [],
    sections: [
      {
        header: 'Project Overview',
        body: [
          'This project translated communication goals into tangible brand and information touchpoints for Kita.',
        ],
      },
      {
        header: 'Challenge',
        body: [
          'The core challenge was aligning messaging clarity with audience understanding across diverse formats.',
        ],
      },
      {
        header: 'Approach',
        bullets: [
          'Mapped communication gaps between concept intent and audience interpretation.',
          'Developed artifacts that improved message consistency from discovery to brochure touchpoints.',
          'Iterated messaging and visual hierarchy for stronger comprehension outcomes.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Delivered a clearer communication pathway that strengthened brand understanding and presentation coherence.',
        ],
      },
    ],
  },
  'brand-style-guide': {
    subtitle: 'Comprehensive brand style system across typography, layout, and visual identity.',
    timeline: '2023',
    tools: 'Adobe Illustrator, Adobe InDesign, Adobe Photoshop',
    heroImage: 'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-01.png',
    gallery: [
      'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-02.png',
      'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-03.png',
      'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-04.png',
      'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-05.png',
      'public/project-media/brand-style-guide/FP__BrandStyleGuide_W4__e0958068_NiikSeah-06.png',
    ],
    sections: [
      {
        header: 'Project Overview',
        body: [
          'Brand Style Guide established a structured visual language for consistent communication across materials.',
        ],
      },
      {
        header: 'Scope',
        bullets: [
          'Defined typography systems, color usage, and compositional principles.',
          'Created reusable visual rules for print and digital outputs.',
          'Documented standards to support consistency across future asset creation.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Produced a practical design system artifact enabling coherent brand execution at scale.',
        ],
      },
    ],
  },
  'miscellaneous-works': {
    subtitle: 'Curated collection of graphic explorations and applied visual communication pieces.',
    timeline: '2023',
    tools: 'Adobe Illustrator, Adobe InDesign',
    heroImage: 'public/project-media/miscellaneous-works/33cb6212-d8d0-43b1-b534-acbaab4666b1.png',
    gallery: [
      'public/project-media/miscellaneous-works/Assignment2__W4__e0958068_NiikSeah_(dragged)-1.png',
      'public/project-media/miscellaneous-works/33cb6212-d8d0-43b1-b534-acbaab4666b1.png',
    ],
    sections: [
      {
        header: 'Project Overview',
        body: [
          'Miscellaneous Works compiles selected graphic experiments and polished outputs across multiple briefs.',
        ],
      },
      {
        header: 'Focus Areas',
        bullets: [
          'Composition and layout clarity.',
          'Visual hierarchy for communication effectiveness.',
          'Stylistic experimentation while maintaining readability and intent.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'The collection demonstrates breadth in visual direction and strong execution fundamentals.',
        ],
      },
    ],
  },
  'magic-of-resilience': {
    subtitle: 'Non-fiction short documentary spotlighting local business Meta Illusions.',
    timeline: '2023',
    tools: 'Adobe Premiere Pro',
    heroImage: 'public/project-media/magic-of-resilience/Screenshot_2025-01-24_at_15.47.19.png',
    gallery: ['public/project-media/magic-of-resilience/Screenshot_2025-01-24_at_15.47.19.png'],
    sections: [
      {
        header: 'Project Overview',
        body: [
          'Magic of Resilience is a non-fiction short documentary centered on storytelling through grounded visual craft.',
        ],
      },
      {
        header: 'Role',
        body: [
          'As Director of Photography, I focused on visual language, shot planning, and continuity to support the documentary narrative.',
        ],
      },
      {
        header: 'Production Approach',
        bullets: [
          'Designed shot strategy to balance authenticity with visual coherence.',
          'Captured footage with attention to tone, pacing, and subject context.',
          'Collaborated through post-production to preserve narrative intent.',
        ],
      },
      {
        header: 'Outcome',
        body: [
          'Delivered a completed documentary piece showcasing local resilience through a cohesive visual narrative.',
        ],
      },
    ],
  },
};
