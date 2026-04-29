const { useState, useEffect } = React;

function Sidebar({ active, setActive, notes }) {
  return (
    <aside className="gh-side">
      <div className="gh-brand">
        <span style={{fontFamily:'var(--font-display)', fontStyle:'italic', fontSize:22}}>niik</span>
        <span style={{color:'var(--electric-glow)', marginLeft:6}}>✺</span>
        <span style={{fontFamily:'var(--font-mono)', fontSize:9, color:'var(--fg-4)', letterSpacing:'.2em', marginLeft:'auto'}}>GREENHOUSE</span>
      </div>
      <div className="gh-search">
        <i data-lucide="search" className="icon" style={{width:14,height:14}}></i>
        <input className="input" placeholder="Find a note…" style={{padding:'6px 10px', fontSize:13, background:'transparent', border:0}} />
        <span className="kbd">⌘K</span>
      </div>
      <div className="gh-section-title">Notes</div>
      <ul className="gh-list">
        {notes.map(n => (
          <li key={n.id}
              className={'gh-item ' + (active === n.id ? 'on' : '')}
              onClick={() => setActive(n.id)}>
            <span className="gh-item-dot" style={{background: n.state==='evergreen'?'#f0b35a':n.state==='budding'?'#e89bc2':'#6fb38a'}}></span>
            <span className="gh-item-title" dangerouslySetInnerHTML={{__html: n.title}} />
            <span className="gh-item-date">{n.date}</span>
          </li>
        ))}
      </ul>
      <div className="gh-section-title">Tags</div>
      <div style={{display:'flex',flexWrap:'wrap',gap:6}}>
        {['writing','gardening','process','reading','language','field'].map(t =>
          <span key={t} className="chip" style={{fontSize:10}}>#{t}</span>)}
      </div>
    </aside>
  );
}

function Composer({ note, onChange }) {
  return (
    <main className="gh-main">
      <header className="gh-topbar">
        <div style={{display:'flex',alignItems:'center',gap:10}}>
          <span className="chip" style={{color:'#6fb38a',borderColor:'rgba(111,179,138,.35)'}}>
            <span className="chip-dot" style={{background:'#6fb38a'}}></span>Seedling
          </span>
          <span style={{fontFamily:'var(--font-mono)',fontSize:11,color:'var(--fg-4)'}}>draft · saved 2m ago</span>
        </div>
        <div style={{marginLeft:'auto',display:'flex',gap:8}}>
          <button className="btn btn-quiet" title="Preview"><i data-lucide="eye" className="icon"></i></button>
          <button className="btn btn-quiet" title="Link"><i data-lucide="link" className="icon"></i></button>
          <button className="btn btn-ghost">Publish</button>
        </div>
      </header>
      <div className="gh-canvas">
        <input className="gh-title" value={note.title.replace(/<[^>]+>/g,'')} onChange={e => onChange({...note, title: e.target.value})} />
        <div style={{display:'flex',gap:10,color:'var(--fg-3)',fontFamily:'var(--font-mono)',fontSize:11,margin:'6px 0 28px'}}>
          <span>{note.date}</span><span>·</span><span>{note.read}</span><span>·</span>
          <span>{note.tags.map(t=>'#'+t).join(' ')}</span>
        </div>
        <div className="gh-body">
          <p>{note.excerpt}</p>
          <p><em>I'm planting this half-thought here to return to.</em> The whole pleasure of a garden is coming back and finding it slightly different than you left it.</p>
          <blockquote>A garden grows in public. Everything here is a draft.</blockquote>
          <p>Tags, links, and backlinks compose themselves as you type. Press <span className="kbd">⌘</span><span className="kbd">↵</span> to plant.</p>
        </div>
      </div>
    </main>
  );
}

function Inspector({ note }) {
  return (
    <aside className="gh-inspect">
      <div className="gh-section-title">Inspector</div>
      <div className="gh-field"><span className="gh-lab">State</span><span className="chip" style={{color:'#6fb38a',borderColor:'rgba(111,179,138,.35)'}}><span className="chip-dot" style={{background:'#6fb38a'}}></span>Seedling</span></div>
      <div className="gh-field"><span className="gh-lab">Planted</span><span>{note.date}</span></div>
      <div className="gh-field"><span className="gh-lab">Tended</span><span>2 times</span></div>
      <div className="gh-field"><span className="gh-lab">Reading</span><span>{note.read}</span></div>
      <div className="gh-section-title" style={{marginTop:24}}>Backlinks</div>
      <ul style={{listStyle:'none',padding:0,margin:0,color:'var(--fg-2)',fontSize:13,lineHeight:1.8}}>
        <li>↩ <em>On the pleasure of unfinishing</em></li>
        <li>↩ <em>Walking as a kind of reading</em></li>
      </ul>
      <div className="gh-section-title" style={{marginTop:24}}>Actions</div>
      <div style={{display:'flex',flexDirection:'column',gap:6}}>
        <button className="btn btn-quiet" style={{justifyContent:'flex-start'}}><i data-lucide="archive" className="icon"></i> Archive</button>
        <button className="btn btn-quiet" style={{justifyContent:'flex-start',color:'var(--rose)'}}><i data-lucide="trash-2" className="icon"></i> Uproot</button>
      </div>
    </aside>
  );
}

window.Sidebar = Sidebar;
window.Composer = Composer;
window.Inspector = Inspector;
