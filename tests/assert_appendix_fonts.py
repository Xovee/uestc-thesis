"""Check actual appendix PDF text sizes and font restoration across boundaries."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

TEX_PT_TO_BP = 72 / 72.27
PROBES = (
    ('main-body', '正文对照段落', 'The main body control confirms', 12),
    ('appendix-title', '附录正文与标题', 'Appendix text and headings', 15),
    ('appendix-a', '附录正文甲', 'Appendix body A', 10.5),
    ('section-title', '附录的二级标题', 'Second-level appendix heading', 14),
    ('after-section', '节后正文继续', 'Text after a section keeps', 10.5),
    ('subsection-title', '附录的三级标题', 'Third-level appendix heading', 14),
    ('subsubsection-title', '附录的四级标题', 'Fourth-level appendix heading', 12),
    ('after-subsubsection', '四级标题后的正文', 'Text after the fourth-level heading', 10.5),
    ('theorem', '附录定理正文', 'Appendix theorem text', 10.5),
    ('proof', '证明文字继承', 'The proof inherits', 10.5),
    ('footnote', '附录脚注保持', 'The appendix footnote keeps', 9),
    ('main-equation', 'MainControl', 'MainControl', 12),
    ('appendix-equation', 'AppendixControl', 'AppendixControl', 12),
    ('after-equation', '公式后正文自动', 'Text after the equation automatically', 10.5),
    ('appendix-b', '附录正文乙', 'Appendix body B', 10.5),
    ('figure-caption', '附录图题检查', 'Appendix figure caption', 10.5),
    ('table-caption', '附录表题检查', 'Appendix table caption', 10.5),
    ('after-table', '表后正文保持', 'Text after the table keeps', 10.5),
    ('after-displays', '所有公式之后的正文', 'Text after all display environments', 10.5),
    ('achievements-body', '成果页对照段落', 'The achievements control paragraph', 12),
    ('achievements-list', '成果列表对照条目', 'The achievement list control', 10.5),
    ('after-achievements-list', '列表后的正文', 'Text after the list keeps', 12),
    ('achievements-equation', 'FinalControl', 'FinalControl', 12),
)
DISPLAY_PROBES = (
    'EquationStar', 'AlignControl', 'AlignStar', 'AlignatControl', 'AlignatStar',
    'FlalignControl', 'FlalignStar', 'GatherControl', 'GatherStar',
    'MultlineControl', 'MultlineStar', 'DisplayControl', 'BracketControl',
)
BODY_LOG_PROBES = (
    'appendix-a', 'after-section', 'after-subsection', 'after-subsubsection',
    'appendix-theorem', 'appendix-proof', 'after-equation', 'appendix-b',
    'after-figure', 'after-table', 'after-all-displays',
)


def inspect(path: Path, english: bool = False) -> dict:
    result = {'pdf': str(path), 'language': 'english' if english else 'chinese',
              'pdf_probes': [], 'body_spacing': [], 'errors': []}
    errors = result['errors']
    with pdfplumber.open(path) as pdf:
        pages = []
        for number, page in enumerate(pdf.pages, 1):
            # Exclude running headers and page numbers, but retain footnotes.
            chars = [c for c in page.chars if 95 < c['top'] and c['bottom'] < 770
                     and c['text'].strip()]
            text = ''.join(c['text'] for c in chars)
            assert all(len(c['text']) == 1 for c in chars)
            pages.append((number, text, chars))

        probes = [(name, en if english else cn, size) for name, cn, en, size in PROBES]
        probes.extend((name, name, 12) for name in DISPLAY_PROBES)
        equation_page = None
        for name, phrase, size in probes:
            target = re.sub(r'\s+', '', phrase)
            hits = []
            for number, text, chars in pages:
                start = text.find(target)
                if start >= 0:
                    hits.append((number, chars[start:start + len(target)]))
            if len(hits) != 1:
                errors.append(f'{name}: expected one PDF match, found {len(hits)}')
                continue
            number, chars = hits[0]
            actual = sorted({round(c['size'], 4) for c in chars})
            result['pdf_probes'].append({'name': name, 'page': number,
                                         'expected_tex_pt': size, 'actual_bp': actual})
            if any(abs(c['size'] - size * TEX_PT_TO_BP) > .03 for c in chars):
                errors.append(f'{name}: expected {size} TeX pt, got {actual} PDF bp')
            if name == 'appendix-equation':
                equation_page = number

        if equation_page is not None:
            number, text, chars = pages[equation_page - 1]
            start = text.find('(A-1)')
            if start < 0:
                errors.append('Appendix equation number (A-1) was not found beside the equation')
            elif any(abs(c['size'] - 12 * TEX_PT_TO_BP) > .03 for c in chars[start:start + 5]):
                errors.append('Appendix equation number does not use 12pt')

    log = path.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
    values = {}
    for name, size, baseline, indent in re.findall(r'F02FONT\|([^|\s]+)\|([\d.]+)\|([\d.]+)\|([\d.]+)', log):
        values[name] = tuple(map(float, (size, baseline, indent)))
    # Actual PDF glyphs above establish the font sizes; these TeX records verify
    # paragraph spacing and restoration at boundaries that may have no text.
    for name in BODY_LOG_PROBES:
        actual = values.get(name)
        result['body_spacing'].append({'name': name, 'size_baseline_indent_pt': actual})
        if actual != (10.5, 20, 21):
            errors.append(f'{name}: expected 10.5pt text, 20pt baseline, 21pt indent; got {actual}')
    for name in ('main-body', 'achievements-body', 'after-achievements-list'):
        if values.get(name) != (12, 20, 24):
            errors.append(f'{name}: original body size/spacing not preserved: {values.get(name)}')

    reader = PdfReader(path)
    destinations = reader.named_destinations
    for page in reader.pages:
        for ref in page.get('/Annots', []):
            obj = ref.get_object()
            action = obj.get('/A', {})
            target = action.get('/D') if action.get('/S') == '/GoTo' else obj.get('/Dest')
            if isinstance(target, str) and target not in destinations:
                errors.append(f'Missing link destination: {target}')
    result['pages'] = len(reader.pages)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--english', action='store_true')
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    result = inspect(args.pdf, args.english)
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    if result['errors']:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(f'PASS: {args.pdf.name}, {len(result["pdf_probes"])} PDF font probes, appendix spacing and restoration verified.')
