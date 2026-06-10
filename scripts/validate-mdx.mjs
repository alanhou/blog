#!/usr/bin/env node

/**
 * Validates MDX files for common syntax issues that break builds
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';
import matter from 'gray-matter';

const ISSUES = {
  UNESCAPED_ANGLE_BRACKETS: {
    pattern: /<\*+>/g,
    message: 'Unescaped angle brackets with asterisks (e.g., <*>, <**>) - wrap in backticks',
    fix: (match) => `\`${match}\``
  }
};

// Additional runtime checks for raw < that break the MDX/JSX parser even if not matching the above regex.
// These are things like bit-shift notation (r << d), generic-like <T>, or plain comparisons in prose.
function findRawAngleBracketIssues(content, filePath) {
  const errors = [];
  const lines = content.split('\n');
  let inFence = false;
  let fenceMarker = '';
  let mathDollarParity = 0; // track $...$ and $$...$$ (simple heuristic)

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
        // toggle math (handles both $ and $$ because we toggle per $)
        inMath = !inMath;
        j++;
        continue;
      }

      if (ch === '<' && !inMath) {
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

        // Only flag the patterns proven to reliably break the MDX JSX parser with the exact error
        // "Unexpected character `<` before name":
        //   - <<   (the original crash: "r << d" in prose)
        //   - >>   (symmetric, or diagram arrows that leak out of code)
        // We are conservative here: many "word < word" and math-in-text still compile thanks to
        // remark-math + how @astrojs/mdx + the JSX recovery works in paragraphs. Only double-angle
        // is a guaranteed hard failure when not protected.
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
            fix: `\`${snippet}\``
          });
          j++; // skip the second one too
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

  // Frontmatter YAML parse check (catches missing closing ---, bad colons, multiline key issues etc.)
  // This mirrors exactly what Astro's content collections + gray-matter do during `astro sync`/`build`.
  try {
    matter(content);
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
        fix: issue.fix ? issue.fix(match[0]) : null
      });
    }
  }

  // Extra structural checks (raw < etc) that the regex table doesn't cover
  errors.push(...findRawAngleBracketIssues(content, filePath));

  return errors;
}

function main() {
  const contentDir = join(process.cwd(), 'src/content/blog');
  const mdxFiles = findMdxFiles(contentDir);

  console.log(`Validating ${mdxFiles.length} MDX files...\n`);

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

  console.error(`✗ Found ${totalErrors} issue(s) in ${fileErrors.length} file(s):\n`);

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
