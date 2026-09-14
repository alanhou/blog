#!/usr/bin/env python3
"""Regression tests for the arXiv metadata fetch path."""

import sys
import unittest
from datetime import datetime, timedelta, timezone
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

OAI_RESPONSE = """\
<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
  <responseDate>2026-08-21T06:31:33Z</responseDate>
  <request verb="ListRecords">http://oaipmh.arxiv.org/oai</request>
  <ListRecords>
    <record>
      <header>
        <identifier>oai:arXiv.org:2608.18066</identifier>
        <datestamp>2026-08-21</datestamp>
        <setSpec>cs:cs:AI</setSpec>
      </header>
      <metadata>
        <arXivRaw xmlns="http://arxiv.org/OAI/arXivRaw/">
          <id>2608.18066</id>
          <submitter>Ada Example</submitter>
          <version version="v1">
            <date>Wed, 19 Aug 2026 12:00:00 GMT</date>
          </version>
          <title>A Paper
            With A Wrapped Title</title>
          <authors>Ada Example, Grace Example</authors>
          <categories>cs.AI cs.LG</categories>
          <abstract>An abstract.</abstract>
        </arXivRaw>
      </metadata>
    </record>
    <record>
      <header>
        <identifier>oai:arXiv.org:2608.18067v1</identifier>
        <datestamp>2026-08-21</datestamp>
        <setSpec>cs:cs:AI</setSpec>
      </header>
      <metadata>
        <arXivRaw xmlns="http://arxiv.org/OAI/arXivRaw/">
          <id>2608.18067</id>
          <submitter>Alan Example</submitter>
          <version version="v1">
            <date>Thu, 20 Aug 2026 12:00:00 GMT</date>
          </version>
          <title>Second Paper</title>
          <authors>Alan Example</authors>
          <categories>cs.LG</categories>
          <abstract>Second abstract.</abstract>
        </arXivRaw>
      </metadata>
    </record>
    <record>
      <header>
        <identifier>oai:arXiv.org:2401.07468</identifier>
        <datestamp>2026-08-21</datestamp>
        <setSpec>cs:cs:AI</setSpec>
      </header>
      <metadata>
        <arXivRaw xmlns="http://arxiv.org/OAI/arXivRaw/">
          <id>2401.07468</id>
          <submitter>Barak Or</submitter>
          <version version="v1">
            <date>Mon, 15 Jan 2024 04:51:34 GMT</date>
          </version>
          <version version="v4">
            <date>Thu, 20 Aug 2026 05:48:42 GMT</date>
          </version>
          <title>An Old Paper On Its Fourth Version</title>
          <authors>Barak Or</authors>
          <categories>cs.LG</categories>
          <abstract>Fourth version abstract.</abstract>
        </arXivRaw>
      </metadata>
    </record>
    <resumptionToken expirationDate="2026-09-15T00:00:00Z">page-2</resumptionToken>
  </ListRecords>
</OAI-PMH>
"""

OAI_LAST_PAGE = """\
<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
  <ListRecords>
    <record>
      <header>
        <identifier>oai:arXiv.org:2608.18065</identifier>
        <datestamp>2026-08-21</datestamp>
        <setSpec>cs:cs:AI</setSpec>
      </header>
      <metadata>
        <arXivRaw xmlns="http://arxiv.org/OAI/arXivRaw/">
          <id>2608.18065</id>
          <submitter>Alan Example</submitter>
          <version version="v1">
            <date>Tue, 18 Aug 2026 12:00:00 GMT</date>
          </version>
          <title>Oldest Submission</title>
          <authors>Alan Example</authors>
          <categories>cs.AI</categories>
          <abstract>Oldest abstract.</abstract>
        </arXivRaw>
      </metadata>
    </record>
  </ListRecords>
</OAI-PMH>
"""


OAI_WITHDRAWN_PAGE = """\
<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">
  <ListRecords>
    <record>
      <header>
        <identifier>oai:arXiv.org:2608.00001</identifier>
        <datestamp>2026-08-21</datestamp>
        <setSpec>cs:cs:AI</setSpec>
      </header>
    </record>
    <resumptionToken/>
  </ListRecords>
</OAI-PMH>
"""


# OAI_RESPONSE without the pagination cursor -- what a single-page window looks
# like, and what each set returns when a paper is cross-listed.
OAI_FINAL_PAGE = OAI_RESPONSE.replace(
    '    <resumptionToken expirationDate="2026-09-15T00:00:00Z">page-2</resumptionToken>\n',
    "",
)


def response(text, status_code=200, headers=None):
    result = Mock()
    result.text = text
    result.status_code = status_code
    result.headers = headers or {}
    result.raise_for_status.side_effect = None
    return result


def oai_papers(xml_text):
    """Papers from an OAI page, without the resumption token."""
    return fetch_arxiv._parse_oai_papers(xml_text)[0]


def rss_feed_dated(pub_date):
    return RSS_RESPONSE.replace("Wed, 29 Jul 2026 00:00:00 -0400", pub_date)


def today_feed():
    return rss_feed_dated(datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z"))


class FetchPapersBetweenTests(unittest.TestCase):
    """The blog walks a date cursor forward one announcement day at a time, so
    every source in the chain has to answer for the requested window rather
    than for "whatever is newest right now"."""

    def setUp(self):
        self.since = datetime(2026, 8, 21, tzinfo=timezone.utc)
        self.until = datetime(2026, 8, 22, tzinfo=timezone.utc)

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_oai_request_carries_the_date_window_and_pages_with_the_token(self, get, _sleep):
        get.side_effect = [response(OAI_RESPONSE), response(OAI_LAST_PAGE)]

        papers = fetch_arxiv.fetch_papers_between(["cs.AI"], self.since, self.until)

        self.assertEqual(
            ["2608.18067", "2608.18066", "2608.18065"],
            [paper["id"] for paper in papers],
        )
        first, second = get.call_args_list
        self.assertEqual("https://oaipmh.arxiv.org/oai", first.args[0])
        self.assertEqual("application/xml", first.kwargs["headers"]["Accept"])
        self.assertEqual("arXivRaw", first.kwargs["params"]["metadataPrefix"])
        self.assertEqual("2026-08-21", first.kwargs["params"]["from"])
        self.assertEqual("2026-08-22", first.kwargs["params"]["until"])
        self.assertEqual("cs:cs:AI", first.kwargs["params"]["set"])
        # The second page must resume by token, not restart the range.
        self.assertEqual("page-2", second.kwargs["params"]["resumptionToken"])
        self.assertNotIn("set", second.kwargs["params"])

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_ignores_papers_whose_first_version_predates_the_window(self, get, _sleep):
        """A 2024 paper re-versioned today has a datestamp inside the window,
        but it is not what the blog means by a new paper."""
        get.return_value = response(OAI_FINAL_PAGE)

        papers = fetch_arxiv.fetch_papers_between(["cs.AI"], self.since, self.until)

        self.assertNotIn("2401.07468", [paper["id"] for paper in papers])

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_oai_results_are_deduped_across_sets(self, get, _sleep):
        get.side_effect = [response(OAI_FINAL_PAGE), response(OAI_FINAL_PAGE)]

        papers = fetch_arxiv.fetch_papers_between(
            ["cs.AI", "cs.LG"], self.since, self.until
        )

        self.assertEqual(["2608.18067", "2608.18066"], [paper["id"] for paper in papers])
        self.assertEqual(["cs.AI", "cs.LG"], papers[1]["categories"])
        self.assertEqual(
            ["cs:cs:AI", "cs:cs:LG"],
            [call.kwargs["params"]["set"] for call in get.call_args_list],
        )

    def test_merge_unions_categories_for_cross_listed_papers(self):
        papers = {}

        fetch_arxiv._merge_paper(papers, {"id": "2608.18066", "categories": ["cs.AI"]})
        fetch_arxiv._merge_paper(papers, {"id": "2608.18066", "categories": ["cs.LG"]})

        self.assertEqual(["2608.18066"], list(papers))
        self.assertEqual(["cs.AI", "cs.LG"], papers["2608.18066"]["categories"])

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_keeps_three_seconds_between_arxiv_requests(self, get, sleep):
        get.side_effect = [response(OAI_RESPONSE), response(OAI_LAST_PAGE)]

        fetch_arxiv.fetch_papers_between(["cs.AI"], self.since, self.until)

        self.assertEqual(2, get.call_count)
        self.assertEqual([3, 3], [call.args[0] for call in sleep.call_args_list])

    @patch("fetch_arxiv._fetch_oai_papers")
    @patch("fetch_arxiv._fetch_atom_papers")
    @patch("fetch_arxiv.time.sleep")
    def test_falls_back_to_the_atom_api_with_the_same_window(self, _sleep, atom, oai):
        oai.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")
        atom.return_value = oai_papers(OAI_LAST_PAGE)

        papers = fetch_arxiv.fetch_papers_between(["cs.AI"], self.since, self.until)

        self.assertEqual(["2608.18065"], [paper["id"] for paper in papers])
        self.assertEqual(
            (self.since, self.until),
            atom.call_args.kwargs["window"],
        )

    @patch("fetch_arxiv._fetch_oai_papers")
    @patch("fetch_arxiv._fetch_atom_papers")
    def test_refuses_rss_for_an_old_window(self, atom, oai):
        """RSS has no date range, so serving a backfilled day from it would
        return today's papers and mark the requested day as covered."""
        oai.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")
        atom.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")

        with self.assertRaises(RuntimeError):
            fetch_arxiv.fetch_papers_between(["cs.AI"], self.since, self.until)

    @patch("fetch_arxiv._fetch_oai_papers")
    @patch("fetch_arxiv._fetch_atom_papers")
    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_uses_rss_for_the_current_day(self, get, _sleep, atom, oai):
        oai.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")
        atom.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")
        get.return_value = response(today_feed())

        today = datetime.now(timezone.utc)
        papers = fetch_arxiv.fetch_papers_between(["cs.AI"], today, today)

        self.assertEqual("2607.24759", papers[0]["id"])
        self.assertEqual("Recovered through the RSS feed.", papers[0]["summary"])
        self.assertEqual(["Ada Example", "Grace Example"], papers[0]["authors"])

    @patch("fetch_arxiv._fetch_oai_papers")
    @patch("fetch_arxiv._fetch_atom_papers")
    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_drops_rss_items_outside_the_window(self, get, _sleep, atom, oai):
        oai.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")
        atom.side_effect = fetch_arxiv.requests.exceptions.ReadTimeout("429")
        get.return_value = response(RSS_RESPONSE)  # dated 2026-07-29

        today = datetime.now(timezone.utc)
        papers = fetch_arxiv.fetch_papers_between(["cs.AI"], today, today)

        self.assertEqual([], papers)

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_caps_the_candidates_it_returns(self, get, _sleep):
        get.side_effect = [response(OAI_RESPONSE), response(OAI_LAST_PAGE)]

        papers = fetch_arxiv.fetch_papers_between(
            ["cs.AI"], self.since, self.until, max_results=2
        )

        self.assertEqual(["2608.18067", "2608.18066"], [paper["id"] for paper in papers])


class ParseOaiPapersTests(unittest.TestCase):
    def test_parses_record_fields(self):
        papers, token = fetch_arxiv._parse_oai_papers(OAI_RESPONSE)

        self.assertEqual("page-2", token)
        self.assertEqual(3, len(papers))
        first = papers[0]
        self.assertEqual("2608.18066", first["id"])
        self.assertEqual("A Paper With A Wrapped Title", first["title"])
        self.assertEqual("An abstract.", first["summary"])
        self.assertEqual(["Ada Example", "Grace Example"], first["authors"])
        self.assertEqual(["cs.AI", "cs.LG"], first["categories"])
        self.assertEqual("2026-08-21", first["announced"])

    def test_published_is_the_first_version_date(self):
        papers, _ = fetch_arxiv._parse_oai_papers(OAI_RESPONSE)

        revised = next(paper for paper in papers if paper["id"] == "2401.07468")
        self.assertTrue(revised["published"].startswith("2024-01-15"))

    def test_last_page_has_no_token(self):
        papers, token = fetch_arxiv._parse_oai_papers(OAI_LAST_PAGE)

        self.assertIsNone(token)
        self.assertEqual(1, len(papers))

    def test_skips_records_without_metadata_and_stops_on_an_empty_token(self):
        papers, token = fetch_arxiv._parse_oai_papers(OAI_WITHDRAWN_PAGE)

        self.assertEqual([], papers)
        self.assertIsNone(token)


class AtomQueryTests(unittest.TestCase):
    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_atom_request_identifies_client_and_uses_https(self, get, _sleep):
        get.return_value = response(ATOM_RESPONSE)

        papers = fetch_arxiv._fetch_atom_papers(["cs.AI"], max_results=1)

        self.assertEqual(["2607.24758"], [paper["id"] for paper in papers])
        request = get.call_args
        self.assertEqual("https://export.arxiv.org/api/query", request.args[0])
        self.assertIn("alanhou-blog", request.kwargs["headers"]["User-Agent"])
        self.assertEqual("application/atom+xml", request.kwargs["headers"]["Accept"])

    @patch("fetch_arxiv.time.sleep")
    @patch("fetch_arxiv.requests.get")
    def test_atom_query_restricts_to_the_window(self, get, _sleep):
        get.return_value = response(ATOM_RESPONSE)
        since = datetime(2026, 8, 21, tzinfo=timezone.utc)
        until = datetime(2026, 8, 22, tzinfo=timezone.utc)

        fetch_arxiv._fetch_atom_papers(["cs.AI"], max_results=5, window=(since, until))

        search_query = get.call_args.kwargs["params"]["search_query"]
        self.assertIn("submittedDate:[202608210000 TO 202608220000]", search_query)


class PatchFrontmatterTests(unittest.TestCase):
    MDX = (
        "---\n"
        'title:\n  en: "A Post"\n  zh: "一篇文章"\n'
        "date: 2026-08-21\n"
        'image: "https://arxiv.org/static/browse/0.3.4/images/arxiv-logo-fb.png"\n'
        "---\n\n"
        ":::en\ndate: this line is body text\n:::zh\n"
    )

    def test_patch_date_replaces_only_the_frontmatter_field(self):
        patched = fetch_arxiv.patch_frontmatter_date(self.MDX, "2026-08-21")

        self.assertIn("date: 2026-08-21", patched)
        self.assertEqual(1, patched.count("date: 2026-08-21"))

    def test_patch_date_leaves_the_body_untouched(self):
        patched = fetch_arxiv.patch_frontmatter_date(self.MDX, "2026-01-02")

        self.assertTrue(patched.startswith("---\ntitle:"))
        self.assertIn("date: 2026-01-02", patched)
        self.assertIn(":::en\ndate: this line is body text", patched)

    def test_patched_date_keeps_frontmatter_valid(self):
        patched = fetch_arxiv.patch_frontmatter_date(self.MDX, "2026-08-21")

        self.assertTrue(fetch_arxiv.frontmatter_is_valid(patched))


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

    @patch("fetch_arxiv.time.sleep")
    def test_cloudflare_challenge_is_retried(self, _sleep):
        """The gateway's challenge page arrives as HTML with no status code in
        the message, so only the body identifies it as transient."""
        client = Mock()
        client.chat.completions.create.side_effect = [
            Exception("<!DOCTYPE html><title>Just a moment...</title>"),
            iter([]),
        ]

        fetch_arxiv.call_llm(client, "gpt-x", "openai", messages=[])

        self.assertEqual(2, client.chat.completions.create.call_count)


if __name__ == "__main__":
    unittest.main()
