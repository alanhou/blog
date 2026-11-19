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

1. Run the six-hour paper check, skill-based generation, validation, commit, and push locally through Codex. The user clarified that GitHub should receive the results rather than execute the recurring paper-generation job. Remove the GitHub Actions schedule and preserve manual dispatch as an optional fallback, avoiding two publishers for the same feed.
2. Fetch the original arXiv HTML, with PDF text extraction as a fallback. Require usable original-paper text for full article generation; retain the announcement cursor for retry when publication fails.
3. Adapt the fork's six sections to the existing bilingual MDX schema. Keep its narrative and accessible language, while applying upstream's evidence-first exceptions above.
4. Ask the authoring model to identify claims and their source locations before drafting, and cite relevant sections, tables, or figures in the article. Record the source URL, source hash, and any excerpting in an audit comment.
5. Preserve the blog's canonical paper links, deduplication, frontmatter, visual pipeline, and automated commit/push behavior.

These changes adapt the installed skill for this blog; they do not modify the installed skill itself or claim to implement the upstream workflow in full.

## Local execution clarification

The recurring automation operates in the local blog checkout. Each run checks the existing paper IDs, reads original sources for selected new papers, produces bilingual articles with the installed skill, validates the generated MDX and site build, and only then commits and pushes the run's output. Unrelated local files are not staged. Runs that find no suitable new papers do not manufacture articles or empty commits.

The GitHub `arxiv.yml` workflow is manual only. The ordinary deploy-on-push workflow remains responsible for publishing committed site changes. The optional Python/API pipeline and its GitHub secrets are still available for manual use; the local Codex skill workflow does not depend on dispatching it remotely.

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
- The existing GitHub paper workflow was verified as available; its scheduled trigger was subsequently removed after the user clarified that the six-hour execution must be local. Manual dispatch is preserved.
- The initial pipeline validation did not include live article generation or independent reading review. The subsequent local publishing test below exercises Codex skill execution; it does not benchmark the optional API prompt across contribution types.

## Local publishing test — 2026-11-19

The test ran in the local repository through Codex, without dispatching GitHub Actions or requiring local LLM API credentials. The native metadata check returned 35 new candidates; supplemental Atom/RSS discovery yielded 252 uncovered candidates after deduplication. Two papers were selected for a focused publishing test:

| Paper | Local article | Original HTML SHA-256 |
| --- | --- | --- |
| `2611.24924`, AHE-Beta | `src/content/blog/arxiv-agentic-harness-engineering-beta-requirements.mdx` | `28c3c024842be4c9548eaf100131a9513dabe591e250d6236888d326aabe8604` |
| `2611.24778`, Counterfactual World Models | `src/content/blog/arxiv-counterfactual-world-models-jepas-what-if.mdx` | `df0ff663af26d0a48e5557b0cd46987ad2d1ae81201c96f624e1b4141d743ffe` |

Both articles were written locally from the original paper text with bilingual frontmatter, the skill's six Chinese sections, evidence locations, limits, and source audit comments. Neither paper ID was already covered by another article. The announcement cursor remains at 2026-11-19 because this selected batch does not establish complete daily coverage.

A separate context read only the finished articles and checked narrative, paper identity, understanding, and reconstruction. It identified missing terminology, the need to explain AHE-Beta's three-run evaluation average, an underspecified feedback comparison, and several bilingual wording differences. These were corrected and reread; the remaining Chinese feedback-comparison wording was aligned afterward. The checks assess readability and consistency, not the original papers' factual correctness or reproducibility.

The normal Satori cover command generated two 1200×630 covers. Both were visually inspected. All 1,878 MDX files passed validation, the final articles compiled through the actual MDX/bilingual plugin, and the 42 Python regression tests passed. The full local `npm run build` succeeded with Astro telemetry disabled: 1,982 pages. Both new article routes rendered with their Chinese sections, and source-audit comments remained absent from visible HTML.

The app-managed local automation **Check papers and publish articles locally** is active at a six-hour interval. GitHub's paper workflow is manual only; GitHub still deploys normal pushes.

## Local publishing check — 2026-11-20

The next local run checked the outstanding 2026-11-19 announcement window: 60 candidates were read from arXiv and 58 were not yet covered in the blog. Two additional source-grounded articles were prepared:

| Paper | Local article | Original HTML SHA-256 |
| --- | --- | --- |
| `2611.24892`, On Evaluating User Simulators for Interactive Agents | `src/content/blog/arxiv-on-evaluating-user-simulators-interactive-agents.mdx` | `4693c97b5dfebf6b741c1b0c1b92687c22d5525cec5bf33408654d961f3bb80e` |
| `2611.24927`, Mapping the AI Supply Chain | `src/content/blog/arxiv-mapping-ai-supply-chain-dependencies.mdx` | `0d42b69674b324465dbd4cd78aacb9662226b1d2e03282378e03566402a732e6` |

Both use the original arXiv HTML and have local claim-to-source records. An independent reading check on the supply-chain article prompted clarification of the covered date range, the counted-edge definition behind concentration, and the mix of broad and site-restricted queries; those points were verified against and corrected from the extracted paper. The user-simulator article distinguishes deliberate perturbations from observed behavior and distinguishes detector sensitivity from trace filtering.

The same reader check found the supply-chain contribution and boundaries clear, and could reconstruct where such a map is useful. It prompted added context for the user-simulator article's score scale and filtering threshold. These are readability checks, not verification of paper facts. The supply-chain dataset spans November 2022–October 2026. Its concentration measure sums each actor's share of monthly recorded relationship counts in a filtered graph; it is not revenue or market share.

This is still a selected batch, not a full issue of every uncovered candidate. The announcement cursor remains unchanged so the next local run can continue from the same date instead of silently skipping unselected papers.
