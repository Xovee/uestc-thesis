"""Release packaging tests with real Markdown and synthetic thesis/font data."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import posixpath
import re
import tempfile
import sys
import unittest
from unittest import mock
from urllib.parse import unquote, urlsplit
import zipfile

from pypdf import PdfWriter


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "package_release.py"
SPEC = importlib.util.spec_from_file_location("package_release", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
PACKAGE = importlib.util.module_from_spec(SPEC)
with mock.patch.object(sys, 'path', [str(SCRIPT.parent), *sys.path]):
    SPEC.loader.exec_module(PACKAGE)


def broken_archive_markdown_links(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    """Check local file targets of inline links and reference definitions in ZIP Markdown.

    Network URLs and same-page anchors do not refer to archive members. Code fences
    and inline code are examples, not navigation. Fragment contents are not checked.
    """
    members = set(archive.namelist())
    broken = []
    for name in sorted(members):
        if not name.lower().endswith('.md'):
            continue
        text = archive.read(name).decode('utf-8')
        text = re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text)
        text = re.sub(r'(`+)[^`\n]*?\1', '', text)
        targets = re.findall(r'\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+"[^"]*")?\s*\)', text)
        targets += re.findall(r'(?m)^\s*\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)', text)
        for target in targets:
            url = urlsplit(target.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
            if resolved not in members and not any(member.startswith(resolved + '/') for member in members):
                broken.append((name, target))
    return broken


class PackageReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="uestc-package-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.defaults_patch = mock.patch.multiple(
            PACKAGE,
            ROOT=self.root,
            DEFAULT_OUTPUT=self.root / PACKAGE.DEFAULT_OUTPUT.relative_to(PACKAGE.ROOT),
            DEFAULT_SOURCE_ONLY_OUTPUT=(
                self.root / PACKAGE.DEFAULT_SOURCE_ONLY_OUTPUT.relative_to(PACKAGE.ROOT)
            ),
            APPROVED_ASSET_HASHES={},
        )
        self.defaults_patch.start()
        self.addCleanup(self.defaults_patch.stop)

        for name in set(PACKAGE.ROOT_FILES) | set(PACKAGE.ENGLISH_SOURCES.values()):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"packaging fixture\n")
        (self.root / 'cover.pdf').write_bytes(self.pdf_bytes(3))
        (self.root / 'declaration.pdf').write_bytes(self.pdf_bytes(1))
        self.guide = self.root / "GUIDE.md"
        self.set_guide("draft")
        self.example = self.root / "example.pdf"
        self.example.write_bytes(self.pdf_bytes(1, example=True))
        self.build_patch = mock.patch.object(PACKAGE, 'build_example', side_effect=self.fake_build)
        self.mock_build = self.build_patch.start()
        self.addCleanup(self.build_patch.stop)
        (self.root / "guide.tex").write_text("historical guide", encoding="utf-8")
        (self.root / "THIRD_PARTY.md").write_text("withheld pending revision", encoding="utf-8")
        (self.root / "uestc-thesis-guide.pdf").write_bytes(b"historical preview")

    @staticmethod
    def pdf_bytes(pages, example=False, language="chinese"):
        writer = PdfWriter()
        for _ in range(pages):
            writer.add_blank_page(595.28, 841.89)
        writer.add_metadata({'/Producer': ''})
        if example:
            writer.add_metadata({'/Title': '论文题目' if language == 'chinese' else 'English Thesis Title',
                                 '/Author': '作者姓名' if language == 'chinese' else 'Author Name',
                                 '/Creator': 'UESTC Thesis LaTeX Template by Xovee Xu'})
        output = io.BytesIO()
        writer.write(output)
        return output.getvalue()

    def fake_build(self, stage):
        english = b'[master,english]' in (stage / 'main.tex').read_bytes()
        entry = 'main-english.tex' if english else 'main.tex'
        expected = PACKAGE.package_payload({'main.tex': (self.root / entry).read_bytes()}, 'english' if english else 'chinese')
        self.assertEqual((stage / 'main.tex').read_bytes(), expected['main.tex'])
        target = stage / 'build/uestc-thesis-example.pdf'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.pdf_bytes(1, example=True, language='english') if english else self.example.read_bytes())
        return {'entry': 'main.tex', 'fresh_build': True, 'latexmk_version': 'test fixture'}

    def approve(self, path):
        report = json.loads(path.read_text(encoding='utf-8'))
        report['review'] = {key: True for key in PACKAGE.REVIEW_FIELDS}
        path.write_text(json.dumps(report, ensure_ascii=False), encoding='utf-8')

    def prepare_formal(self):
        self.set_guide('ready')
        result, text = self.run_main()
        self.assertEqual(result, 0, text)
        return self.root / 'dist/uestc-thesis-xovee-chinese-candidate.review.json'

    def set_guide(self, state: str) -> None:
        self.guide.write_text(
            f"# Test guide\n\n<!-- guide-status: {state} -->\n\nTest content.\n",
            encoding="utf-8",
        )

    def run_main(self, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with mock.patch("sys.argv", [str(SCRIPT), *args]):
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = PACKAGE.main()
        return result, output.getvalue()

    def test_source_package_includes_draft_markdown_not_guide_pdf(self) -> None:
        output = self.root / "source.zip"
        result, text = self.run_main("--source-only", "--output", str(output))
        self.assertEqual(result, 0, text)
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            self.assertIn("uestc-thesis-xovee-chinese/GUIDE.md", names)
            self.assertEqual(
                archive.read("uestc-thesis-xovee-chinese/GUIDE.md"), self.guide.read_bytes()
            )
            self.assertNotIn("uestc-thesis-xovee-chinese/guide.tex", names)
            self.assertNotIn("uestc-thesis-xovee-chinese/THIRD_PARTY.md", names)
            self.assertNotIn("uestc-thesis-xovee-chinese/uestc-thesis-guide.pdf", names)
            self.assertNotIn("uestc-thesis-xovee-chinese/uestc-thesis-example.pdf", names)

    def test_default_formal_archive_name_and_root(self) -> None:
        report = self.prepare_formal()
        self.assertFalse((self.root / 'dist/uestc-thesis-xovee-chinese.zip').exists())
        self.approve(report)
        result, text = self.run_main('--reviewed', str(report))
        self.assertEqual(result, 0, text)
        output = self.root / "dist" / "uestc-thesis-xovee-chinese.zip"
        self.assertTrue(output.is_file())
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(
                {Path(name).parts[0] for name in archive.namelist()},
                {"uestc-thesis-xovee-chinese"},
            )

    def test_only_approved_vscode_files_are_packaged(self) -> None:
        private = self.root / ".vscode" / "private.json"
        private.write_text("private fixture", encoding="utf-8")
        output = self.root / "source.zip"
        result, text = self.run_main("--source-only", "--output", str(output))
        self.assertEqual(result, 0, text)
        approved = {".vscode/settings.json", ".vscode/extensions.json"}
        with zipfile.ZipFile(output) as archive:
            names = {
                name.removeprefix("uestc-thesis-xovee-chinese/")
                for name in archive.namelist()
                if "/.vscode/" in name
            }
            self.assertEqual(names, approved)
            for name in approved:
                self.assertEqual(
                    archive.read(f"uestc-thesis-xovee-chinese/{name}"),
                    (self.root / name).read_bytes(),
                )

    def test_default_source_archive_keeps_preview_suffix(self) -> None:
        result, text = self.run_main("--source-only")
        self.assertEqual(result, 0, text)
        self.assertTrue(
            (self.root / "dist" / "uestc-thesis-xovee-chinese-source-preview.zip").is_file()
        )
        self.assertFalse((self.root / "dist" / "uestc-thesis-xovee-chinese.zip").exists())

    def test_formal_package_rejects_draft_guide(self) -> None:
        output = self.root / "formal.zip"
        result, text = self.run_main(
            "--output", str(output)
        )
        self.assertEqual(result, 1)
        self.assertIn("GUIDE.md is not approved", text)
        self.assertFalse(output.exists())

    def test_formal_package_accepts_ready_markdown_without_guide_pdf(self) -> None:
        self.set_guide("ready")
        (self.root / "uestc-thesis-guide.pdf").unlink()
        output = self.root / "formal.zip"
        result, text = self.run_main(
            "--output", str(output)
        )
        self.assertEqual(result, 0, text)
        self.assertFalse(output.exists())
        report = output.with_name('formal-candidate.review.json')
        self.approve(report)
        result, text = self.run_main('--reviewed', str(report), '--output', str(output))
        self.assertEqual(result, 0, text)
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            self.assertIn("uestc-thesis-xovee-chinese/GUIDE.md", names)
            self.assertIn("uestc-thesis-xovee-chinese/uestc-thesis-example.pdf", names)
            self.assertFalse(any("guide.pdf" in name for name in names))

    def test_missing_markdown_blocks_source_package(self) -> None:
        self.guide.unlink()
        output = self.root / "source.zip"
        result, text = self.run_main("--source-only", "--output", str(output))
        self.assertEqual(result, 1)
        self.assertIn("GUIDE.md", text)
        self.assertFalse(output.exists())

    def test_failed_fresh_build_blocks_candidate(self) -> None:
        self.set_guide("ready")
        output = self.root / "formal.zip"
        self.mock_build.side_effect = ValueError('Fresh example build failed')
        result, text = self.run_main('--output', str(output))
        self.assertEqual(result, 1)
        self.assertIn('Fresh example build failed', text)
        self.assertFalse(output.exists())
        self.assertFalse(output.with_name('formal-candidate.zip').exists())

    def test_ambiguous_or_missing_status_is_not_ready(self) -> None:
        for content in (
            "# No status\n",
            "<!-- guide-status: unknown -->\n",
            "<!-- guide-status: ready -->\n<!-- guide-status: draft -->\n",
        ):
            with self.subTest(content=content):
                self.guide.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "not approved"):
                    PACKAGE.require_ready_guide()

    def test_archive_is_deterministic(self) -> None:
        first, second = self.root / "first.zip", self.root / "second.zip"
        for output in (first, second):
            result, text = self.run_main("--source-only", "--output", str(output))
            self.assertEqual(result, 0, text)
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_suffix_compatible_private_backups_are_excluded(self):
        names = ['chapters/drafts/private-note.tex', 'figures/backups/private-scan.pdf',
                 'figures/private-photo.png', 'chapters/private.md']
        for name in names:
            file = self.root / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(b'private synthetic fixture')
        result, text = self.run_main('--source-only')
        self.assertEqual(result, 0, text)
        archive_path = self.root / 'dist/uestc-thesis-xovee-chinese-source-preview.zip'
        with zipfile.ZipFile(archive_path) as archive:
            self.assertEqual(len(archive.namelist()), 30)
            self.assertFalse(any('private' in name for name in archive.namelist()))
        report = json.loads(archive_path.with_suffix('.review.json').read_text(encoding='utf-8'))
        self.assertTrue(set(names) <= set(report['excluded_files']))

    def test_modified_approved_binary_is_rejected(self):
        with mock.patch.object(PACKAGE, 'APPROVED_ASSET_HASHES', {'cover.pdf': '0' * 64}):
            result, text = self.run_main('--source-only')
        self.assertEqual(result, 1)
        self.assertIn('approved binary asset has changed: cover.pdf', text)

    def test_private_email_in_selected_content_is_rejected(self):
        (self.root / 'chapters/chapter-1.tex').write_text('private.person@example.invalid', encoding='utf-8')
        result, text = self.run_main('--source-only')
        self.assertEqual(result, 1)
        self.assertIn('content checks failed', text)
        self.assertFalse((self.root / 'dist/uestc-thesis-xovee-chinese-source-preview.zip').exists())

    def test_unreviewed_candidate_cannot_be_finalized(self):
        report = self.prepare_formal()
        result, text = self.run_main('--reviewed', str(report))
        self.assertEqual(result, 1)
        self.assertIn('review checks first', text)

    def test_source_change_invalidates_review(self):
        report = self.prepare_formal()
        self.approve(report)
        (self.root / 'chapters/chapter-1.tex').write_text('Updated public example', encoding='utf-8')
        result, text = self.run_main('--reviewed', str(report))
        self.assertEqual(result, 1)
        self.assertIn('Source changed since review', text)

    def test_candidate_change_invalidates_review(self):
        report = self.prepare_formal()
        self.approve(report)
        candidate = self.root / 'dist/uestc-thesis-xovee-chinese-candidate.zip'
        with zipfile.ZipFile(candidate, 'a') as archive:
            archive.writestr('uestc-thesis-xovee-chinese/extra-private.txt', 'fixture')
        result, text = self.run_main('--reviewed', str(report))
        self.assertEqual(result, 1)
        self.assertIn('Candidate archive changed', text)

    def test_preview_change_invalidates_review(self):
        report = self.prepare_formal()
        self.approve(report)
        (self.root / 'dist/uestc-thesis-xovee-chinese-candidate.example.pdf').write_bytes(b'stale preview')
        result, text = self.run_main('--reviewed', str(report))
        self.assertEqual(result, 1)
        self.assertIn('Reviewed PDF preview', text)

    def test_old_example_is_not_used(self):
        old = self.root / 'output/pdf/uestc-thesis-template-preview.pdf'
        old.parent.mkdir(parents=True, exist_ok=True)
        old.write_bytes(b'old example must not be distributed')
        report_path = self.prepare_formal()
        self.mock_build.assert_called_once()
        report = json.loads(report_path.read_text(encoding='utf-8'))
        with zipfile.ZipFile(report_path.parent / report['candidate']) as archive:
            self.assertEqual(archive.read('uestc-thesis-xovee-chinese/uestc-thesis-example.pdf'), self.example.read_bytes())

    def test_source_preview_is_not_a_formal_candidate(self):
        result, text = self.run_main('--source-only')
        self.assertEqual(result, 0, text)
        report = self.root / 'dist/uestc-thesis-xovee-chinese-source-preview.review.json'
        self.approve(report)
        self.set_guide('ready')
        result, text = self.run_main('--reviewed', str(report))
        self.assertEqual(result, 1)
        self.assertIn('formal candidate review record', text)

    def test_output_cannot_replace_source(self):
        before = self.guide.read_bytes()
        result, text = self.run_main('--source-only', '--output', str(self.guide))
        self.assertEqual(result, 1)
        self.assertIn('cannot also be an input', text)
        self.assertEqual(self.guide.read_bytes(), before)

    def test_selected_path_cannot_escape_project(self):
        project = self.root / 'project'
        project.mkdir()
        (self.root / 'private.tex').write_text('synthetic outside fixture', encoding='utf-8')
        with mock.patch.multiple(PACKAGE, ROOT=project, ROOT_FILES=('../private.tex',)):
            with self.assertRaisesRegex(ValueError, 'outside the project'):
                PACKAGE.collect_user_files()

    def test_source_change_during_preparation_is_rejected(self):
        self.set_guide('ready')
        def changing_build(stage):
            result = self.fake_build(stage)
            (self.root / 'chapters/chapter-1.tex').write_text('Concurrent edit', encoding='utf-8')
            return result
        self.mock_build.side_effect = changing_build
        result, text = self.run_main()
        self.assertEqual(result, 1)
        self.assertIn('Source changed during preparation', text)

    def test_build_must_not_rewrite_staged_source(self):
        self.set_guide('ready')
        def changing_build(stage):
            result = self.fake_build(stage)
            (stage / 'main.tex').write_text('Changed by build', encoding='utf-8')
            return result
        self.mock_build.side_effect = changing_build
        result, text = self.run_main()
        self.assertEqual(result, 1)
        self.assertIn('modified a staged source file', text)

    def test_editing_generated_audit_data_invalidates_review(self):
        path = self.prepare_formal()
        self.approve(path)
        report = json.loads(path.read_text(encoding='utf-8'))
        report['audit']['pdfs'][0]['pages'] = 999
        path.write_text(json.dumps(report, ensure_ascii=False), encoding='utf-8')
        result, text = self.run_main('--reviewed', str(path))
        self.assertEqual(result, 1)
        self.assertIn('inspection no longer matches', text)

    def test_user_markdown_links_resolve_inside_actual_archive(self) -> None:
        # Preserve the real public Markdown and filenames. Binary and thesis
        # payloads remain synthetic, so this test needs no LaTeX compilation.
        with mock.patch.object(PACKAGE, 'ROOT', SCRIPT.parents[1]):
            real_entries = PACKAGE.collect_user_files()
        for source, name in real_entries:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix.lower() == '.md':
                target.write_bytes(source.read_bytes())
            elif not target.exists():
                target.write_bytes(b'packaging fixture\n')
        for directory in ('docs', 'tests', 'tools'):
            extra = self.root / directory / 'maintainer-only.md'
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('Maintainer content', encoding='utf-8')
        output = self.root / 'user-documents.zip'
        result, text = self.run_main('--source-only', '--output', str(output))
        self.assertEqual(result, 0, text)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(broken_archive_markdown_links(archive), [])
            self.assertFalse(any(name.split('/')[1] in {'docs', 'tests', 'tools'}
                                 for name in archive.namelist()))

    def test_archive_links_distinguish_navigation_from_urls_and_examples(self) -> None:
        output = self.root / 'link-cases.zip'
        with zipfile.ZipFile(output, 'w') as archive:
            archive.writestr('template/README.md', '''[Guide](GUIDE.md#start)
![Logo](figures/logo.png)
[Encoded name](notes/usage%20note.md)
[Quoted name](<notes/usage note.md>)
[Web](https://example.org/missing.md)
[Mail](mailto:example@example.org)
[Anchor](#start)
`[Code example](not-a-link.md)`
```markdown
[Fenced example](not-a-file.md)
```
[Missing](docs/missing.md)
[Reference][reference-id]
[reference-id]: docs/other-missing.md
''')
            archive.writestr('template/notes/usage note.md', '[Parent](../GUIDE.md)')
            archive.writestr('template/GUIDE.md', '# Start')
            archive.writestr('template/figures/logo.png', b'image fixture')
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(broken_archive_markdown_links(archive), [
                ('template/README.md', 'docs/missing.md'),
                ('template/README.md', 'docs/other-missing.md'),
            ])

    def english_fixture(self):
        # Distinct source contents catch selection of the other language's chapter.
        (self.root / 'GUIDE-english.md').write_text('# English user guide\n', encoding='utf-8')
        for destination, source in PACKAGE.ENGLISH_SOURCES.items():
            if source.endswith('.tex'):
                (self.root / source).write_text(f'% English {source}\n', encoding='utf-8')
        inputs = '\n'.join('\\input{' + source.removesuffix('.tex') + '}'
                           for destination, source in PACKAGE.ENGLISH_SOURCES.items()
                           if destination.startswith('chapters/') and destination.endswith('.tex'))
        (self.root / 'main-english.tex').write_text(
            '\\documentclass[master,english]{uestcthesis}\n\\input{chapters/abstract}\n' + inputs,
            encoding='utf-8')

    def test_english_archive_has_one_entry_and_only_english_chapters(self):
        self.english_fixture()
        result, text = self.run_main('--source-only', '--language', 'english')
        self.assertEqual(result, 0, text)
        output = self.root / 'dist/uestc-thesis-xovee-english-source-preview.zip'
        prefix = 'uestc-thesis-xovee-english/'
        with zipfile.ZipFile(output) as archive:
            self.assertEqual({n.removeprefix(prefix) for n in archive.namelist()}, set(PACKAGE.ROOT_FILES))
            self.assertEqual(archive.read(prefix + 'chapters/abstract.tex'), (self.root / 'chapters/abstract.tex').read_bytes())
            self.assertNotIn(b'-english', archive.read(prefix + 'main.tex'))
            self.assertNotIn(prefix + 'THIRD_PARTY.md', archive.namelist())
            self.assertEqual(archive.read(prefix + 'GUIDE.md').decode().splitlines(), ['# English user guide'])
            for destination, source in PACKAGE.ENGLISH_SOURCES.items():
                if destination != 'main.tex':
                    self.assertEqual(archive.read(prefix + destination), (self.root / source).read_bytes())
            for chapter in re.findall(rb'\\input\{([^}]+)\}', archive.read(prefix + 'main.tex')):
                self.assertIn(prefix + chapter.decode() + '.tex', archive.namelist())

    def test_english_formal_candidate_finalizes_its_own_pdf_and_language(self):
        self.english_fixture()
        self.set_guide('ready')
        result, text = self.run_main('--language', 'english')
        self.assertEqual(result, 0, text)
        path = self.root / 'dist/uestc-thesis-xovee-english-candidate.review.json'
        self.approve(path)
        result, text = self.run_main('--reviewed', str(path))
        self.assertEqual(result, 0, text)
        self.assertEqual((self.root / 'dist/uestc-thesis-xovee-english.zip').read_bytes(),
                         path.with_suffix('').with_suffix('.zip').read_bytes())
        report = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(report['language'], 'english')
        self.assertEqual(report['source_map']['main.tex'], 'main-english.tex')
        self.assertFalse(report['audit']['findings'])

    def test_review_cannot_be_used_for_the_other_language(self):
        self.english_fixture()
        path = self.prepare_formal()
        self.approve(path)
        result, text = self.run_main('--reviewed', str(path), '--language', 'english')
        self.assertEqual(result, 1)
        self.assertIn('language or source mapping differs', text)

    def test_english_source_change_invalidates_review(self):
        self.english_fixture()
        self.set_guide('ready')
        result, text = self.run_main('--language', 'english')
        self.assertEqual(result, 0, text)
        path = self.root / 'dist/uestc-thesis-xovee-english-candidate.review.json'
        self.approve(path)
        with (self.root / 'main-english.tex').open('a', encoding='utf-8') as handle:
            handle.write('\n% changed source comment\n')
        result, text = self.run_main('--reviewed', str(path))
        self.assertEqual(result, 1)
        self.assertIn('Source changed since review', text)

    def test_source_mapping_change_invalidates_review(self):
        path = self.prepare_formal()
        self.approve(path)
        report = json.loads(path.read_text(encoding='utf-8'))
        report['source_map']['main.tex'] = 'main-english.tex'
        path.write_text(json.dumps(report), encoding='utf-8')
        result, text = self.run_main('--reviewed', str(path))
        self.assertEqual(result, 1)
        self.assertIn('language or source mapping differs', text)

    def test_english_user_markdown_links_resolve_inside_actual_archive(self):
        with mock.patch.object(PACKAGE, 'ROOT', SCRIPT.parents[1]):
            real_entries = PACKAGE.collect_user_files('english')
        for source, destination in real_entries:
            if source.suffix == '.md':
                (self.root / source.relative_to(SCRIPT.parents[1])).write_bytes(source.read_bytes())
        result, text = self.run_main('--source-only', '--language', 'english')
        self.assertEqual(result, 0, text)
        with zipfile.ZipFile(self.root / 'dist/uestc-thesis-xovee-english-source-preview.zip') as archive:
            self.assertEqual(broken_archive_markdown_links(archive), [])


if __name__ == "__main__":
    unittest.main()
