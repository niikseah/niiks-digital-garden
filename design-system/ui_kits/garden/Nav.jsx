const { useState } = React;

function Nav({ route, setRoute }) {
  const items = [
    { id: 'home', label: 'Notes' },
    { id: 'essay', label: 'Essays' },
    { id: 'reading', label: 'Reading' },
    { id: 'now', label: 'Now' },
    { id: 'about', label: 'About' },
  ];
  return (
    <nav className="gn-nav">
      <a className="gn-brand" onClick={() => setRoute('home')}>
        <span className="gn-mark">niik</span>
        <span className="gn-rosette">✺</span>
      </a>
      <div className="gn-links">
        {items.map(it => (
          <a key={it.id}
             className={'gn-link ' + (route === it.id ? 'on' : '')}
             onClick={() => setRoute(it.id)}>{it.label}</a>
        ))}
      </div>
      <div className="gn-cmd">
        <span className="kbd">⌘</span><span className="kbd">K</span>
        <span style={{marginLeft:6, color:'var(--fg-3)'}}>search</span>
      </div>
      <button className="btn btn-ghost" style={{padding:'6px 10px'}} title="Toggle day / night">
        <i data-lucide="moon" className="icon"></i>
      </button>
    </nav>
  );
}
window.Nav = Nav;
