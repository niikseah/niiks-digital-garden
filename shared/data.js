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
        header: 'Project Overview',
        body: [
          'Pantry Pal is a mobile UI/UX concept designed to tackle food waste by simplifying pantry management and meal planning.',
          'The project centered on helping households track groceries better, reduce duplicate purchases, and turn ingredients into actionable meal plans.',
        ],
      },
      {
        header: 'Research & Key Findings',
        bullets: [
          'Conducted user interviews and synthesized responses into recurring themes around convenience and low visibility of food expiry.',
          'Built empathy maps and personas to ground feature priorities in real household behaviors.',
          'Validated that users preferred quicker, low-friction input methods such as barcode scanning and voice entry.',
        ],
      },
      {
        header: 'Design Approach',
        body: [
          'Designed pantry navigation, meal planning flows, and expiry tracking views to make food state and usage immediately clear.',
          'Ran low-fidelity prototyping and iterative user testing to refine onboarding, pantry interactions, and recipe recommendations.',
        ],
      },
      {
        header: 'Outcome & Skills',
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
        header: 'Project Overview',
        body: [
          'FlexiJio is a desktop video conferencing platform concept specifically designed for fitness sessions.',
        ],
      },
      {
        header: 'Problem',
        body: [
          'General-purpose video tools often miss session-specific controls needed for coaching, class pacing, and participant visibility.',
        ],
      },
      {
        header: 'Approach',
        bullets: [
          'Researched instructor and participant workflow needs unique to remote fitness.',
          'Proposed interface patterns that reduce control switching during live sessions.',
          'Mapped feature priorities to preserve flow between instruction and feedback loops.',
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
        header: 'Project Overview',
        body: [
          'Fusion Scanner is a browser extension concept created to support users facing language barriers and reading disabilities.',
        ],
      },
      {
        header: 'Problem & User Need',
        body: [
          'Web reading often assumes a single comprehension style, which can exclude users who need adaptive support.',
          'The project explored ways to make reading assistance available in-context without disrupting browsing flow.',
        ],
      },
      {
        header: 'Design Strategy',
        bullets: [
          'Identified critical support moments where users need immediate clarity while reading.',
          'Designed assistive interaction patterns that stay lightweight and non-intrusive.',
          'Iterated prototype direction with usability and accessibility priorities at the core.',
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
