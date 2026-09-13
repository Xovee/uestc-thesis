"""Real PDF objects and synthetic contact details exercise the release audit."""
from pathlib import Path
import importlib.util
import io
import unittest

from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject, DecodedStreamObject

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/release_audit.py'
SPEC = importlib.util.spec_from_file_location('audit_under_test', SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class ReleaseAuditTests(unittest.TestCase):
    def writer(self):
        writer = PdfWriter()
        writer.add_blank_page(595.28, 841.89)
        writer.add_metadata({'/Producer': '', '/Title': '论文题目', '/Author': '作者姓名',
                             '/Creator': 'UESTC Thesis LaTeX Template by Xovee Xu'})
        return writer

    def inspect(self, writer):
        output = io.BytesIO()
        writer.write(output)
        summary, findings = AUDIT.inspect_pdf('uestc-thesis-example.pdf', output.getvalue())
        self.assertNotIn('unreadable_pdf', {row['kind'] for row in findings}, summary)
        return {row['kind'] for row in findings}

    def test_normal_web_links_and_public_contact_are_allowed(self):
        text = 'https://github.com/Xovoee/uestc-thesis http://example.org/home/public mailto:xovee.xu@gmail.com'
        self.assertEqual(AUDIT.scan_text(text, 'fixture'), [])

    def test_private_contact_numbers_and_local_paths_are_detected(self):
        fixtures = {
            'private.person@example.invalid': 'email',
            '138-0013-8000': 'phone',
            'Phone: +1 (202) 555-0147': 'phone',
            '110101199001011234': 'identity_number',
            '学号：202301234567': 'student_number',
            'Student ID: 202301234567': 'student_number',
            'C:\\Users\\Synthetic\\private.tex': 'local_path',
            '/home/synthetic/private.tex': 'local_path',
            'file:///Users/synthetic/private.pdf': 'local_path',
            '\\\\server\\private\\document.pdf': 'local_path',
        }
        for text, kind in fixtures.items():
            with self.subTest(text=text):
                self.assertIn(kind, {row['kind'] for row in AUDIT.scan_text(text, 'fixture')})

    def test_masked_student_numbers_are_not_real_identifiers(self):
        self.assertEqual(AUDIT.scan_text('学  号 2017XXXXXXXX\nStudent ID 2017XXXXXXXX', 'fixture'), [])

    def test_clean_example_metadata_is_allowed(self):
        self.assertEqual(self.inspect(self.writer()), set())

    def test_example_metadata_matches_selected_language(self):
        writer = self.writer()
        writer.add_metadata({'/Title': 'English Thesis Title', '/Author': 'Author Name'})
        output = io.BytesIO()
        writer.write(output)
        _, english = AUDIT.inspect_pdf('uestc-thesis-example.pdf', output.getvalue(), 'english')
        _, chinese = AUDIT.inspect_pdf('uestc-thesis-example.pdf', output.getvalue(), 'chinese')
        self.assertEqual(english, [])
        self.assertIn('example_metadata_must_use_placeholders', {r['kind'] for r in chinese})

    def test_bookmark_siblings_are_not_executable_actions(self):
        writer = self.writer()
        writer.add_outline_item('First', 0)
        writer.add_outline_item('Second', 0)
        self.assertEqual(self.inspect(writer), set())

    def test_personal_author_and_custom_metadata_are_rejected(self):
        writer = self.writer()
        writer.add_metadata({'/Author': 'Synthetic Person', '/PrivateNote': 'private.person@example.invalid'})
        self.assertTrue({'example_metadata_must_use_placeholders', 'unexpected_example_metadata', 'email'} <= self.inspect(writer))

    def test_pdf_attachment_is_rejected(self):
        writer = self.writer()
        writer.add_attachment('private-note.txt', b'Synthetic test content')
        self.assertIn('attachments_forms_or_active_content', self.inspect(writer))

    def test_pdf_javascript_is_rejected(self):
        writer = self.writer()
        writer.add_js("app.alert('synthetic test');")
        self.assertIn('attachments_forms_or_active_content', self.inspect(writer))

    def test_pdf_form_is_rejected(self):
        writer = self.writer()
        writer._root_object[NameObject('/AcroForm')] = DictionaryObject({NameObject('/Fields'): ArrayObject()})
        self.assertIn('attachments_forms_or_active_content', self.inspect(writer))

    def test_pdf_comment_is_rejected(self):
        writer = self.writer()
        writer.add_annotation(0, DictionaryObject({
            NameObject('/Subtype'): NameObject('/Text'),
            NameObject('/Rect'): ArrayObject([NumberObject(n) for n in (10, 10, 30, 30)]),
            NameObject('/Contents'): TextStringObject('Synthetic private note'),
        }))
        self.assertIn('unexpected_pdf_annotation', self.inspect(writer))

    def test_launch_action_is_rejected(self):
        writer = self.writer()
        writer._root_object[NameObject('/OpenAction')] = DictionaryObject({
            NameObject('/S'): NameObject('/Launch'), NameObject('/F'): TextStringObject('synthetic.exe')})
        self.assertIn('unsafe_pdf_action', self.inspect(writer))

    def test_new_xmp_metadata_is_rejected(self):
        writer = self.writer()
        metadata = DecodedStreamObject()
        metadata.set_data(b'<metadata>private.person@example.invalid</metadata>')
        metadata[NameObject('/Type')] = NameObject('/Metadata')
        metadata[NameObject('/Subtype')] = NameObject('/XML')
        writer._root_object[NameObject('/Metadata')] = writer._add_object(metadata)
        self.assertTrue({'unreviewed_xmp_metadata', 'email'} <= self.inspect(writer))

    def test_existing_font_copyright_metadata_is_preserved(self):
        root = SCRIPT.parents[1]
        for name in ('cover.pdf', 'declaration.pdf'):
            summary, findings = AUDIT.inspect_pdf(name, (root / name).read_bytes())
            self.assertEqual(findings, [])
            self.assertEqual(set(summary['xmp_sha256']), AUDIT.APPROVED_RIGHTS_XMP)

    def test_unreadable_and_encrypted_pdfs_are_rejected(self):
        _, findings = AUDIT.inspect_pdf('fixture.pdf', b'not a PDF')
        self.assertIn('unreadable_pdf', {row['kind'] for row in findings})
        writer = self.writer()
        writer.encrypt('synthetic password')
        output = io.BytesIO()
        writer.write(output)
        _, findings = AUDIT.inspect_pdf('fixture.pdf', output.getvalue())
        self.assertIn('encrypted_pdf', {row['kind'] for row in findings})


if __name__ == '__main__':
    unittest.main()
