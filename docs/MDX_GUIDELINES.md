# MDX Content Guidelines

## Common Pitfalls

### 1. Angle Brackets with Special Characters

**Problem**: MDX interprets `<...>` as JSX tags. Patterns like `<*>`, `<**>`, or `<variable>` will cause build failures.

**Solution**: Wrap them in backticks to treat as inline code:

```markdown
❌ Bad: "Node <*> failed"
✅ Good: "Node `<*>` failed"

❌ Bad: template "Error on <**> at <*>"
✅ Good: template "Error on `<**>` at `<*>`"
```

### 2. When This Happens

Common in technical content:
- Log templates with placeholders
- Generic type parameters
- Placeholder syntax in examples
- Variable notation in algorithms

### 3. Validation

Run validation before committing:

```bash
npm run validate
```

This checks all MDX files for common syntax issues.

### 4. Build Process

The build automatically validates MDX files:

```bash
npm run build
# Runs: validate → generate-covers → astro build
```

If validation fails, the build stops with clear error messages showing:
- File path
- Line and column number
- The problematic pattern
- Suggested fix

## Best Practices

1. **Always wrap technical placeholders in backticks** - Treat `<*>`, `<variable>`, etc. as code
2. **Test locally before pushing** - Run `npm run validate` or `npm run build`
3. **Review generated content** - When using automated blog generation, check for angle bracket patterns
4. **Use code blocks for examples** - Fenced code blocks (```) automatically escape content

## Automated Prevention

The arxiv skill has been updated to remind about this issue when generating blog posts. The validation script catches these errors before they reach the build stage.
