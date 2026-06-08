import tempfile
import unittest
from pathlib import Path

import fitz

from backend.pdf_processing.extract_drawing_comments import extract_drawing_comments


class ExtractDrawingCommentsTest(unittest.TestCase):
    def test_extracts_only_pdf_annotation_comments(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "annotated.pdf"

            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "PROJECT HEADING SHOULD NOT BE EXTRACTED")
            annot = page.add_text_annot((100, 100), "Please revise cable routing on this drawing")
            annot.update()
            doc.save(pdf_path)
            doc.close()

            comments = extract_drawing_comments(str(pdf_path))

        self.assertEqual(
            comments,
            [
                {
                    "reference": "Page 1",
                    "comment": "Please revise cable routing on this drawing",
                }
            ],
        )

    def test_ignores_text_only_pdf_content(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "text_only.pdf"

            doc = fitz.open()
            page = doc.new_page()
            page.insert_text((72, 72), "PROJECT HEADING SHOULD NOT BE EXTRACTED")
            page.insert_text((72, 96), "Drawing title block and document number")
            doc.save(pdf_path)
            doc.close()

            comments = extract_drawing_comments(str(pdf_path))

        self.assertEqual(comments, [])


if __name__ == "__main__":
    unittest.main()
