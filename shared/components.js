// Shared UI atoms for niik's portfolio skeleton.
// Loaded as a plain script. Exposes globals on window.

(function () {
  const e = React.createElement;
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  const isGithubPagesHost = window.location.hostname.endsWith('github.io');
  const basePath =
    isGithubPagesHost && pathParts.length > 0 && !pathParts[0].includes('.')
      ? `/${pathParts[0]}/`
      : '/';
  const toSitePath = (relativePath) => `${basePath}${relativePath}`;

  // ─── Icon (Lucide-style) ───────────────────────────────
  const iconPaths = {
    search: [e('circle', { key: 'c', cx: 11, cy: 11, r: 7 }), e('path', { key: 'p', d: 'm20 20-3-3' })],
    arrowR: e('path', { d: 'M5 12h14M13 6l6 6-6 6' }),
    arrowUR: [e('path', { key: 'a', d: 'M7 17 17 7' }), e('path', { key: 'b', d: 'M7 7h10v10' })],
    chevL: e('path', { d: 'M15 6l-6 6 6 6' }),
    github: e('path', { d: 'M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22' }),
    twitter: e('path', { d: 'M18 2h3l-7.5 8.5L22 22h-6.8l-5.3-6.9L3.7 22H.7l8-9.1L.3 2h7l4.8 6.4L18 2z' }),
    linkedin: [e('path', { key: 'a', d: 'M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z' }), e('rect', { key: 'b', x: 2, y: 9, width: 4, height: 12 }), e('circle', { key: 'c', cx: 4, cy: 4, r: 2 })],
    mail: [e('rect', { key: 'r', x: 2, y: 4, width: 20, height: 16, rx: 2 }), e('path', { key: 'p', d: 'm22 6-10 7L2 6' })],
    rss: [e('path', { key: 'a', d: 'M4 11a9 9 0 0 1 9 9' }), e('path', { key: 'b', d: 'M4 4a16 16 0 0 1 16 16' }), e('circle', { key: 'c', cx: 5, cy: 19, r: 1 })],
    filter: e('path', { d: 'M22 3H2l8 9.5V19l4 2v-8.5L22 3z' }),
    layout: [e('rect', { key: 'r', x: 3, y: 3, width: 18, height: 18, rx: 2 }), e('path', { key: 'p', d: 'M9 3v18M3 9h18' })],
    sliders: [e('path', { key: 'a', d: 'M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6' })],
    x: [e('line', { key: 'a', x1: 6, y1: 6, x2: 18, y2: 18 }), e('line', { key: 'b', x1: 6, y1: 18, x2: 18, y2: 6 })],
    quote: e('path', { d: 'M3 21c3 0 7-1 7-8V5c0-1.25-.8-2-2-2H4c-1.25 0-2 .75-2 2v6c0 1.25.75 2 2 2h2c0 1-.25 4-3 4v4zm12 0c3 0 7-1 7-8V5c0-1.25-.8-2-2-2h-4c-1.25 0-2 .75-2 2v6c0 1.25.75 2 2 2h2c0 1-.25 4-3 4v4z' }),
  };
  const Icon = ({ name, size = 18, style }) =>
    e('svg', {
      viewBox: '0 0 24 24', width: size, height: size,
      style: { display: 'inline-block', verticalAlign: 'middle', ...style },
      fill: 'none', stroke: 'currentColor', strokeWidth: 1.75,
      strokeLinecap: 'round', strokeLinejoin: 'round',
    }, iconPaths[name]);

  // ─── Nav ────────────────────────────────────────────────
  const Nav = ({ current = 'home' }) => {
    const links = [
      { key: 'home', href: toSitePath('index.html'), label: 'home' },
      { key: 'portfolio', href: toSitePath('portfolio.html'), label: 'projects' },
    ];
    return e('header', { className: 'nav' },
      e('a', { href: toSitePath('index.html'), className: 'nav__brand' },
        e('img', { src: toSitePath('design-system/assets/brand/niik-mark.svg'), alt: '' }),
        e('span', null, 'niik', e('span', { className: 'dot' }, '.')),
      ),
      e('nav', { className: 'nav__links' },
        links.map(l => e('a', {
          key: l.key, href: l.href, className: 'nav__link',
          'aria-current': current === l.key ? 'page' : undefined,
        }, l.label))
      ),
      e('div', { className: 'nav__spacer' }),
      e('div', { className: 'nav__meta' },
        e('span', { className: 'spark' }),
        e('span', null, 'open to work'),
      ),
    );
  };

  // ─── Footer ─────────────────────────────────────────────
  const Footer = () =>
    e('footer', { className: 'footer' },
      e('span', null, 'tended with care · last update ', e('span', { className: 'slot' }, 'date')),
      e('span', { style: { display: 'flex', gap: 16, alignItems: 'center' } },
        e('a', { href: 'writing.html' }, e(Icon, { name: 'rss', size: 13 }), ' feed'),
        e('span', null, '·'),
        e('span', null, '© niik, 2026'),
      ),
    );

  // ─── Eyebrow ────────────────────────────────────────────
  const Eyebrow = ({ children, style }) =>
    e('div', { className: 'eyebrow', style }, children);

  // ─── Slot — marks a replace-me block ────────────────────
  const Slot = ({ children }) => e('span', { className: 'slot' }, children);

  // ─── Kind chip ──────────────────────────────────────────
  const Kind = ({ type = 'uiux', children }) =>
    e('span', { className: `kind kind--${type}` }, children);

  // ─── Project Card ───────────────────────────────────────
  const ProjectCard = ({ project, showThumb = true, href }) => {
    const p = project;
    return e('a', { href: href || p.href || '#', className: 'card' },
      showThumb && e('div', { className: 'card__thumb' }, p.thumbLabel || 'project image'),
      e('div', { className: 'card__meta' },
        e(Kind, { type: p.kind }, p.kindLabel),
        e('span', { className: 'dot' }),
        e('span', null, p.year || e(Slot, null, 'year')),
        e('span', { className: 'dot' }),
        e('span', null, p.role || e(Slot, null, 'role')),
      ),
      e('h3', { className: 'card__title' }, p.title || e(Slot, null, 'project title')),
      e('p', { className: 'card__excerpt' }, p.excerpt || e(Slot, null, 'one–two sentence summary of the problem, approach, and outcome.')),
      e('div', { className: 'card__foot' },
        e('span', null, (p.tags || []).slice(0, 3).map((t, i) =>
          e('span', { key: i, className: 'tag', style: { marginRight: 6 } }, '#', t)
        )),
        e('span', { className: 'arrow' }, 'read →'),
      ),
    );
  };

  // ─── List row variant ───────────────────────────────────
  const ListRow = ({ project }) => {
    const p = project;
    return e('a', { href: p.href || '#', className: 'list-row' },
      e('span', { className: 'list-row__year' }, p.year || '—'),
      e('span', null,
        e('div', { className: 'list-row__title' }, p.title || e(Slot, null, 'project title')),
        e('div', { className: 'list-row__excerpt' }, p.excerpt || e(Slot, null, 'short line')),
      ),
      e('span', { className: 'list-row__kind' }, e(Kind, { type: p.kind }, p.kindLabel)),
      e('span', { className: 'list-row__arrow' }, '→'),
    );
  };

  // ─── Tweaks infra ──────────────────────────────────────
  function useTweaksHost() {
    const [open, setOpen] = React.useState(false);
    React.useEffect(() => {
      function onMsg(ev) {
        const d = ev.data || {};
        if (d.type === '__activate_edit_mode') setOpen(true);
        if (d.type === '__deactivate_edit_mode') setOpen(false);
      }
      window.addEventListener('message', onMsg);
      window.parent.postMessage({ type: '__edit_mode_available' }, '*');
      return () => window.removeEventListener('message', onMsg);
    }, []);
    return [open, setOpen];
  }
  function persistTweak(key, value) {
    window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { [key]: value } }, '*');
  }

  Object.assign(window, {
    Icon, Nav, Footer, Eyebrow, Slot, Kind, ProjectCard, ListRow,
    useTweaksHost, persistTweak,
  });
})();
