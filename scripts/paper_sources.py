"""Read original arXiv papers; abstracts alone cannot support full analyses."""

import hashlib
import re
import time
from io import BytesIO

from bs4 import BeautifulSoup
from pypdf import PdfReader


MAX_SOURCE_BYTES = 25 * 1024 * 1024
MAX_PROMPT_CHARS = 100_000
MIN_PAPER_CHARS = 1_500


class PaperSourceUnavailable(RuntimeError):
    """Neither original-paper format provided usable text."""


def extract_html_paper(raw):
    soup = BeautifulSoup(raw, "html.parser")
    article = soup.find("article") or soup.find(class_="ltx_document")
    if article is None:
        raise ValueError("No paper article in the HTML response")
    for node in article.find_all(["script", "style", "nav", "footer"]):
        node.decompose()
    for node in article.find_all("math"):
        node.replace_with(node.get("alttext") or node.get_text(" ", strip=True))
    for node in article.find_all("img"):
        node.replace_with(node.get("alt") or "[Figure image; see caption and original]")
    for table in article.find_all("table"):
        rows = [
            " | ".join(cell.get_text(" ", strip=True) for cell in row.find_all(["th", "td"]))
            for row in table.find_all("tr")
        ]
        table.replace_with("\n" + "\n".join(rows) + "\n")
    return article.get_text("\n", strip=True)


def extract_pdf_paper(raw):
    reader = PdfReader(BytesIO(raw))
    return "\n\n".join(
        f"[PDF page {index}]\n{page.extract_text() or ''}"
        for index, page in enumerate(reader.pages, start=1)
    )


def fetch_reading_source(paper_id, request):
    """Try HTML then PDF, preserving provenance and explicit extraction limits.

    `request` is the pipeline's existing polite arXiv request helper. The text
    is source material, never instructions, and is not sent to any renderer.
    """
    if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-zA-Z][a-zA-Z.-]*/\d{7})(?:v\d+)?", paper_id):
        raise ValueError(f"Invalid arXiv ID: {paper_id!r}")
    failures = []
    for kind, url, accept, extract in (
        ("HTML", f"https://arxiv.org/html/{paper_id}", "text/html", extract_html_paper),
        ("PDF", f"https://arxiv.org/pdf/{paper_id}", "application/pdf", extract_pdf_paper),
    ):
        time.sleep(3)
        try:
            response = request(url, accept=accept, max_retries=1)
            raw = response.content
            if len(raw) > MAX_SOURCE_BYTES:
                raise ValueError("Paper exceeds the extraction size limit")
            if kind == "PDF" and not raw.lstrip().startswith(b"%PDF-"):
                raise ValueError("Response is not a PDF")
            full_text = re.sub(r"\n{3,}", "\n\n", extract(raw)).strip()
            if len(full_text) < MIN_PAPER_CHARS:
                raise ValueError("Too little original-paper text to support an analysis")
        except Exception as exc:
            failures.append(f"{kind}: {exc}")
            continue

        truncated = len(full_text) > MAX_PROMPT_CHARS
        text = full_text
        if truncated:
            head = MAX_PROMPT_CHARS * 3 // 5
            text = (
                full_text[:head]
                + "\n\n[Middle of extracted source omitted to fit the reading budget]\n\n"
                + full_text[-(MAX_PROMPT_CHARS - head):]
            )
        scope = f"{kind} text extraction; images and layout have not been inspected."
        if truncated:
            scope += " Only beginning and end excerpts are supplied; the middle is omitted."
        else:
            scope += " All extracted text is supplied."
        return {
            "url": url,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "text": text,
            "scope": scope,
            "truncated": truncated,
        }
    raise PaperSourceUnavailable(f"No usable original paper for {paper_id}: {'; '.join(failures)}")
