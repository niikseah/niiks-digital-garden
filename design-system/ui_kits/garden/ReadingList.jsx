function ReadingList() {
  const books = [
    { t: 'A Field Guide to Getting Lost', a: 'Rebecca Solnit', s: 'currently', note: '…walking as a kind of thinking.' },
    { t: 'How to Do Nothing', a: 'Jenny Odell', s: 'finished', note: 'Underlined half of it.' },
    { t: 'The Order of Time', a: 'Carlo Rovelli', s: 'paused', note: 'Will return in spring.' },
    { t: 'Draft No. 4', a: 'John McPhee', s: 'evergreen', note: 'Re-read yearly.' },
  ];
  const color = { currently:'#6fb38a', finished:'#93befd', paused:'#f0b35a', evergreen:'#e89bc2' };
  return (
    <div className="gn-reading">
      <div className="gn-reading-head">
        <div className="eyebrow">§ Reading log</div>
        <h2 className="gn-section-title">On the bedside table</h2>
      </div>
      <ul className="gn-booklist">
        {books.map(b => (
          <li key={b.t} className="gn-book">
            <span className="gn-book-dot" style={{background:color[b.s]}}></span>
            <div className="gn-book-body">
              <div className="gn-book-title"><em>{b.t}</em> <span className="gn-book-author">— {b.a}</span></div>
              <div className="gn-book-note">{b.note}</div>
            </div>
            <span className="gn-book-state">{b.s}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
window.ReadingList = ReadingList;
