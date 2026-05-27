#!/usr/bin/env node

/**
 * Validates MDX files for common syntax issues that break builds
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';

const ISSUES = {
  UNESCAPED_ANGLE_BRACKETS: {
    pattern: /<\*+>/g,
    message: 'Unescaped angle brackets with asterisks (e.g., <*>, <**>) - wrap in backticks',
    fix: (match) => `\`${match}\``
  }
};

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
