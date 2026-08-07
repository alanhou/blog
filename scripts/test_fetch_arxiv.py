#!/usr/bin/env python3
"""Regression tests for the arXiv metadata fetch path."""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fetch_arxiv


ATOM_RESPONSE = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>https://arxiv.org/abs/2607.24758v1</id>
    <published>2026-07-29T00:00:00Z</published>
    <title>Do Models Fake Alignment?</title>
    <summary>An abstract.</summary>
    <author><name>Ada Example</name></author>
    <category term="cs.AI"/>
  </entry>
</feed>
"""

RSS_RESPONSE = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:arxiv="http://arxiv.org/schemas/atom"
     xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">
  <channel>
    <item>
      <title>Fallback Paper</title>
      <link>https://arxiv.org/abs/2607.24759</link>
      <description>arXiv:2607.24759v1 Announce Type: new
Abstract: Recovered through the RSS feed.</description>
      <category>cs.AI</category>
      <pubDate>Wed, 29 Jul 2026 00:00:00 -0400</pubDate>
      <dc:creator>Ada Example, Grace Example</dc:creator>
    </item>
  </channel>
</rss>
"""


def response(text, status_code=200, headers=None):
    result = Mock()
    result.text = text
    result.status_code = status_code
    result.headers = headers or {}
    result.raise_for_status.side_effect = None
    return result


class FetchRecentPapersTests(unittest.TestCase):
    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_atom_request_identifies_client_and_uses_https(self, get, _sleep):
        get.return_value = response(ATOM_RESPONSE)

        papers = fetch_arxiv.fetch_recent_papers(["cs.AI"], max_results=1)

        self.assertEqual(["2607.24758"], [paper["id"] for paper in papers])
        request = get.call_args
        self.assertEqual("https://export.arxiv.org/api/query", request.args[0])
        self.assertIn("alanhou-blog", request.kwargs["headers"]["User-Agent"])
        self.assertEqual("application/atom+xml", request.kwargs["headers"]["Accept"])

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_rss_fallback_recovers_after_atom_timeouts(self, get, _sleep):
        get.side_effect = [
            fetch_arxiv.requests.exceptions.ReadTimeout("atom unavailable"),
            fetch_arxiv.requests.exceptions.ReadTimeout("atom unavailable"),
            fetch_arxiv.requests.exceptions.ReadTimeout("atom unavailable"),
            response(RSS_RESPONSE),
        ]

        papers = fetch_arxiv.fetch_recent_papers(["cs.AI"], max_results=1)

        self.assertEqual("2607.24759", papers[0]["id"])
        self.assertEqual("Recovered through the RSS feed.", papers[0]["summary"])
        self.assertEqual(
            ["Ada Example", "Grace Example"],
            papers[0]["authors"],
        )
        self.assertEqual(
            "https://rss.arxiv.org/rss/cs.AI",
            get.call_args.args[0],
        )


class CallLlmTests(unittest.TestCase):
    """The endpoint sits behind a gateway that drops silent connections, so
    every call has to stream."""

    def _anthropic_client(self, chunks):
        stream = Mock()
        stream.text_stream = iter(chunks)
        client = Mock()
        client.messages.stream.return_value.__enter__ = Mock(return_value=stream)
        client.messages.stream.return_value.__exit__ = Mock(return_value=False)
        return client

    def _openai_client(self, chunks):
        def make_chunk(text):
            chunk = Mock()
            chunk.choices = [Mock(delta=Mock(content=text))]
            return chunk

        client = Mock()
        client.chat.completions.create.return_value = iter(
            [make_chunk(text) for text in chunks]
        )
        return client

    def test_anthropic_streams_and_joins_chunks(self):
        client = self._anthropic_client(["Hello", " ", "world"])

        result = fetch_arxiv.call_llm(client, "claude-x", "anthropic", messages=[])

        self.assertEqual("Hello world", result)

    def test_openai_requests_a_stream(self):
        client = self._openai_client(["Hello", " world"])

        result = fetch_arxiv.call_llm(client, "gpt-x", "openai", messages=[])

        self.assertEqual("Hello world", result)
        self.assertTrue(client.chat.completions.create.call_args.kwargs["stream"])

    def test_openai_tolerates_chunks_without_choices(self):
        """Usage-only chunks arrive with an empty choices list."""
        client = self._openai_client(["Hi"])
        empty = Mock()
        empty.choices = []
        client.chat.completions.create.return_value = iter([empty])

        self.assertEqual("", fetch_arxiv.call_llm(client, "gpt-x", "openai", messages=[]))

    @patch("fetch_arxiv.time.sleep")
    def test_gateway_403_is_retried(self, _sleep):
        client = Mock()
        client.chat.completions.create.side_effect = [
            Exception("<h1>403 Forbidden</h1> openresty"),
            iter([]),
        ]

        fetch_arxiv.call_llm(client, "gpt-x", "openai", messages=[])

        self.assertEqual(2, client.chat.completions.create.call_count)


if __name__ == "__main__":
    unittest.main()
