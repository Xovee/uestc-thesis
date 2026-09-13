"""Check rendered reference hit areas, unlinked stars, and an intervening float page."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


def inspect(path: Path) -> dict:
    reader = PdfReader(path)
    result = {'pdf': str(path), 'pages': len(reader.pages), 'boundaries': [], 'errors': []}
    errors = result['errors']

    def require(condition, message):
        if not condition:
            errors.append(message)

    def compact(text):
        return re.sub(r'\s+', '', text)

    texts = [compact(p.extract_text()) for p in reader.pages]
    links = []
    with pdfplumber.open(path) as layout:
        for number, page in enumerate(reader.pages):
            page_links = []
            for ref in page.get('/Annots', []):
                a = ref.get_object()
                if a.get('/Subtype') != '/Link':
                    continue
                x0, y0, x1, y1 = map(float, a['/Rect'])
                top, bottom = float(page.mediabox.height) - y1, float(page.mediabox.height) - y0
                target = str(a.get('/A', {}).get('/D', a.get('/Dest', '')))
                hit = [c for c in layout.pages[number].chars
                       if x0 - .2 <= (c['x0'] + c['x1']) / 2 <= x1 + .2
                       and top - .5 <= (c['top'] + c['bottom']) / 2 <= bottom + .5]
                page_links.append({'target': target, 'rect': [x0, top, x1, bottom],
                                   'text': compact(''.join(c['text'] for c in hit))})
                require(y0 >= 75 and y1 <= 770,
                        f'Page {number + 1}: link leaked into header/footer: {target}')
                require(target in reader.named_destinations,
                        f'Page {number + 1}: unknown target {target}')
            links.append(page_links)

        def marker_page(marker):
            pattern = re.compile(re.escape(marker) + r'(?!STAR|-CITATION)')
            found = [i for i, text in enumerate(texts) if pattern.search(text)]
            require(len(found) == 1, f'{marker}: expected one page, got {found}')
            return found[0] if len(found) == 1 else None

        for case, expected_text, linked in [
            ('REF', '1-10', True), ('AUTOREF', None, True), ('PAGEREF', '1', True),
            ('BAREMATH', '1−10', True),
            ('REFSTAR', '1-10', False), ('AUTOSTAR', None, False), ('PAGESTAR', '1', False),
            ('FLOAT', '1-10', True),
        ]:
            start, end = marker_page('R01-' + case), marker_page('R01-END-' + case)
            if start is None or end is None:
                continue
            require(end == start + (2 if case == 'FLOAT' else 1),
                    f'{case}: expected reference at tested page boundary')
            relevant = [link for i in range(start, end + 1) for link in links[i]
                        if link['target'] != 'cite.r01:control']
            require(len(relevant) == int(linked), f'{case}: unexpected reference link count {len(relevant)}')
            if linked and len(relevant) == 1:
                require(relevant[0]['target'] == 'figure.caption.1', f'{case}: wrong target')
                actual = relevant[0]['text']
                require(actual == expected_text if expected_text else actual in {'图1-10', 'Figure1-10'},
                        f'{case}: link does not cover the actual reference: {actual!r}')
                require(relevant[0] in links[end], f'{case}: reference link is not on its text page')
            if case == 'FLOAT':
                require(len(links[start + 1]) == 1 and links[start + 1][0]['target'] == 'cite.r01:control',
                        'Float page: citation link missing or contaminated by reference link')
                if links[start + 1]:
                    require(links[start + 1][0]['text'] == '1', 'Float citation hit area is incorrect')
            result['boundaries'].append({'case': case, 'start_page': start + 1, 'end_page': end + 1,
                                         'reference_links': relevant})

        normal = marker_page('R01-NORMAL')
        if normal is not None:
            for target in ['figure.caption.1', 'table.caption.2', 'equation.1.10', 'chapter.1', 'section.1.1']:
                require(any(a['target'] == target for a in links[normal]), f'Normal references: missing {target}')
            star_hits = layout.pages[normal].search(r'R01-STAR[\s\S]*?R01-STAR-END')
            require(len(star_hits) == 1, 'Could not locate the unlinked-star reference row')
            if star_hits:
                star = star_hits[0]
                require(not any(a['rect'][1] < star['bottom'] - .5 and a['rect'][3] > star['top'] + .5
                                for a in links[normal]), 'Starred reference unexpectedly has a link')

    def outline_titles(items):
        for item in items:
            if isinstance(item, list):
                yield from outline_titles(item)
            else:
                yield str(item.get('/Title', ''))

    titles = list(outline_titles(reader.outline))
    require(any('1-10' in title for title in titles), 'Reference values missing from PDF bookmark')
    require(not any('??' in title or 'mbox' in title for title in titles), 'Broken reference in PDF bookmark')
    log = path.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
    require(not re.search(r'Reference .* undefined|There were undefined references|Token not allowed in a PDF string', log),
            'Final log has an undefined reference or invalid bookmark token')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    args = parser.parse_args()
    result = inspect(args.pdf)
    args.pdf.with_suffix('.links.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for error in result['errors']:
        print('FAIL:', error)
    if result['errors']:
        return 1
    print(f'PASS: {args.pdf.name}, {result["pages"]} pages; reference regions, stars, float citation, and bookmarks verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
