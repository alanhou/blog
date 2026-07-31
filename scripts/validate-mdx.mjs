#!/usr/bin/env node

/**
 * Validates MDX files for common syntax issues that break builds.
 *
 * Pass --fix to rewrite the issues that have a deterministic repair
 * (raw "<" in prose becomes the &lt; entity, <*> gets wrapped in backticks).
 * Issues without a repair (frontmatter problems) are still reported and
 * still fail the run.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';
import matter from 'gray-matter';

const ISSUES = {
  UNESCAPED_ANGLE_BRACKETS: {
    pattern: /<\*+>/g,
    message: 'Unescaped angle brackets with asterisks (e.g., <*>, <**>) - wrap in backticks',
    fix: (match) => `\`${match}\``
  }
};

// MDX renders these entities back as literal < and > in the published page,
// so escaping is invisible to the reader and keeps prose out of code styling.
function escapeAngles(text) {
  return text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Additional runtime checks for raw < that break the MDX/JSX parser even if not matching the above regex.
// These are things like bit-shift notation (r << d), generic-like <T>, or plain comparisons in prose.
function findRawAngleBracketIssues(content, filePath) {
  const errors = [];
  const lines = content.split('\n');
  let inFence = false;
  let fenceMarker = '';
  let inDisplayMath = false;

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];

    // Fenced code
    if (!inFence) {
      const fenceMatch = line.match(/^(```+|~~~+)/);
      if (fenceMatch) {
        inFence = true;
        fenceMarker = fenceMatch[1];
        continue;
      }
    } else {
      if (line.startsWith(fenceMarker) || line.match(new RegExp('^' + fenceMarker[0] + '{' + fenceMarker.length + '}'))) {
        inFence = false;
      }
      continue;
    }

    // Track display math $$ ... $$ (cross-line rough toggle for skipping angle checks in LaTeX math source)
    const dmCount = (line.match(/\$\$/g) || []).length;
    if (dmCount % 2 === 1) {
      inDisplayMath = !inDisplayMath;
    }

    // Track inline math $...$ / $$...$$ on this line (very approximate; good enough for validation)
    // Count unescaped $ that are not doubled oddly. We flip parity for each top-level $.
    let temp = line.replace(/\\\$/g, ''); // ignore escaped \$
    const dollars = (temp.match(/\$/g) || []).length;
    // For each pair we enter/exit math regions. For heuristic we just skip segments between $.
    // Simpler: scan and when we see a < while "inside math" according to running parity, ignore it.

    let inInlineCode = false;
    let inMath = false;
    let j = 0;
    while (j < line.length) {
      const ch = line[j];

      if (ch === '`') {
        inInlineCode = !inInlineCode;
        j++;
        continue;
      }
      if (inInlineCode) {
        j++;
        continue;
      }

      if (ch === '$') {
        // Toggle math. Treat a `$$` pair as a single delimiter so that
        // single-line display math ($$ ... $$) protects its contents
        // (otherwise the two `$` cancel out and the math body is scanned).
        if (line[j + 1] === '$') {
          inMath = !inMath;
          j += 2;
          continue;
        }
        inMath = !inMath;
        j++;
        continue;
      }

      if (ch === '<' && !inMath && !inDisplayMath) {
        const next = line[j + 1] || '';
        const prev = line[j - 1] || '';

        // Respect backslash escape (e.g. \< or \<\< written by generators to "escape" for markdown)
        if (prev === '\\') {
          j++;
          continue;
        }

        // Skip if this looks like a valid opening of a known component used in the site
        const rest = line.slice(j + 1, j + 30);
        if (/^(YouTube|img|video|audio|source|picture|iframe|canvas|svg|div|span|code|pre|table|thead|tbody|tr|td|th|ul|ol|li|a |A |strong|em|br |hr |input|button|form|blockquote|details|summary|script|style|link|meta|head|body|html|slot|astro-island|Fragment|React\.Fragment)/i.test(rest)) {
          j++;
          continue;
        }
        // Skip closing tags </foo>
        if (next === '/') {
          j++;
          continue;
        }

        // A JSX tag name must start with a letter, `$` or `_`, so any other character
        // after a raw `<` makes the parser fail with "Unexpected character ... before name".
        // That covers everything seen in generated prose: `r << d`, `x <= 5`,
        // `health < 30%`, `p < 10^-70`, `x<3`, and `<--` arrows.
        const isDoubleShift = (next === '<' || next === '>');
        if (isDoubleShift) {
          const snippet = line.slice(j, j + 2);
          errors.push({
            file: filePath,
            line: i + 1,
            column: j + 1,
            issue: 'RAW_DOUBLE_ANGLE_BRACKET_IN_PROSE',
            message: 'Raw "<<" or ">>" in prose is parsed as JSX tag start and fails with "Unexpected character `<` before name". Wrap in backticks (e.g. `r << d`) or in $math$.',
            match: snippet,
            fix: `\`${snippet}\``,
            autofix: { length: 2, replacement: escapeAngles(snippet) }
          });
          j++; // skip the second one too
        }

        // Catch the cases that actually broke the build: <= , "x < 5", "x<3", "<-- arrows" etc.
        if (!isDoubleShift && next !== '' && !/[A-Za-z$_/!]/.test(next)) {
          const snippet = line.slice(j, j + 2);
          errors.push({
            file: filePath,
            line: i + 1,
            column: j + 1,
            issue: 'RAW_ANGLE_BRACKET_IN_PROSE',
            message: 'Raw "<" (comparison <= / < 30% / x<3, or arrow <--) in prose is parsed as JSX tag start and fails with "Unexpected character `=` (or other) before name". Escape it as &lt;, wrap the expression in backticks (e.g. `health < 30%`), or use $math$.',
            match: snippet,
            fix: `\`${snippet}\``,
            autofix: { length: 1, replacement: '&lt;' }
          });
          if (next !== ' ') {
            j++; // advance past the second char for <= or <-
          }
        }
      }
      j++;
    }
  }
  return errors;
}

function findMdxFiles(dir, files = []) {
  const entries = readdirSync(dir);

  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);

    if (stat.isDirectory()) {
      findMdxFiles(fullPath, files);
    } else if (extname(entry) === '.mdx') {
      files.push(fullPath);
    }
  }

  return files;
}

function isInCodeBlock(content, position) {
  // Check if position is inside inline code (backticks)
  const beforePos = content.substring(0, position);
  const afterPos = content.substring(position);

  // Count backticks before position on the same line
  const lineStart = beforePos.lastIndexOf('\n') + 1;
  const lineBeforePos = content.substring(lineStart, position);
  const backticksBeforeOnLine = (lineBeforePos.match(/`/g) || []).length;

  // If odd number of backticks before, we're inside inline code
  if (backticksBeforeOnLine % 2 === 1) {
    return true;
  }

  // Check if inside fenced code block (```)
  const fencedBlocksBefore = (beforePos.match(/^```/gm) || []).length;
  if (fencedBlocksBefore % 2 === 1) {
    return true;
  }

  return false;
}

function validateFile(filePath) {
  const content = readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const errors = [];

  // Frontmatter must begin on line 1. gray-matter tolerates junk before the
  // opening "---" (returning empty data), but Astro ignores such frontmatter
  // entirely and then fails the build with "title/date Required". Mirror Astro.
  if (!content.startsWith('---\n') && !content.startsWith('---\r\n')) {
    errors.push({
      file: filePath,
      line: 1,
      column: 1,
      issue: 'FRONTMATTER_NOT_AT_TOP',
      message: 'File must begin with the "---" frontmatter delimiter on line 1. Astro ignores frontmatter that is not at the very top of the file.',
      match: JSON.stringify(lines[0]),
      fix: null
    });
  }

  // Frontmatter YAML parse check (catches missing closing ---, bad colons, multiline key issues etc.)
  // This mirrors exactly what Astro's content collections + gray-matter do during `astro sync`/`build`.
  try {
    const parsed = matter(content);
    // Mirror the required fields of the blog collection schema (src/content/config.ts).
    for (const key of ['title', 'date']) {
      if (parsed.data[key] === undefined) {
        errors.push({
          file: filePath,
          line: 1,
          column: 1,
          issue: 'MISSING_REQUIRED_FRONTMATTER',
          message: `Frontmatter is missing required field "${key}" (required by the blog collection schema).`,
          match: '--- ... ---',
          fix: null
        });
      }
    }
  } catch (e) {
    errors.push({
      file: filePath,
      line: 1,
      column: 1,
      issue: 'INVALID_FRONTMATTER',
      message: `Frontmatter YAML parse failed: ${e.message || e}`,
      match: '--- ... ---',
      fix: null
    });
  }

  for (const [issueKey, issue] of Object.entries(ISSUES)) {
    const matches = [...content.matchAll(issue.pattern)];

    for (const match of matches) {
      const position = match.index;

      // Skip if already in code block
      if (isInCodeBlock(content, position)) {
        continue;
      }

      const lineNumber = content.substring(0, position).split('\n').length;
      const columnNumber = position - content.lastIndexOf('\n', position - 1);

      errors.push({
        file: filePath,
        line: lineNumber,
        column: columnNumber,
        issue: issueKey,
        message: issue.message,
        match: match[0],
        fix: issue.fix ? issue.fix(match[0]) : null,
        autofix: issue.fix
          ? { length: match[0].length, replacement: issue.fix(match[0]) }
          : null
      });
    }
  }

  // Extra structural checks (raw < etc) that the regex table doesn't cover
  errors.push(...findRawAngleBracketIssues(content, filePath));

  return errors;
}

/**
 * Applies every autofixable error in one pass and writes the file back.
 * Edits are applied right-to-left within each line so that earlier columns
 * stay valid as the line grows. Returns the number of repairs made.
 */
function fixFile(filePath, errors) {
  const fixable = errors.filter((e) => e.autofix);
  if (fixable.length === 0) {
    return 0;
  }

  const lines = readFileSync(filePath, 'utf-8').split('\n');
  const byLine = new Map();
  for (const error of fixable) {
    if (!byLine.has(error.line)) {
      byLine.set(error.line, []);
    }
    byLine.get(error.line).push(error);
  }

  for (const [lineNumber, lineErrors] of byLine) {
    let line = lines[lineNumber - 1];
    if (line === undefined) {
      continue;
    }
    for (const error of lineErrors.sort((a, b) => b.column - a.column)) {
      const start = error.column - 1;
      const { length, replacement } = error.autofix;
      line = line.slice(0, start) + replacement + line.slice(start + length);
    }
    lines[lineNumber - 1] = line;
  }

  writeFileSync(filePath, lines.join('\n'));
  return fixable.length;
}

function main() {
  const shouldFix = process.argv.includes('--fix');
  const contentDir = join(process.cwd(), 'src/content/blog');
  const mdxFiles = findMdxFiles(contentDir);

  console.log(`Validating ${mdxFiles.length} MDX files...\n`);

  if (shouldFix) {
    let fixedFiles = 0;
    let fixedIssues = 0;
    for (const file of mdxFiles) {
      const repairs = fixFile(file, validateFile(file));
      if (repairs > 0) {
        fixedFiles++;
        fixedIssues += repairs;
        console.log(`  fixed ${repairs} issue(s) in ${file}`);
      }
    }
    console.log(
      fixedIssues === 0
        ? 'Nothing to auto-fix.\n'
        : `\nAuto-fixed ${fixedIssues} issue(s) in ${fixedFiles} file(s). Re-validating...\n`
    );
  }

  let totalErrors = 0;
  const fileErrors = [];

  for (const file of mdxFiles) {
    const errors = validateFile(file);
    if (errors.length > 0) {
      totalErrors += errors.length;
      fileErrors.push({ file, errors });
    }
  }

  if (totalErrors === 0) {
    console.log('✓ All MDX files are valid!\n');
    process.exit(0);
  }

  console.error(
    shouldFix
      ? `✗ ${totalErrors} issue(s) in ${fileErrors.length} file(s) have no automatic repair:\n`
      : `✗ Found ${totalErrors} issue(s) in ${fileErrors.length} file(s) (run \`npm run fix:mdx\` to repair the mechanical ones):\n`
  );

  for (const { file, errors } of fileErrors) {
    console.error(`\n${file}:`);
    for (const error of errors) {
      console.error(`  Line ${error.line}:${error.column} - ${error.message}`);
      console.error(`    Found: ${error.match}`);
      if (error.fix) {
        console.error(`    Fix: ${error.fix}`);
      }
    }
  }

  console.error('\n');
  process.exit(1);
}

main();
