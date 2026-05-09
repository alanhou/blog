# ArXiv Blog Post Generation Improvements

Based on the ljg-skill-paper approach, we've upgraded the arxiv blog post generation to create more insightful, readable content.

## Key Changes

### 1. **Added "The Gap" Section with Logic Topology**
- **Before**: Jumped straight to abstract summary
- **After**: Start by identifying the research frontier and the specific gap being filled
- Includes ASCII diagram showing: Problem → Assumption → Method → Evidence → Conclusion

### 2. **Sharpened "The Increment"**
- **Before**: Generic "Key Contributions" list
- **After**: One bold sentence capturing "before → after" shift, followed by detailed mechanism explanation

### 3. **Added Core Mechanism Visualization**
- **Before**: Text-only method description
- **After**: ASCII diagram showing internal structure (components, data flow, operations)
- This is the "X-ray" of how the method works inside

### 4. **Added Structural Metaphor (核喻)**
- **Before**: Abstract technical descriptions
- **After**: Load-bearing analogy where method components map to familiar concepts
- Goal: Reader can retell the method in their own words after reading

### 5. **Added "Framework Shift" Section (Napkin Sketch)**
- **Before**: No visual comparison of approaches
- **After**: Side-by-side ASCII diagram comparing mainstream approach vs this paper's approach
- Shows gestalt shift in thinking, not just feature comparison

### 6. **Upgraded to "Expert Assessment"**
- **Before**: Generic "Implications and Future Directions"
- **After**: Honest, calibrated review covering:
  - Problem choice (real gap or manufactured?)
  - Method maturity (clever or brute force?)
  - Experimental integrity (fair baselines? red flags?)
  - Writing quality (where did authors cut corners?)
  - One-line verdict: strong accept / weak accept / borderline / weak reject / strong reject

### 7. **Changed "Takeaways" Focus**
- **Before**: Generic insights and conclusions
- **After**: Specific ideas/techniques/framings a practitioner can steal and apply elsewhere
- Allows "none" if there's nothing concrete (honesty > forced insights)

### 8. **ASCII Art Constraints**
- Only pure ASCII: `+ - | / \ > < v ^ * = ~ . : # [ ] ( ) _`
- **Banned** Unicode box drawing: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╔ ╗ ╚ ╝ ● ○ ■ □ ◆ ◇ ▼ ▲ ► ◄ → ← ↑ ↓`

### 9. **Automatic Chinese Line Break Fixing**
- Added to `sanitize_mdx()`: automatically inserts line breaks after Chinese periods (。) in `:::zh` sections
- Prevents horizontal scrolling in rendered Chinese paragraphs

### 10. **MDX Curly Brace Escaping**
- **Problem**: Mathematical set notation like `{-1,1}^n` or `{1,...,n}` causes MDX build failures because MDX tries to parse curly braces as JSX expressions
- **Solution**: 
  - Added explicit instruction in the prompt to escape curly braces in mathematical notation (use `\{` and `\}`)
  - Added automatic escaping in `sanitize_mdx()` as a safety net
  - Prevents `[@mdx-js/rollup] Could not parse expression with acorn` errors
- **Example**: `{-1,1}^n` → `\{-1,1\}^n`, `{1,...,n}` → `\{1,...,n\}`

### 11. **Tone Shift**
- **Before**: Academic, comprehensive coverage
- **After**: Conversational, like explaining to a colleague over coffee
- Focus on **what the paper means** and **why it matters**, not just what it says

## New Structure

```
:::en
## The Gap
[Frontier + specific gap + ASCII logic topology]

## The Increment
**One sentence**: [before → after]
### Core Mechanism
[Explanation + ASCII internals diagram + structural metaphor]
### Key Concepts
[1-3 Feynman-style concept explanations]

## Framework Shift
[ASCII before/after comparison + one-sentence shift summary]

## Expert Assessment
[Honest evaluation + verdict]

## Takeaways
[Concrete, transferable insights]
:::

:::zh
[Parallel Chinese composition with same structure]
:::
```

## Implementation

Updated files:
- `/Users/alan/workspace/alanhou/blog/scripts/fetch_arxiv.py`
  - `generate_blog_post()`: New prompt incorporating ljg-paper principles
  - `sanitize_mdx()`: Added Chinese line break fixing

## Testing

To test the new prompt:
```bash
cd /Users/alan/workspace/alanhou/blog/scripts
python3 fetch_arxiv.py
```

The next batch of arxiv posts will use the improved structure.

## Philosophy

The old approach treated papers as **information to summarize**.
The new approach treats papers as **ideas to understand and evaluate**.

Key question shift:
- Old: "What does this paper say?"
- New: "What gap does this fill, what's actually new, and is it worth my attention?"
