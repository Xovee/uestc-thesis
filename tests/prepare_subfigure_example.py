"""Extract the actual guide's subfigure example for the PDF regression fixture."""
from __future__ import annotations

import argparse
from pathlib import Path
import re


def extract(guide: Path, output: Path) -> None:
    text = guide.read_text(encoding='utf-8')
    sections = text.split('#### 并排子图\n')
    if len(sections) != 2:
        raise ValueError('GUIDE.md must contain exactly one 并排子图 section')
    section = re.split(r'\n#{1,4} ', sections[1], maxsplit=1)[0]
    blocks = re.findall(r'```latex\s*\n(.*?)\n```', section, re.S)
    if len(blocks) != 1:
        raise ValueError('The subfigure section must contain exactly one LaTeX example')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(blocks[0] + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('guide', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    extract(args.guide, args.output)
