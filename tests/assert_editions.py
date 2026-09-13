#!/usr/bin/env python3
"""Check literal edition expectations in both BibTeX output and rendered PDF."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


# Literal expected results also protect normal suffixes and nonnumeric branches.
EXPECTED = {
    'en-1': '', 'en-2': '2nd ed.', 'en-3': '3rd ed.', 'en-4': '4th ed.',
    'en-10': '10th ed.', 'en-11': '11th ed.', 'en-12': '12th ed.',
    'en-13': '13th ed.', 'en-14': '14th ed.', 'en-20': '20th ed.',
    'en-21': '21st ed.', 'en-22': '22nd ed.', 'en-23': '23rd ed.',
    'en-24': '24th ed.', 'en-100': '100th ed.', 'en-101': '101st ed.',
    'en-102': '102nd ed.', 'en-103': '103rd ed.', 'en-110': '110th ed.',
    'en-111': '111th ed.', 'en-112': '112th ed.', 'en-113': '113th ed.',
    'en-114': '114th ed.', 'en-121': '121st ed.', 'en-122': '122nd ed.',
    'en-123': '123rd ed.', 'en-211': '211th ed.', 'en-212': '212th ed.',
    'en-213': '213th ed.', 'zh-1': '', 'zh-2': '2 版', 'zh-11': '11 版',
    'zh-112': '112 版', 'en-empty': '', 'zh-empty': '',
    'en-revised': 'Rev. ed.', 'en-revised-edition': 'Rev. ed.',
    'en-text': 'Second ed.', 'zh-text': '修订版',
    'auto-en-11': '11th ed.', 'auto-zh-11': '11 版',
    'incollection-12': '12th ed.',
}


def compact(text: str) -> str:
    return re.sub(r'\s+', '', text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--json', type=Path, help='Optional detailed verification record')
    args = parser.parse_args()
    bbl = args.pdf.with_suffix('.bbl').read_text(encoding='utf-8')
    parts = re.split(r'\\bibitem\[[\s\S]*?\]\{([^{}]+)\}\s*', bbl)
    keys = parts[1::2]
    entries = dict(zip(keys, parts[2::2]))
    reader = PdfReader(args.pdf)
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    pdf_parts = re.split(r'\[(\d+)\]\s*', text)
    pdf_numbers = list(map(int, pdf_parts[1::2]))
    pdf_entries = dict(zip(pdf_numbers, pdf_parts[2::2]))
    failures = []
    checks = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    check(keys == list(EXPECTED), 'BBL records or citation order differ from the fixture')
    check(pdf_numbers == list(range(1, len(EXPECTED) + 1)),
          'PDF record labels are missing, duplicated, or out of order')
    for number, (key, expected) in enumerate(EXPECTED.items(), 1):
        for source, entry in [('BBL', entries.get(key, '')), ('PDF', pdf_entries.get(number, ''))]:
            # Check the edition segment itself, after the title/container and
            # immediately before the publisher. This catches extra/wrong suffixes.
            normalized = compact(entry.replace(r'\newblock', '').replace(r'\allowbreak', ''))
            match = re.search(r'(?:\[M\]\.|Collectedexamples\.)(.*?)Chengdu:', normalized)
            actual = match.group(1) if match else None
            wanted = compact(expected)
            if wanted and not wanted.endswith('.'):
                wanted += '.'
            passed = actual == wanted
            check(passed, f'{source} {key}: expected edition {wanted!r}, got {actual!r}')
            checks.append({'source': source, 'key': key, 'expected': wanted,
                           'actual': actual, 'passed': passed})
    result = {'pdf': str(args.pdf), 'pages': len(reader.pages), 'records': len(EXPECTED),
              'checks': checks, 'failures': failures}
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for failure in failures:
        print('FAIL: ' + failure)
    if not failures:
        print(f'PASS: {len(EXPECTED)} edition records verified in BBL and PDF ({len(reader.pages)} pages).')
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
