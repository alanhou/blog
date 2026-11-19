"""Regression checks for grounded generation and the retry cursor."""

import io
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fetch_arxiv
from paper_sources import PaperSourceUnavailable


PAPER = {
    "id": "2611.12345",
    "title": "Example Research Method",
    "authors": ["Example Author"],
    "categories": ["cs.AI"],
    "summary": "Abstract overview.",
}
SOURCE = {
    "url": "https://arxiv.org/html/2611.12345",
    "sha256": "a" * 64,
    "text": "Section 4: Real method detail, including literal $cost and {data}.",
    "scope": "HTML text extraction; images and layout have not been inspected.",
}
ARTICLE = '''---
title:
  en: "Example contribution"
  zh: "例子中的具体贡献"
description:
  en: "An example description."
  zh: "例子的说明。"
date: 2026-11-19
tags: ["arxiv", "ai"]
image: "https://example.com/image.png"
---

:::en
**Paper**: [2611.12345](https://arxiv.org/abs/2611.12345)
## The Problem
A concrete problem.
:::

:::zh
## 问题
一个具体的问题。
:::
'''


class GenerateArticleTests(unittest.TestCase):
    @patch("fetch_arxiv.call_llm", return_value=ARTICLE)
    @patch("fetch_arxiv.fetch_reading_source", return_value=SOURCE)
    def test_original_source_reaches_prompt_without_interpolating_its_literals(self, read, llm):
        result = fetch_arxiv.generate_blog_post(Mock(), "model", "openai", PAPER)
        read.assert_called_once_with(PAPER["id"], fetch_arxiv._request_arxiv)
        prompt = llm.call_args.kwargs["messages"][0]["content"]
        self.assertIn(SOURCE["text"], prompt)
        self.assertIn(SOURCE["scope"], prompt)
        self.assertIn("Abstract overview.", prompt)
        self.assertIn("## 博导审稿", prompt)
        self.assertIn(SOURCE["sha256"], result)

    @patch("fetch_arxiv.call_llm")
    @patch("fetch_arxiv.fetch_reading_source", side_effect=PaperSourceUnavailable("No original text"))
    def test_no_original_means_no_article_generation(self, _read, llm):
        with self.assertRaises(PaperSourceUnavailable):
            fetch_arxiv.generate_blog_post(Mock(), "model", "openai", PAPER)
        llm.assert_not_called()

    @patch("fetch_arxiv.call_llm", return_value="```mdx\n" + ARTICLE + "```")
    @patch("fetch_arxiv.fetch_reading_source", return_value=SOURCE)
    def test_outer_fence_and_sanitizer_preserve_inert_mdx_provenance(self, _read, _llm):
        content = fetch_arxiv.generate_blog_post(Mock(), "model", "openai", PAPER)
        clean = fetch_arxiv.sanitize_mdx(content)
        self.assertTrue(fetch_arxiv.frontmatter_is_valid(clean))
        self.assertTrue(clean.startswith("---\n"))
        self.assertNotIn("```", clean)
        self.assertIn("{/* Reading source: https://arxiv.org/html/2611.12345;", clean)
        self.assertNotIn("\\{/*", clean)
        self.assertNotIn("<!--", clean)


class CursorRetryTests(unittest.TestCase):
    def run_pipeline(self, results, selected=True):
        start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        papers = [dict(PAPER, id=f"2611.{12345 + index}", title=f"Method {index}") for index in range(len(results))]
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            stack.enter_context(patch("fetch_arxiv.BLOG_DIR", Path(tmp)))
            stack.enter_context(patch("fetch_arxiv.get_llm_client", return_value=(Mock(), "model", "openai")))
            stack.enter_context(patch("fetch_arxiv._parse_env_date", return_value=None))
            stack.enter_context(patch("fetch_arxiv.load_cursor", return_value=start))
            stack.enter_context(patch("fetch_arxiv.fetch_papers_between", return_value=papers))
            stack.enter_context(patch("fetch_arxiv.get_existing_arxiv_ids", return_value=set()))
            stack.enter_context(patch("fetch_arxiv.select_papers", return_value=papers if selected else []))
            stack.enter_context(patch("fetch_arxiv.generate_blog_post", side_effect=results))
            stack.enter_context(patch("fetch_arxiv.generate_paper_visuals", return_value={}))
            save = stack.enter_context(patch("fetch_arxiv.save_cursor"))
            stack.enter_context(redirect_stdout(io.StringIO()))
            stack.enter_context(redirect_stderr(io.StringIO()))
            error = None
            try:
                fetch_arxiv.main()
            except SystemExit as exc:
                error = exc.code
            return start, save.call_args, error, len(list(Path(tmp).glob("*.mdx")))

    def test_partial_failure_keeps_day_for_retry_and_writes_successful_article(self):
        start, saved, error, written = self.run_pipeline([ARTICLE, PaperSourceUnavailable("No source")])
        self.assertIsNone(error)
        self.assertEqual(1, written)
        self.assertEqual(start, saved.args[0])

    def test_all_failed_exits_without_advancing_cursor(self):
        _start, saved, error, written = self.run_pipeline([PaperSourceUnavailable("No source")])
        self.assertEqual(1, error)
        self.assertEqual(0, written)
        self.assertIsNone(saved)

    def test_success_advances_to_next_day(self):
        start, saved, error, written = self.run_pipeline([ARTICLE])
        self.assertIsNone(error)
        self.assertEqual(1, written)
        self.assertEqual(start + timedelta(days=1), saved.args[0])

    def test_empty_window_advances_to_avoid_stalling_on_weekend(self):
        start, saved, error, written = self.run_pipeline([])
        self.assertIsNone(error)
        self.assertEqual(0, written)
        self.assertEqual(start + timedelta(days=1), saved.args[0])

    def test_empty_selection_is_a_failure_not_a_covered_day(self):
        _start, saved, error, written = self.run_pipeline([ARTICLE], selected=False)
        self.assertEqual(1, error)
        self.assertEqual(0, written)
        self.assertIsNone(saved)


if __name__ == "__main__":
    unittest.main()
