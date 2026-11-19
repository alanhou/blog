"""Original-paper extraction and failure handling, without network calls."""

import hashlib
import sys
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock, patch

from pypdf import PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paper_sources


class PaperSourceTests(unittest.TestCase):
    def test_html_keeps_section_labels_tables_captions_and_math(self):
        raw = b'''<html><nav>Outside navigation</nav><article>
        <h2>3 Experiments</h2><script>do not keep this script</script>
        <p>The scores are in Table 1.</p><table><tr><th>Method</th><th>Score</th></tr>
        <tr><td>Baseline</td><td>42%</td></tr></table>
        <figure><img alt="Architecture drawing"><figcaption>Figure 2: system</figcaption></figure>
        <math alttext="x + y"><mi>scrambled math</mi></math></article></html>'''
        text = paper_sources.extract_html_paper(raw)
        for expected in ("3 Experiments", "Method | Score", "Baseline | 42%", "Figure 2", "x + y"):
            self.assertIn(expected, text)
        for unwanted in ("Outside navigation", "do not keep", "scrambled math"):
            self.assertNotIn(unwanted, text)

    def test_html_rejects_non_paper_landing_page(self):
        with self.assertRaises(ValueError):
            paper_sources.extract_html_paper(b"<html><main>Access challenge</main></html>")

    @patch("paper_sources.time.sleep")
    def test_html_success_records_raw_source_hash_and_does_not_fetch_pdf(self, sleep):
        raw = ("<article><h2>Method</h2><p>" + "An actual method step. " * 100 + "</p></article>").encode()
        request = Mock(return_value=Mock(content=raw))
        source = paper_sources.fetch_reading_source("2611.12345", request)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), source["sha256"])
        self.assertEqual("https://arxiv.org/html/2611.12345", source["url"])
        self.assertFalse(source["truncated"])
        self.assertIn("images and layout have not been inspected", source["scope"])
        request.assert_called_once_with(source["url"], accept="text/html", max_retries=1)
        sleep.assert_called_once_with(3)

    @patch("paper_sources.extract_pdf_paper", return_value="PDF methods and results. " * 100)
    @patch("paper_sources.time.sleep")
    def test_pdf_fallback_after_html_request_failure(self, sleep, extract):
        request = Mock(side_effect=[RuntimeError("HTML not available"), Mock(content=b"%PDF-1.7 source")])
        source = paper_sources.fetch_reading_source("2611.12345", request)
        self.assertEqual("https://arxiv.org/pdf/2611.12345", source["url"])
        self.assertIn("PDF text extraction", source["scope"])
        self.assertEqual(2, sleep.call_count)
        extract.assert_called_once_with(b"%PDF-1.7 source")

    @patch("paper_sources.time.sleep")
    def test_unreadable_original_does_not_fall_back_to_abstract(self, _sleep):
        request = Mock(return_value=Mock(content=b"<html>Temporary error</html>"))
        with self.assertRaises(paper_sources.PaperSourceUnavailable):
            paper_sources.fetch_reading_source("2611.12345", request)
        self.assertEqual(2, request.call_count)

    @patch("paper_sources.time.sleep")
    def test_abstract_sized_article_is_not_treated_as_full_paper(self, _sleep):
        request = Mock(return_value=Mock(content=b"<article>Only a short abstract.</article>"))
        with self.assertRaises(paper_sources.PaperSourceUnavailable):
            paper_sources.fetch_reading_source("2611.12345", request)

    @patch("paper_sources.MAX_SOURCE_BYTES", 10)
    @patch("paper_sources.time.sleep")
    def test_oversized_source_is_rejected(self, _sleep):
        request = Mock(return_value=Mock(content=b"x" * 11))
        with self.assertRaises(paper_sources.PaperSourceUnavailable):
            paper_sources.fetch_reading_source("2611.12345", request)

    @patch("paper_sources.MAX_PROMPT_CHARS", 2000)
    @patch("paper_sources.time.sleep")
    def test_excerpting_preserves_both_ends_and_is_disclosed(self, _sleep):
        raw = ("<article>Beginning " + "Methods and evidence. " * 200 + " The ending.</article>").encode()
        source = paper_sources.fetch_reading_source("2611.12345", Mock(return_value=Mock(content=raw)))
        self.assertTrue(source["truncated"])
        self.assertTrue(source["text"].startswith("Beginning"))
        self.assertTrue(source["text"].endswith("The ending."))
        self.assertIn("Middle of extracted source omitted", source["text"])
        self.assertIn("middle is omitted", source["scope"])

    def test_pdf_reader_retains_original_page_numbers(self):
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=300)
        writer.add_blank_page(width=300, height=300)
        buffer = BytesIO()
        writer.write(buffer)
        self.assertEqual("[PDF page 1]\n\n\n[PDF page 2]\n", paper_sources.extract_pdf_paper(buffer.getvalue()))

    def test_invalid_id_cannot_redirect_requests_to_another_host(self):
        request = Mock()
        with self.assertRaises(ValueError):
            paper_sources.fetch_reading_source("https://example.com/commands", request)
        request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
