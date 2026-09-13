"""Verify actual subfigure labels, caption order, references, and float placement."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import pdfplumber
from pypdf import PdfReader

TEX_PT_TO_BP = 72 / 72.27


def groups(text: str) -> list[str]:
    """Read adjacent TeX brace groups, retaining nested caption text unchanged."""
    result, depth, start = [], 0, 0
    for i, char in enumerate(text):
        if char == '{':
            if depth == 0:
                start = i+1
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                result.append(text[start:i])
    return result


def inspect(path: Path, english: bool = False) -> dict:
    result = {'pdf': str(path), 'font_checks': [], 'panels': [], 'labels': [], 'errors': []}
    errors = result['errors']

    def require(condition, message):
        if not condition:
            errors.append(message)

    def find(page, phrase):
        pattern = r'\s*'.join(re.escape(word) for word in phrase.split())
        hits = page.search(pattern)
        require(len(hits) == 1, f'{phrase}: expected one match on page {page.page_number}, got {len(hits)}')
        return hits[0] if len(hits) == 1 else None

    def font(hit, name, size):
        if hit is None:
            return
        sizes = sorted({round(c['size'] / TEX_PT_TO_BP, 4) for c in hit['chars']})
        result['font_checks'].append({'name': name, 'expected_tex_pt': size, 'actual_tex_pt': sizes})
        require(all(abs(s-size) < .04 for s in sizes), f'{name}: expected {size}pt, got {sizes}')

    with pdfplumber.open(path) as pdf:
        result['pages'] = len(pdf.pages)
        require(len(pdf.pages) == 5, f'Fixture should have five pages, got {len(pdf.pages)}')
        if len(pdf.pages) != 5:
            return result
        normal = 'Ordinary figure control' if english else '普通单图对照'
        long = 'Long panel descriptions and pagination' if english else '长分图题与分页测试'
        font(find(pdf.pages[0], 'BodyBefore'), 'body-before', 12)
        font(find(pdf.pages[0], 'BodyAfter'), 'body-after-ordinary', 12)
        font(find(pdf.pages[0], normal), 'ordinary-caption', 10.5)
        font(find(pdf.pages[1], 'GuideAfter'), 'body-after-subfigures', 12)
        cases = [
            (2, '并排子图示例', ['第一张图', '第二张图']),
            (4, long, ['Left panel shows', 'Middle panel shows', 'Right panel shows'] if english
             else ['左侧子图展示', '中间子图展示', '右侧子图展示']),
        ]
        for number, title, descriptions in cases:
            page = pdf.pages[number-1]
            main = find(page, title)
            font(main, title, 10.5)
            images = sorted(page.images, key=lambda image: image['x0'])
            require(len(images) == len(descriptions), f'Page {number}: wrong number of panel images')
            if main is None or len(images) != len(descriptions):
                continue
            for i, (img, description) in enumerate(zip(images, descriptions)):
                label = '(' + chr(ord('a')+i) + ')'
                hits = [h for h in page.search(re.escape(label))
                        if img['bottom'] <= h['top'] < main['top']-1]
                require(len(hits) == 1, f'Page {number}: expected one image label {label}')
                if len(hits) == 1:
                    hit = hits[0]
                    font(hit, f'page-{number}-{label}', 10.5)
                    offset = (hit['x0']+hit['x1']-img['x0']-img['x1']) / 2
                    require(abs(offset) < .5, f'Page {number}: {label} not centered under its image ({offset:.2f}bp)')
                    result['panels'].append({'page': number, 'label': label, 'center_offset_bp': round(offset, 4)})
                detail = find(page, description)
                font(detail, description, 10.5)
                if detail:
                    # Compare reading order by baseline and x, allowing continuation on the same line.
                    same_line = abs(detail['chars'][0]['matrix'][5]-main['chars'][0]['matrix'][5]) < 2
                    follows = detail['top'] > main['top']+2 or (same_line and detail['x0'] >= main['x1'])
                    require(follows, f'Page {number}: {description} must follow the main caption')
            if number == 4:
                ending = 'natural wrapping.' if english else '顺序及自然换行。'
                # Content order preserves phrases across a line break inside a narrow panel;
                # page-wide visual extraction can interleave neighboring columns.
                content = ''.join(c['text'] for c in page.chars if c['text'].strip())
                # TeX may insert a discretionary hyphen when wrapping a narrow caption.
                require(re.sub(r'[\s-]+', '', ending) in content.replace('-', ''),
                        'Long caption must finish on the figure page')

        # Confirm visible reference text, not merely the existence of labels in auxiliary files.
        for page_index, figure, letters in ((1, '1-2', 'ab'), (2, '1-3', 'abc')):
            text = re.sub(r'\s+', '', pdf.pages[page_index].extract_text())
            for letter in letters:
                require(f'{figure}({letter})' in text, f'Missing visible reference {figure}({letter})')
        lof_text = re.sub(r'\s+', '', pdf.pages[4].extract_text())
        for title in (normal, '并排子图示例', long):
            require(re.sub(r'\s+', '', title) in lof_text, f'Missing figure-list title {title}')
        require(not any(s in lof_text for s in ('第一张图', '第二张图', '左侧子图', 'Leftpanelshows')),
                'Figure list should contain short main titles without panel descriptions')

    reader = PdfReader(path)
    destinations = reader.named_destinations
    label_map = {}
    for line in path.with_suffix('.aux').read_text(encoding='utf-8').splitlines():
        if line.startswith('\\newlabel{'):
            outer = groups(line[len('\\newlabel'):])
            if len(outer) == 2:
                label_map[outer[0]] = groups(outer[1])
    expected = {'f04:ordinary': ('1-1', 1), 'fig:guide-pair': ('1-2', 2), 'f04:long': ('1-3', 4)}
    for prefix, parent, page, parts in [('fig:guide', '1-2', 2, ['left', 'right']),
                                      ('f04:long', '1-3', 4, ['left', 'middle', 'right'])]:
        for i, part in enumerate(parts):
            key = f'{prefix}-{part}'
            letter = chr(ord('a')+i)
            expected[key] = (parent+letter, page)
            expected['sub@'+key] = (letter, page)
    for key, (value, page) in expected.items():
        actual = label_map.get(key)
        require(actual is not None and len(actual) >= 4, f'Missing label {key}')
        if actual is None or len(actual) < 4:
            continue
        require(actual[:2] == [value, str(page)], f'{key}: expected {value} on page {page}, got {actual[:2]}')
        destination = destinations.get(actual[3])
        require(destination is not None, f'{key}: missing PDF destination')
        if destination is not None:
            require(reader.get_destination_page_number(destination)+1 == page, f'{key}: wrong destination page')
        result['labels'].append({'key': key, 'value': actual[0], 'page': actual[1], 'destination': actual[3]})

    link_counts = {}
    for number, page in enumerate(reader.pages, 1):
        links = 0
        for ref in page.get('/Annots', []):
            obj = ref.get_object()
            action = obj.get('/A', {})
            target = action.get('/D') if action.get('/S') == '/GoTo' else obj.get('/Dest')
            if isinstance(target, str):
                links += 1
                destination = destinations.get(target)
                require(destination is not None, f'Page {number}: missing link target {target}')
                if number in (2, 3) and destination is not None:
                    expected_page = 2 if number == 2 else 4
                    require(reader.get_destination_page_number(destination)+1 == expected_page,
                            f'Page {number}: figure reference jumps to the wrong page')
        link_counts[number] = links
    require(link_counts.get(2, 0) >= 8 and link_counts.get(3, 0) >= 6 and link_counts.get(5, 0) == 3,
            f'Expected figure/subfigure links and three figure-list links, got {link_counts}')
    result['links_per_page'] = link_counts
    lof = path.with_suffix('.lof').read_text(encoding='utf-8')
    require(len(re.findall(r'\\contentsline\s*\{figure\}', lof)) == 3, 'Expected exactly three figure-list entries')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--english', action='store_true')
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    result = inspect(args.pdf, args.english)
    (args.json or args.pdf.with_suffix('.subfigures.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    if result['errors']:
        print('\n'.join(result['errors']))
        raise SystemExit(1)
    print(f'PASS: {args.pdf.name}, {len(result["font_checks"])} font checks, '
          f'{len(result["panels"])} panel placements, {len(result["labels"])} labels and PDF links verified.')
