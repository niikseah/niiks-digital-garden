function stateMeta(s) {
  if (s === 'evergreen') return { dot: '#f0b35a', label: '✺ Evergreen', color: '#f0b35a' };
  if (s === 'budding')   return { dot: '#e89bc2', label: 'Budding',    color: '#e89bc2' };
  if (s === 'uprooted')  return { dot: '#e8697a', label: 'Uprooted',   color: '#e8697a' };
  return { dot: '#6fb38a', label: 'Seedling', color: '#6fb38a' };
}

function NoteCard({ note, onOpen }) {
  const m = stateMeta(note.state);
  return (
    <article className="card gn-note" onClick={onOpen}>
      <div className="gn-note-meta">
        <span className="chip" style={{color:m.color, borderColor:'rgba(124,184,255,.18)'}}>
          <span className="chip-dot" style={{background:m.dot}}></span>{m.label}
        </span>
        <span className="gn-note-date">{note.date}</span>
      </div>
      <h3 className="gn-note-title" dangerouslySetInnerHTML={{__html: note.title}} />
      <p className="gn-note-excerpt">{note.excerpt}</p>
      <div className="gn-note-tags">
        {note.tags.map(t => <span key={t} className="chip" style={{fontSize:10}}>#{t}</span>)}
        <span className="gn-note-read">{note.read} · read on →</span>
      </div>
    </article>
  );
}
window.NoteCard = NoteCard;
window.stateMeta = stateMeta;
