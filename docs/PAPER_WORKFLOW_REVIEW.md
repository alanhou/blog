# Paper workflow review — 2026-11-19

## Sources checked

- Local `alanhou-paper` version 5.0.0: `SKILL.md` and `references/template.md` from the installed skill. Both installed copies have the same stated version and story structure.
- Upstream `lijigang/ljg-skills`, `skills/ljg-paper`: `SKILL.md`, `ReadingGuide.md`, `references/template.org`, and `references/paper-map.md`.
- Upstream revision: `36ad0ac7589454c8000e38f848b4b5e062cfdf97`, dated 2026-10-30. Retrieved on 2026-11-19. This was the latest commit affecting the skill on `master` when checked through the GitHub API.
- Blog implementation: `scripts/fetch_arxiv.py`, `scripts/ARXIV_PROMPT_IMPROVEMENTS.md`, the workflow, and a generated article.

Upstream source: <https://github.com/lijigang/ljg-skills/tree/36ad0ac7589454c8000e38f848b4b5e062cfdf97/skills/ljg-paper>

## Findings

The September prompt update already adopted useful ljg-paper ideas: explain the actual contribution, route the explanation by contribution type, give numbers context, distinguish correlation from causation, and identify important assumptions. Replacing its headings alone would add little.

| Area | Local fork / blog behavior | Improvement supported by current upstream |
| --- | --- | --- |
| Source material | The fork asks for methods and results. The blog passes only the abstract to the authoring model, while requesting judgments about baselines, ablations, and writing quality. | Read the original paper before writing a full analysis. State the exact reading source and its limits. Do not turn missing material into invented detail. |
| Storytelling | The fork's seven-beat arc and concrete examples help a general reader follow the explanation. | Keep that strength, but do not force a reversal or causal story when the paper only confirms, measures, distinguishes, or narrows a claim. |
| Examples | The fork strongly requires one anchor example. | Prefer continuity, but allow a second example when needed to preserve an independent research question. Explain the connection. Label invented teaching examples. |
| Evidence | The fork requires at least three numerical comparisons. | Select evidence by purpose. Explain the question, fixed conditions, comparison, units, and limits. Do not invent results or pad a theoretical paper to satisfy a quota. |
| Concepts and analogy | The fork requires three concepts and a load-bearing analogy, despite describing its tools as optional elsewhere. | Explain the actual concepts and consequential design choices. Use an analogy only if its mapping is accurate; do not manufacture a third independent concept. |
| Figures | The blog always requests a gap diagram and a before/after sketch. | Use diagrams where they reduce mental assembly. Explain each diagram through a concrete case. Do not imply causal evidence or a wholesale replacement the paper did not establish. |
| Assessment | The fork and blog ask for a formal accept/reject verdict. Upstream explicitly excludes formal peer review from its default task. | Preserve calibrated limitations and useful critique, but distinguish a reading-based assessment from a venue decision. Do not allege omissions or unfair baselines without the relevant source. |
| Verification | The blog checks frontmatter and MDX, not factual support or reader understanding. | Separate syntax validation, claim/source checking, and readability evaluation. A successful build does not prove an article accurate or understandable. |

## Changes selected for this repository

1. Reuse the existing GitHub Actions pipeline and change its interval from eight to six hours. Avoid a second scheduler publishing the same feed.
2. Fetch the original arXiv HTML, with PDF text extraction as a fallback. Require usable original-paper text for full article generation; retain the announcement cursor for retry when publication fails.
3. Adapt the fork's six sections to the existing bilingual MDX schema. Keep its narrative and accessible language, while applying upstream's evidence-first exceptions above.
4. Ask the authoring model to identify claims and their source locations before drafting, and cite relevant sections, tables, or figures in the article. Record the source URL, source hash, and any excerpting in an audit comment.
5. Preserve the blog's canonical paper links, deduplication, frontmatter, visual pipeline, and automated commit/push behavior.

These changes adapt the installed skill for this blog; they do not modify the installed skill itself or claim to implement the upstream workflow in full.

## Useful follow-up work

- Persist a machine-readable paper-map containing each major research question, evidence location, support level, and claim-to-source correspondence.
- Add a separate factual review against the original material and a separate readability review given only the final article. Keep actual review answers; never prefill PASS. This change does not introduce either model review, and the prompt's self-check is not a substitute.
- Evaluate the prompt on a method paper, a theory paper, a benchmark paper, and a resource paper before making broader style changes or rewriting old posts.
- Review generated Manim illustrations against the full paper; existing visual generation is a separate path and is not validated by article checks.

Do not import upstream's personal Org/Denote/Emacs file conventions into the Astro site. Upstream currently contains mixed `.md` and `.org` references after its format rollback; this is another reason to adapt the methodology rather than copy the packaging.

## Validation of this change

- 42 Python regression tests passed, including original-paper extraction, PDF fallback, provenance, and complete/partial/failed publication cursor handling.
- All 1,876 existing MDX files passed `npm run validate`.
- A generated-format bilingual fixture with its source audit comment compiled through the actual MDX compiler and bilingual directive plugin.
- Astro's production build completed successfully: 1,980 pages.
- Live source extraction was checked against arXiv `2611.24032`: HTML yielded 131,954 text characters with table rows retained; the PDF yielded 122,797 text characters across 38 labeled pages. Both exceed the 100,000-character reading budget, exercising the need to disclose excerpting.
- The existing GitHub paper workflow was verified as active before publication.
- No live LLM article generation or independent model review was run for this change. Prompt behavior still needs the representative-paper evaluation described above; extraction and build checks do not certify generated factual claims.
