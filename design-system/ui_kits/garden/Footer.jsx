function Footer() {
  return (
    <footer className="gn-footer">
      <div className="gn-footer-inner">
        <div className="gn-footer-brand">
          <span style={{fontFamily:'var(--font-display)', fontStyle:'italic', fontSize:18}}>niik</span>
          <span style={{color:'var(--electric-glow)', marginLeft:8}}>✺</span>
          <div style={{fontFamily:'var(--font-mono)', fontSize:10, color:'var(--fg-4)', letterSpacing:'.18em', marginTop:4}}>DIGITAL · GARDEN · EST. 2023</div>
        </div>
        <div className="gn-footer-links">
          <a>RSS</a><span className="gn-dot">·</span>
          <a>Atom</a><span className="gn-dot">·</span>
          <a>Email</a><span className="gn-dot">·</span>
          <a>Colophon</a>
        </div>
      </div>
      <div className="gn-footer-note">Last tended — two Tuesdays ago. Everything here is a draft.</div>
    </footer>
  );
}

function Essay({ onBack }) {
  return (
    <article className="gn-essay">
      <a className="btn btn-quiet" onClick={onBack} style={{paddingLeft:0}}>
        <i data-lucide="arrow-left" className="icon"></i> back to notes
      </a>
      <div className="eyebrow" style={{marginTop:24}}>§ Essay · Evergreen ✺</div>
      <h1 className="gn-essay-title">On the pleasure of <em>unfinishing</em>.</h1>
      <div className="gn-essay-meta">
        <span>6 min</span><span className="gn-dot">·</span>
        <span>tended weekly since 2023</span><span className="gn-dot">·</span>
        <span>v14</span>
      </div>
      <p>I keep a folder of things I will not finish. Not the unfinished-because-abandoned kind — the unfinished-on-purpose kind. Notes that stay notes. Essays kept just below the boil.</p>
      <p>A garden, someone said, is a thing that happens. <em>This</em> one happens in small increments: a paragraph pruned, a link added, a tag renamed. Nothing here is a post; everything is a plot.</p>
      <blockquote>
        A garden grows in public. Notes wander. Some die back; some bloom. Everything is a draft.
      </blockquote>
      <p>The pleasure is in the tending. In coming back and finding something slightly different than you left it. In the <em>not</em>-shipping. In keeping a thing alive by not calling it done.</p>
      <div style={{textAlign:'center', color:'var(--electric-glow)', letterSpacing:'1em', margin:'48px 0 8px'}}>❋</div>
    </article>
  );
}

window.Footer = Footer;
window.Essay = Essay;
