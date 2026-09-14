"""Check actual math glyphs and text-font isolation in the compiled PDF."""
from __future__ import annotations

import argparse
from pathlib import Path

import pdfplumber


def inspect(path: Path) -> None:
    log = path.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
    for diagnostic in ('Missing character:', 'Overfull', 'Undefined control sequence'):
        if diagnostic in log:
            raise AssertionError(f'{path.name}: {diagnostic}')
    with pdfplumber.open(path) as pdf:
        if len(pdf.pages) != 1:
            raise AssertionError('Expected one compact math test page')
        chars = pdf.pages[0].chars
    # Computer Modern maps these two glyphs to their historical Unicode equivalents.
    equivalents = str.maketrans({'∆': 'Δ', 'Ω': 'Ω'})
    bold_greek = ''.join(c['text'].translate(equivalents) for c in chars
                         if c['fontname'].split('+')[-1].startswith('CMBX'))
    for letter in 'ΓΔΘΛΞΠΣΥΦΨΩ':
        if bold_greek.count(letter) < 2:
            raise AssertionError(f'Missing bold Greek glyph: {letter}')
    for marker, expected_font in [('TextControl', 'TimesNewRomanPSMT'),
                                  ('BoldControl', 'TimesNewRomanPS-BoldMT')]:
        text = ''.join(c['text'] for c in chars
                       if c['fontname'].split('+')[-1] == expected_font)
        if marker not in text:
            raise AssertionError(f'Text font changed for {marker}')
    fonts = {c['fontname'].split('+')[-1] for c in chars}
    for family in ('CMR', 'CMMI', 'CMBX', 'CMSS', 'CMTT'):
        if not any(font.startswith(family) for font in fonts):
            raise AssertionError(f'Missing default math family: {family}')
    print(f'PASS: {path.name}, Greek glyphs, math families and text fonts verified.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    inspect(parser.parse_args().pdf)
