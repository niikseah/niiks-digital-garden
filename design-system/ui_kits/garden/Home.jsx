const NOTES = [
  { id:'n1', state:'evergreen', date:'tended weekly',
    title:'On the pleasure of <em>unfinishing</em>',
    excerpt:"I keep a folder of things I will not finish. Not the unfinished-because-abandoned kind — the unfinished-on-purpose kind.",
    tags:['writing','gardening'], read:'6 min' },
  { id:'n2', state:'seedling', date:'two Tuesdays ago',
    title:'Three notes becoming an essay',
    excerpt:"I'm planting these three half-thoughts next to each other to see whether they root.",
    tags:['process'], read:'4 min' },
  { id:'n3', state:'budding', date:'last Sunday',
    title:'Walking as a kind of reading',
    excerpt:"Solnit again. The sentence that undid me: the object of walking is never the destination.",
    tags:['reading','walking'], read:'3 min' },
  { id:'n4', state:'seedling', date:'earlier this week',
    title:'A very small defense of <em>maybe</em>',
    excerpt:'"I don\'t know yet" is a complete sentence and, some days, the bravest one.',
    tags:['language'], read:'2 min' },
  { id:'n5', state:'budding', date:'mid-month',
    title:'Notes on the colour of weather',
    excerpt:'A log of every sky I noticed this month — pale lilac, gunmetal, pewter, bruise.',
    tags:['field','colour'], read:'5 min' },
  { id:'n6', state:'uprooted', date:'pruned',
    title:'Why I deleted my analytics',
    excerpt:"It turns out I'd rather not know. Writing for an audience of one is generous. Writing for a counter is not.",
    tags:['meta'], read:'3 min' },
];

function Home({ onOpen }) {
  return (
    <>
      <Hero />
      <section className="gn-section">
        <div className="gn-section-head">
          <div className="eyebrow">§ Recently tended</div>
          <h2 className="gn-section-title">Notes in the garden</h2>
          <p className="gn-section-lede">Six notes, various stages. Seedlings are new and rough; evergreens get tended every week.</p>
        </div>
        <div className="gn-notes-grid">
          {NOTES.map(n => <NoteCard key={n.id} note={n} onOpen={() => onOpen(n)} />)}
        </div>
      </section>
      <section className="gn-section">
        <ReadingList />
      </section>
    </>
  );
}
window.Home = Home;
window.NOTES = NOTES;
