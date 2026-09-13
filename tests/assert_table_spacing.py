"""Check actual PDF table baselines, text sizes, and surrounding paragraph controls."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber

TEX_PT_TO_BP = 72 / 72.27
TOLERANCE_PT = .04
# Consecutive markers are on consecutive lines of one cell or ordinary short rows.
GROUPS = (
    (('POne', 'PTwo', 'PThree'), 13.6, 10.5),
    (('XOne', 'XTwo', 'XThree'), 13.6, 10.5),
    (('MOne', 'MTwo', 'MThree'), 13.6, 10.5),
    (('BOne', 'BTwo', 'BThree'), 13.6, 10.5),
    (('COne', 'CTwo', 'CThree'), 13.6, 10.5),
    (('InnerOne', 'InnerTwo', 'InnerThree'), 13.6, 10.5),
    (('OuterTwo', 'OuterThree'), 13.6, 10.5),
    (('StretchOne', 'StretchTwo', 'StretchThree'), 13.6, 10.5),
    (('StarOne', 'StarTwo', 'StarThree'), 13.6, 10.5),
    (('TallTwo', 'TallThree'), 13.6, 10.5),
    (('NOne', 'NTwo', 'NThree'), 20, 12),
    (('PShortOne', 'PShortTwo'), 17, 10.5),
    (('XShortOne', 'XShortTwo'), 17, 10.5),
    (('CShortOne', 'CShortTwo'), 26, 10.5),
    (('InnerShortOne', 'InnerShortTwo'), 17, 10.5),
    (('StretchShortOne', 'StretchShortTwo'), 17, 10.5),
    (('StarShortOne', 'StarShortTwo'), 17, 10.5),
    (('NShortOne', 'NShortTwo'), 17, 12),
    (('BodyBeforeOne', 'BodyBeforeTwo'), 20, 12),
    (('BodyAfterOne', 'BodyAfterTwo'), 20, 12),
    (('BodyFinalOne', 'BodyFinalTwo'), 20, 12),
    (('DefaultAfterOne', 'DefaultAfterTwo'), 20, 12),
    (('EndOne', 'EndTwo'), 20, 12),
    (('StretchBeforeOne', 'StretchBeforeTwo'), 30, 12),
    (('StretchAfterOne', 'StretchAfterTwo'), 30, 12),
    (('NoteOne', 'NoteTwo'), 20, 10.5),
    (('MSingle', 'LSingle'), 0, 10.5),
)
EXTRA_SIZES = (
    ('TallOne', 10.5), ('OuterOne', 10.5),
    ('Fixed width paragraph cells', 10.5),
    ('Flexible width paragraph cells', 10.5),
    ('中文第一行', 10.5), ('中文第三行', 10.5),
    ('自适应列第一行', 10.5),
)


def inspect(path: Path) -> dict:
    result = {'pdf': str(path), 'markers': {}, 'gaps': [], 'errors': []}
    errors = result['errors']
    expected = {name: size for names, gap, size in GROUPS for name in names}
    expected.update(EXTRA_SIZES)
    markers = result['markers']
    with pdfplumber.open(path) as pdf:
        result['pages'] = len(pdf.pages)
        for phrase, expected_size in expected.items():
            # PDF extraction may omit narrow interword spaces in a caption.
            pattern = r'\s*'.join(re.escape(word) for word in phrase.split())
            hits = [(number, match) for number, page in enumerate(pdf.pages, 1)
                    for match in page.search(pattern)]
            if len(hits) != 1:
                errors.append(f'{phrase}: expected one PDF match, found {len(hits)}')
                continue
            number, hit = hits[0]
            # Use the text matrix, not the glyph top: fonts/bold can have different ascenders.
            chars = hit['chars']
            actual_sizes = sorted({round(c['size'] / TEX_PT_TO_BP, 4) for c in chars})
            markers[phrase] = {'page': number, 'baseline_bp': chars[0]['matrix'][5],
                               'sizes_tex_pt': actual_sizes, 'expected_size_tex_pt': expected_size}
            if any(abs(size - expected_size) > TOLERANCE_PT for size in actual_sizes):
                errors.append(f'{phrase}: expected {expected_size}pt text, got {actual_sizes}')
        for names, expected_gap, size in GROUPS:
            for first, second in zip(names, names[1:]):
                check_gap(first, second, expected_gap, markers, result)
        # Tall content must be able to grow the spacing instead of colliding with the next line.
        check_gap('TallOne', 'TallTwo', 13.6, markers, result, minimum=True)
    return result


def check_gap(first: str, second: str, expected: float, markers: dict,
              result: dict, minimum: bool = False) -> None:
    if first not in markers or second not in markers:
        return  # Missing markers already failed; never silently count them as checked.
    a, b = markers[first], markers[second]
    if a['page'] != b['page']:
        result['errors'].append(f'{first}/{second}: expected the same page')
        return
    gap = (a['baseline_bp'] - b['baseline_bp']) / TEX_PT_TO_BP
    result['gaps'].append({'first': first, 'second': second, 'actual_tex_pt': round(gap, 4),
                           'expected_tex_pt': expected, 'minimum_only': minimum})
    failed = gap < expected - TOLERANCE_PT if minimum else abs(gap - expected) > TOLERANCE_PT
    if failed:
        relation = 'at least' if minimum else 'exactly'
        result['errors'].append(f'{first}/{second}: expected {relation} {expected}pt, got {gap:.4f}pt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    result = inspect(args.pdf)
    output = args.json or args.pdf.with_suffix('.table-spacing.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if result['errors']:
        print('\n'.join(result['errors']))
        raise SystemExit(1)
    print(f'PASS: {args.pdf.name}, {len(result["gaps"])} PDF spacing checks and '
          f'{len(result["markers"])} text size checks.')
