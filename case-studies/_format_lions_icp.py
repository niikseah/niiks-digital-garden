#!/usr/bin/env python3
"""Regenerate structured HTML for lions-befrienders-communications-plan.html from extracted .txt."""
from __future__ import annotations

import html as htmllib
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TXT = BASE / "public/documents/NM4208_LionsBefrienders_ICP-extracted.txt"
HTML = BASE / "case-studies/lions-befrienders-communications-plan.html"

HEADINGS = [
    "PR Problems/Opportunities",
    "SWOT Analysis",
    "Publics",
    "Strategic Plan",
    "Gantt Chart",
    "Appendix",
    "References",
]
APPENDIX_SUB = frozenset({"Brochure", "Social Media Campaign", "Microsite", "Magazine"})
TABLE_HEADER = ["Public", "Type", "Problem", "Recognition", "Constraint Recognition", "Level of Involvement"]
DISPLAY_HEADERS = [
    "Public",
    "Type",
    "Problem recognition",
    "Constraint recognition",
    "Level of involvement",
]


def esc(s: str) -> str:
    return htmllib.escape(s, quote=True)


def esc_br(s: str) -> str:
    return esc(s).replace("\n", "<br>\n")


def prose_paragraphs(body: str) -> list[str]:
    body = body.strip()
    if not body:
        return []
    parts = [p.strip() for p in re.split(r"\s{4,}", body) if p.strip()]
    return parts if len(parts) > 1 else [body]


def normalize_intro(intro: str) -> str:
    """Join title clause to opening sentence (Word used long spaces here)."""
    intro = intro.strip()
    intro = re.sub(
        r"(Introduction to Lions Befrienders Service Association \(Singapore\))\s+(?=Singapore)",
        r"\1 — ",
        intro,
        count=1,
    )
    return intro


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s or "section"


def parse_publics_rows(table_text: str) -> tuple[bool, list[list[str]]]:
    lines = [ln.strip() for ln in table_text.splitlines() if ln.strip()]
    if len(lines) < len(TABLE_HEADER) or lines[: len(TABLE_HEADER)] != TABLE_HEADER:
        return False, []
    rest = lines[len(TABLE_HEADER) :]
    n = 5
    rows: list[list[str]] = []
    for i in range(0, len(rest), n):
        chunk = rest[i : i + n]
        if len(chunk) < n:
            break
        rows.append(chunk)
    return True, rows


def format_publics_chapter(content: str) -> list[str]:
    out: list[str] = []
    idx = content.find("\n\nPublic\n\nType\n\nProblem")
    if idx == -1:
        for p in prose_paragraphs(content):
            out.append(f"          <p>{esc_br(p)}</p>")
        return out

    grunig = content[:idx].strip()
    rest = content[idx:].strip()
    fp = rest.find("\n\nFrom the Publics identified")
    if fp == -1:
        table_text = rest
        tail = ""
    else:
        table_text = rest[:fp].strip()
        tail = rest[fp:].strip()

    for p in prose_paragraphs(grunig):
        out.append(f"          <p>{esc_br(p)}</p>")

    ok, rows = parse_publics_rows(table_text)
    if ok and rows:
        out.append('          <div class="icp-table-wrap" role="region" aria-label="Publics matrix">')
        out.append('            <table class="icp-table">')
        out.append("              <thead><tr>")
        for h in DISPLAY_HEADERS:
            out.append(f'                <th scope="col">{esc(h)}</th>')
        out.append("              </tr></thead><tbody>")
        for row in rows:
            out.append("                <tr>")
            for j, cell in enumerate(row):
                tag = "th" if j == 0 else "td"
                scope = ' scope="row"' if j == 0 else ""
                out.append(f"                <{tag}{scope}>{esc_br(cell)}</{tag}>")
            out.append("                </tr>")
        out.append("              </tbody></table></div>")
    else:
        out.append(f'          <pre class="icp-raw-fallback">{esc(table_text)}</pre>')

    for p in prose_paragraphs(tail):
        out.append(f"          <p>{esc_br(p)}</p>")
    return out


def format_appendix(content: str) -> list[str]:
    out: list[str] = []
    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b in APPENDIX_SUB:
            out.append(f'          <h3 class="icp-subhead" id="{slugify(b)}">{esc(b)}</h3>')
            i += 1
            chunk: list[str] = []
            while i < len(blocks) and blocks[i] not in APPENDIX_SUB:
                chunk.append(blocks[i])
                i += 1
            if chunk:
                raw = "\n\n".join(chunk)
                raw = re.sub(r"\n{3,}", "\n\n", raw)
                out.append(f'          <pre class="icp-appendix-pre">{esc(raw)}</pre>')
        else:
            for p in prose_paragraphs(b):
                out.append(f"          <p>{esc_br(p)}</p>")
            i += 1
    return out


def format_references(content: str) -> list[str]:
    out: list[str] = []
    refs = [r.strip() for r in content.split("\n\n") if r.strip()]
    out.append('          <ol class="icp-refs">')
    for r in refs:
        out.append(f"            <li>{esc_br(r)}</li>")
    out.append("          </ol>")
    return out


def build_from_bits(bits: list[str]) -> str:
    lines: list[str] = []
    prelude = bits[0].strip()
    pre_blocks = [b.strip() for b in prelude.split("\n\n") if b.strip()]
    meta: list[str] = []
    intro_chunks: list[str] = []
    for b in pre_blocks:
        if len(b) < 200 and b.count("\n") == 0:
            meta.append(b)
        else:
            intro_chunks.append(b)
    intro = normalize_intro("\n\n".join(intro_chunks).strip())

    lines.append('    <section class="section icp-fulltext">')
    lines.append('      <h2 id="icp-document">Full plan — extracted text</h2>')
    lines.append(
        '      <p class="icp-fulltext-note">Structured from the plain-text extract (tables simplified). '
        '<a href="../public/documents/NM4208_LionsBefrienders_ICP-extracted.txt">Open .txt</a> · '
        '<a href="../public/documents/NM4208_AY2526S1_NiikSeah_e0958068_LionsBefrienders_ICP.docx">Download .docx</a>.</p>'
    )
    lines.append('      <nav class="icp-toc" aria-label="In this document">')
    lines.append('        <span class="icp-toc__label">Jump to</span>')
    toc = [
        ("#introduction", "Introduction"),
        ("#swot-analysis", "SWOT"),
        ("#pr-problems-opportunities", "PR problems / opportunities"),
        ("#publics", "Publics"),
        ("#strategic-plan", "Strategic plan"),
        ("#gantt-chart", "Gantt chart"),
        ("#appendix", "Appendix"),
        ("#references", "References"),
    ]
    for href, label in toc:
        lines.append(f'        <a class="icp-toc__link" href="{href}">{esc(label)}</a>')
    lines.append("      </nav>")
    lines.append('      <article class="icp-body" aria-labelledby="icp-document">')
    lines.append('        <header class="icp-doc-head">')
    for m in meta:
        lines.append(f'          <p class="icp-doc-head__line">{esc_br(m)}</p>')
    lines.append("        </header>")

    if intro:
        lines.append('        <section class="icp-chapter" id="introduction">')
        lines.append("          <h2>Introduction</h2>")
        for p in prose_paragraphs(intro):
            lines.append(f"          <p>{esc_br(p)}</p>")
        lines.append("        </section>")

    it = iter(bits[1:])
    for title in it:
        body = next(it, "")
        title = title.strip()
        sid = slugify(title)
        lines.append(f'        <section class="icp-chapter" id="{sid}">')
        lines.append(f"          <h2>{esc(title)}</h2>")
        if title == "Publics":
            inner = format_publics_chapter(body)
        elif title == "Appendix":
            inner = format_appendix(body)
        elif title == "References":
            inner = format_references(body)
        else:
            inner = [f"          <p>{esc_br(p)}</p>" for p in prose_paragraphs(body)]
        lines.extend(inner)
        lines.append("        </section>")

    lines.append("      </article>")
    lines.append("    </section>")
    return "\n".join(lines) + "\n"


def apply_heading_markers(raw: str) -> str:
    """Insert @@HRULE@@title@@ENDHR@@ before each major section."""
    raw = re.sub(r"\n\n(Appendix)\n\n", r"\n\n@@HRULE@@\1@@ENDHR@@\n\n", raw)
    raw = re.sub(r"\n\n(References)\n\n", r"\n\n@@HRULE@@\1@@ENDHR@@\n\n", raw)
    spaced_only = [h for h in HEADINGS if h not in ("Appendix", "References")]
    alt = "|".join(re.escape(h) for h in sorted(spaced_only, key=len, reverse=True))

    def repl(m: re.Match[str]) -> str:
        return f"\n\n@@HRULE@@{m.group(2)}@@ENDHR@@\n\n"

    return re.sub(rf"(\s{{4,}})({alt})(\s{{4,}})", repl, raw)


def main() -> None:
    raw = TXT.read_text(encoding="utf-8", errors="replace")
    marked = apply_heading_markers(raw)
    bits = re.split(r"\n\n@@HRULE@@(.+?)@@ENDHR@@\n\n", marked)
    new_section = build_from_bits(bits)
    html = HTML.read_text(encoding="utf-8")
    pattern = (
        r"\n\n\s+<section class=\"section icp-fulltext\">[\s\S]*?</article>\s*</section>"
        r"(?=\s*<section class=\"section icp-foot\"|\s*</main>)"
    )
    if not re.search(pattern, html):
        raise SystemExit("Could not find icp-fulltext section to replace")

    def _repl(_: re.Match[str]) -> str:
        return "\n\n" + new_section.rstrip() + "\n"

    html = re.sub(pattern, _repl, html, count=1)
    HTML.write_text(html, encoding="utf-8")
    print("Wrote", HTML)


if __name__ == "__main__":
    main()
