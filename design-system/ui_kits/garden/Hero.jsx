function Hero() {
  return (
    <section className="aurora-bg gn-hero">
      <div className="gn-hero-inner">
        <div className="eyebrow">§ Field notes, 2026</div>
        <h1 className="gn-hero-title">
          <em>A garden</em> grows<br/>
          in public.
        </h1>
        <p className="gn-hero-lede">
          Essays, half-thoughts, and reading logs from <em>niik</em>.
          Some notes are seedlings; some are evergreen. Everything is a draft.
        </p>
        <div style={{display:'flex', gap:12, marginTop:28}}>
          <a className="btn btn-primary">Browse notes <i data-lucide="arrow-right" className="icon"></i></a>
          <a className="btn btn-ghost">What I'm reading</a>
        </div>
      </div>
    </section>
  );
}
window.Hero = Hero;
