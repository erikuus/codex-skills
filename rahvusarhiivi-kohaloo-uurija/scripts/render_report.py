#!/usr/bin/env python3
"""Render a local, printable report from JSON. Python standard library only."""
import argparse
import base64
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

LABELS = {'otsene': 'Otsene allikas', 'jareldus': 'Järeldus',
          'oletus': 'Oletus', 'ebakindel': 'Ebakindel lugem',
          'kontrollimata': 'Kontrollimata', 'malestus': 'Mälestus'}

def esc(value):
    return html.escape(str(value), quote=True)

def url(value):
    """Only explicit HTTP(S) source links; no executable or local-file URLs."""
    value = str(value)
    parsed = urlsplit(value)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or any(ord(c) < 32 for c in value):
        raise ValueError(f'Allikaviide peab olema HTTP(S) URL: {value!r}')
    return esc(value)

class Renderer:
    def __init__(self, data, base):
        self.data, self.base = data, base
        if not isinstance(data.get('demo', False), bool):
            raise ValueError('demo peab olema JSON tõeväärtus true või false')
        self.sources = {}
        for s in data.get('sources', []):
            ident = s['id']
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', ident) or ident in self.sources:
                raise ValueError(f'Vigane või korduv allika ID: {ident}')
            self.sources[ident] = s

    def refs(self, items):
        links = []
        for item in items:
            item = {'source': item} if isinstance(item, str) else item
            ident = item['source']
            if ident not in self.sources:
                raise ValueError(f'Puuduv allikas: {ident}')
            locator = item.get('locator', '')
            label = ident + (': ' + locator if locator else '')
            links.append(f'<a href="#source-{esc(ident)}" title="{esc(self.sources[ident]["title"])}">[{esc(label)}]</a>')
        return '<span class="refs">' + ' '.join(links) + '</span>' if links else ''

    def text(self, value):
        if isinstance(value, str):
            return esc(value)
        badge = ''
        if value.get('status'):
            state = value['status']
            if state not in LABELS:
                raise ValueError(f'Tundmatu kindlusmärgend: {state}')
            badge = f'<span class="badge {state}">{LABELS[state]}</span>'
        return badge + esc(value['text']) + self.refs(value.get('refs', []))

    def figure(self, b):
        if b.get('image'):
            # Embed local raster images to make the report portable/offline.
            path = (self.base / b['image']).resolve()
            raw = path.read_bytes()
            if raw.startswith(b'\x89PNG\r\n\x1a\n'):
                mime = 'image/png'
            elif raw.startswith(b'\xff\xd8\xff'):
                mime = 'image/jpeg'
            elif raw[:4] == b'RIFF' and raw[8:12] == b'WEBP':
                mime = 'image/webp'
            else:
                raise ValueError(f'Pilt peab olema PNG, JPEG või WebP: {path}')
            if not b.get('alt'):
                raise ValueError('Pildil puudub alt-tekst')
            image = f'<img src="data:{mime};base64,{base64.b64encode(raw).decode()}" alt="{esc(b["alt"])}">'
        elif self.data.get('demo'):
            image = '<div class="image-placeholder"><strong>Arhiivipildi koht</strong><span>Vormistuse näidis · ajaloolist pilti pole lisatud</span></div>'
        else:
            raise ValueError('Lõppraporti pildiplokil puudub image')
        if not b.get('refs'):
            raise ValueError('Pildiplokil puudub allikaviide')
        return f'<figure>{image}<figcaption><strong>{esc(b["title"])}</strong> {esc(b.get("caption", ""))}{self.refs(b["refs"])}</figcaption></figure>'

    def block(self, b):
        kind = b['type']
        if kind == 'paragraph':
            return '<p>' + self.text(b) + '</p>'
        if kind == 'notice':
            tone = ' warning' if b.get('tone') == 'warning' else ''
            title = f'<h3>{esc(b["title"])}</h3>' if b.get('title') else ''
            return f'<div class="notice{tone}">{title}<p>{self.text(b)}</p></div>'
        if kind == 'list':
            tag = 'ol' if b.get('ordered') else 'ul'
            return f'<{tag}>' + ''.join('<li>' + self.text(x) + '</li>' for x in b['items']) + f'</{tag}>'
        if kind == 'table':
            n = len(b['columns'])
            if not n or any(len(r) != n for r in b['rows']):
                raise ValueError('Tabeli veergude arv ei klapi ridadega')
            caption = f'<caption>{esc(b["caption"])}</caption>' if b.get('caption') else ''
            heads = ''.join(f'<th scope="col">{esc(c)}</th>' for c in b['columns'])
            rows = ''.join('<tr>' + ''.join('<td>' + self.text(c) + '</td>' for c in row) + '</tr>' for row in b['rows'])
            return f'<div class="table-scroll" tabindex="0" role="region" aria-label="{esc(b.get("caption", "Andmetabel"))}"><table>{caption}<thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>'
        if kind == 'timeline':
            events = []
            for ev in b['events']:
                events.append(f'<li class="event"><time>{esc(ev["date"])}</time><div class="event-content"><span class="event-kind">{esc(ev.get("kind", ""))}</span><p>{self.text(ev)}</p></div></li>')
            return '<ol class="timeline">' + ''.join(events) + '</ol>'
        if kind == 'figure':
            return self.figure(b)
        if kind == 'document':
            image = self.figure(b['figure']) if b.get('figure') else ''
            return (f'<article class="document"><h3>{esc(b["title"])}</h3>{image}'
                    f'<p class="document-label">Originaallugem</p><blockquote class="transcription">{esc(b["original"])}</blockquote>'
                    f'<p class="document-label">Tõlge ja selgitus</p><p>{self.text(b["translation"])}</p>'
                    f'<p>{self.text(b["note"])}</p>{self.refs(b.get("refs", []))}</article>')
        raise ValueError(f'Tundmatu ploki tüüp: {kind}')

    def render(self, template):
        sections, toc, seen = [], [], set()
        for section in self.data['sections']:
            ident = section['id']
            if not re.fullmatch(r'sec-[1-9][0-9]*', ident) or ident in seen:
                raise ValueError(f'Vigane või korduv peatüki ID: {ident}')
            seen.add(ident)
            blocks = section.get('blocks', [])
            if not blocks:
                continue
            heading = section['title']
            toc.append(f'<li><a href="#{ident}">{esc(heading)}</a></li>')
            sections.append(f'<section class="report-section" id="{ident}"><h2>{esc(heading)}</h2>' + ''.join(self.block(b) for b in blocks) + '</section>')
        if self.sources:
            sources_heading = f'{len(sections) + 1}. Allikad ja meetod'
            toc.append(f'<li><a href="#sources">{sources_heading}</a></li>')
            sources = []
            for ident, s in self.sources.items():
                href = url(s['url'])
                sources.append(f'<li id="source-{ident}"><span class="source-id">{ident}</span><a href="{href}">{esc(s["title"])}</a><span class="source-detail">{esc(s.get("citation", ""))}</span><span class="source-detail">{esc(s.get("access", ""))}</span><span class="source-url">{esc(s["url"])}</span></li>')
            method = ''.join('<p>' + esc(p) + '</p>' for p in self.data.get('method', []))
            sections.append(f'<section class="report-section" id="sources"><h2>{sources_heading}</h2>' + method + '<ul class="source-list">' + ''.join(sources) + '</ul></section>')
        facts = []
        for fact in self.data.get('facts', []):
            facts.append(f'<div class="fact"><dt>{esc(fact["label"])}</dt><dd>{esc(fact["value"])}<small>{esc(fact.get("note", ""))}{self.refs(fact.get("refs", []))}</small></dd></div>')
        notice = ''
        if self.data.get('demo'):
            notice = '<div class="notice warning demo"><strong>Vormistuse näidis.</strong> Näidisandmed ei ole ajaloolised uurimistulemused.</div>'
        if self.data.get('notice'):
            notice += '<div class="notice"><p>' + esc(self.data['notice']) + '</p></div>'
        values = {
            'TITLE': esc(self.data['title']),
            'SUBTITLE': '<p class="subtitle">' + esc(self.data['subtitle']) + '</p>' if self.data.get('subtitle') else '',
            'META': '<span>Koostatud ' + esc(self.data['date']) + '</span><span>' + esc(self.data.get('author', '')) + '</span>',
            'NOTICE': notice, 'FACTS': '<dl class="facts">' + ''.join(facts) + '</dl>' if facts else '',
            'TOC': ''.join(toc), 'SECTIONS': '\n'.join(sections), 'FOOTER': esc(self.data.get('footer', '')),
        }
        # Single substitution pass: source text containing {{...}} stays literal.
        return re.sub(r'\{\{([A-Z]+)\}\}', lambda m: values[m[1]], template)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--template', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/report-template.html')
    args = parser.parse_args()
    try:
        data = json.loads(args.data.read_text(encoding='utf-8'))
        result = Renderer(data, args.data.resolve().parent).render(args.template.read_text(encoding='utf-8'))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f'Raport jäi loomata: {exc}\n')
    print(args.output.resolve())

if __name__ == '__main__':
    main()
