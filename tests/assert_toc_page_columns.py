"""Check visible ToC page-number geometry, not just extracted title strings."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import pdfplumber
from pypdf import PdfReader

def inspect(path: Path, pages: list[int], expected_entries: int | None = None) -> dict:
    result={'pdf':str(path),'pages':pages,'entries':[],'errors':[]}
    with pdfplumber.open(path) as pdf:
        for number in pages:
            page=pdf.pages[number-1]
            right=page.width-30*72/25.4
            # Font ascent varies between Chinese and Latin glyphs. Group by the
            # PDF text baseline, so a Chinese title and its Latin page number
            # cannot silently become separate extracted lines.
            rows=[]
            for char in sorted(page.chars,key=lambda c:-c['matrix'][5]):
                if char['top']<140 or char['bottom']>755 or not char['text'].strip() or char['text'] in '.·⋅':
                    continue
                baseline=char['matrix'][5]
                if not rows or abs(rows[-1][0]-baseline)>.6:
                    rows.append((baseline,[]))
                rows[-1][1].append(char)
            for baseline, row in rows:
                chars=sorted(row,key=lambda c:c['x0'])
                if not chars or chars[-1]['x1']<right-2:
                    continue
                end=len(chars)
                start=end
                while start and re.fullmatch(r'[0-9IVXLCDM]',chars[start-1]['text']):
                    if start<end and chars[start]['x0']-chars[start-1]['x1']>.8:
                        break
                    start-=1
                if start==end:
                    continue
                numchars=chars[start:]
                body=[c for c in chars[:start] if c['text'].strip() and c['text'] not in '.·⋅']
                if not body:
                    continue
                gap=numchars[0]['x0']-max(c['x1'] for c in body)
                line_text=''.join(c['text'] for c in chars)
                entry={'page':number,'text':line_text,'number':''.join(c['text'] for c in numchars),'gap_bp':gap,'right_bp':numchars[-1]['x1']}
                # The leaders are raised by 1pt. Measure their visible edge
                # separately from the title baseline and the page-number box.
                dots=[c for c in page.chars if c['text'] in '.·⋅'
                      and abs(c['matrix'][5]-baseline)<1.5
                      and max(b['x1'] for b in body)<c['x0']<numchars[0]['x0']]
                if dots:
                    leader_gap=numchars[0]['x0']-max(c['x1'] for c in dots)
                    entry['leader_gap_bp']=leader_gap
                    if not 1.8<=leader_gap<=6.5:
                        result['errors'].append(f'Page {number}: leader/page gap {leader_gap:.3f}bp: {line_text}')
                elif gap>20:
                    result['errors'].append(f'Page {number}: no leaders in available title/page space: {line_text}')
                result['entries'].append(entry)
                if gap<1.8:
                    result['errors'].append(f'Page {number}: title/page gap {gap:.3f}bp: {line_text}')
                if abs(numchars[-1]['x1']-right)>.3:
                    result['errors'].append(f'Page {number}: page number is not aligned with the text right edge')
                for rect in page.rects:
                    if not rect.get('fill') or rect.get('non_stroking_color') not in (1,1.0,(1,),(1,1,1),(1.0,1.0,1.0)):
                        continue
                    for char in body:
                        if min(rect['x1'],char['x1'])-max(rect['x0'],char['x0'])>.1 and min(rect['bottom'],char['bottom'])-max(rect['top'],char['top'])>.1:
                            result['errors'].append(f'Page {number}: white rectangle covers title character {char["text"]!r}')
    if not result['entries']:
        result['errors'].append('No right-aligned page-number entries found')
    if expected_entries is not None and len(result['entries'])!=expected_entries:
        result['errors'].append(f'Expected {expected_entries} entries, found {len(result["entries"])}')
    reader=PdfReader(path)
    names=reader.named_destinations
    for page in reader.pages:
        for ref in page.get('/Annots',[]):
            obj=ref.get_object();action=obj.get('/A',{})
            target=obj.get('/Dest')
            if action.get('/S')=='/GoTo': target=action.get('/D')
            if isinstance(target,str) and target not in names:
                result['errors'].append(f'Missing link destination: {target}')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path)
    parser.add_argument('--pages',type=int,nargs='+',required=True)
    parser.add_argument('--json',type=Path)
    parser.add_argument('--entries',type=int)
    args=parser.parse_args()
    result=inspect(args.pdf,args.pages,args.entries)
    if args.json:args.json.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['errors']))
