# Taixr Skills Improvement Guide

Based on learnings from Claude Design System Prompt, this document outlines 5 key improvements to apply across all taixr skills.

---

## 1. Structured Workflow (6-Step Process)

Add this workflow section to all taixr skills after the "When to Use" section:

```markdown
## Workflow

Follow this 6-step process for all content creation:

### 1. Understand User Needs
- Ask clarifying questions for new/ambiguous work
- Understand the output type, fidelity, constraints
- Identify target audience and context
- **For complex projects: Ask 10+ questions before starting**
- **For simple tweaks: Skip questions if user provided everything**

### 2. Explore Resources
- Check for existing design systems, templates, or reference materials
- Read relevant examples and patterns
- Identify reusable components or assets
- **Never start from scratch if context exists**

### 3. Plan
- Create a todo list for multi-step work
- Identify which components/scenes are needed
- Determine the visual system upfront (colors, fonts, layouts)
- Document approach before building

### 4. Build
- Create folder structure
- Build components incrementally
- Follow established patterns from step 2
- **Keep files under 1000 lines** - split into smaller components if needed

### 5. Verify
- Preview the output
- Check for errors and quality issues
- Test key functionality
- Iterate based on findings

### 6. Summarize
- **EXTREMELY BRIEFLY** - caveats and next steps only
- No verbose recaps or bullet point lists
- 1-2 sentences maximum
```

---

## 2. Question-Asking Guidelines

Add this section after "Required Inputs":

```markdown
## Asking Questions

**When to ask questions:**
- ✅ New projects with ambiguous requirements
- ✅ Complex multi-scene/multi-slide content
- ✅ When design context is unclear
- ❌ Small tweaks or follow-ups
- ❌ When user provided complete specifications

**What to ask (for complex projects):**
1. **Confirm starting point**: "Do you have existing design assets, templates, or reference materials?"
2. **Clarify variations**: "How many variations would you like? Which aspects should vary?"
3. **Understand priorities**: "What matters most - visuals, content flow, or interactions?"
4. **Explore style preferences**: "Do you want options using existing patterns, novel visuals, or a mix?"
5. **Identify tweaks needed**: "What aspects would you like to be adjustable?"
6. **Ask 4+ problem-specific questions** based on the content type

**Minimum questions for complex projects: 10+**

**One-round rule**: Ask focused questions once, then proceed. Don't ask repeatedly.
```

---

## 3. Content Quality Guidelines

Add this section before "Limitations":

```markdown
## Content Quality Standards

### Do Not Add Filler Content
- Every element must earn its place
- No placeholder text or dummy sections just to fill space
- If a section feels empty, solve it with layout/composition, not invented content
- **Ask before adding material** - don't unilaterally add sections

### Create a System Upfront
After exploring design assets, vocalize the system you'll use:
- For presentations: Choose layouts for headers, content, images
- For videos: Define scene types and transitions
- Use the system to introduce intentional variety and rhythm
- Commit to 1-2 background colors max for presentations

### Use Appropriate Scales
- **Slides (1920x1080)**: Text never smaller than 24px, ideally much larger
- **Print documents**: 12pt minimum
- **Mobile mockups**: Hit targets never less than 44px
- **Videos**: Ensure text is readable at target resolution

### Avoid AI Slop Tropes
**Never use these patterns:**
- ❌ Aggressive gradient backgrounds
- ❌ Emoji unless explicitly part of brand (use placeholders instead)
- ❌ Rounded corners with left-border accent color containers
- ❌ Drawing imagery using SVG (use placeholders, ask for real materials)
- ❌ Overused fonts: Inter, Roboto, Arial, Fraunces, system fonts
- ❌ Generic stock photo aesthetics
- ❌ Unnecessary iconography or "data slop" (meaningless numbers/stats)

**Do use:**
- ✅ Bold, specific aesthetic choices
- ✅ Advanced CSS (text-wrap: pretty, CSS grid, modern effects)
- ✅ Placeholders when you don't have real assets
- ✅ Intentional visual rhythm and variety
- ✅ Less is more - one thousand no's for every yes
```

---

## 4. File Management Best Practices

Add this section to "Technical Details":

```markdown
## File Management

### File Size Limits
- **CRITICAL**: Avoid files larger than 1000 lines
- Split large files into smaller components
- Import components into a main file
- Makes files easier to manage and edit

### Version Management
- When making significant revisions, copy the file first
- Use version suffixes: `video-v1.tsx`, `video-v2.tsx`, `video-v3.tsx`
- Preserves old versions for comparison
- Never overwrite working versions

### Descriptive Naming
- Use clear, descriptive filenames
- Examples: `ProductDemo.tsx`, `ChinesePoetry.tsx`, `FinancialReport.pptx`
- Avoid generic names like `output.mp4`, `video.tsx`, `presentation.pptx`

### Persistent State (for videos/presentations)
- Store playback position in localStorage
- Update on every slide/time change
- Re-read on page load
- Makes refresh-without-losing-place possible
```

---

## 5. Technical Standards

Add/update these sections in "Technical Details":

```markdown
## Technical Standards

### Dependency Management
**CRITICAL**: Always pin exact versions with integrity hashes for CDN dependencies.

**React + Babel (for HTML-based outputs):**
```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" 
        integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" 
        crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" 
        integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" 
        crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" 
        integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" 
        crossorigin="anonymous"></script>
```

**Never use unpinned versions** (e.g., `react@18`) or omit integrity attributes.

### Style Object Naming
**CRITICAL**: When defining global-scoped style objects, give them SPECIFIC names.

❌ **NEVER do this:**
```typescript
const styles = { ... };  // Will break with multiple components
```

✅ **Always do this:**
```typescript
const productDemoStyles = { ... };
const poetrySceneStyles = { ... };
// OR use inline styles
```

**Why**: Multiple components with `const styles = {...}` cause name collisions and breakages.

### Component Scoping (Multiple Babel Scripts)
**CRITICAL**: Each `<script type="text/babel">` gets its own scope.

To share components between files, export to `window`:

```javascript
// At the end of components.tsx:
Object.assign(window, {
  Terminal, Line, Spacer,
  Gray, Blue, Green, Bold,
  // ... all components that need to be shared
});
```

This makes components globally available to other scripts.

### Script Import Order
**CRITICAL**: Register listeners BEFORE announcing availability.

❌ **Wrong order:**
```javascript
window.parent.postMessage({type: '__ready'}, '*');
window.addEventListener('message', handler);  // Too late!
```

✅ **Correct order:**
```javascript
window.addEventListener('message', handler);  // Register first
window.parent.postMessage({type: '__ready'}, '*');  // Then announce
```

### Python Environment (for Python-based skills)
```bash
source ~/miniconda3/etc/profile.d/conda.sh && conda activate skills
```

Always activate the `skills` conda environment before running Python code.
```

---

## Implementation Checklist

For each taixr skill, apply these updates:

### All Skills
- [ ] Add 6-step workflow section
- [ ] Add question-asking guidelines
- [ ] Add content quality standards
- [ ] Add file management section
- [ ] Update technical standards

### HTML/React-based Skills (taixr-remotion, taixr-three-js)
- [ ] Add pinned React/Babel versions with integrity hashes
- [ ] Add style object naming warnings
- [ ] Add component scoping guidelines
- [ ] Add script import order guidelines

### Python-based Skills (taixr-ppt, taixr-manim, taixr-diagrams)
- [ ] Add conda environment activation reminder
- [ ] Add file size warnings for generated code
- [ ] Add version management patterns

### Presentation Skills (taixr-ppt, taixr-remotion)
- [ ] Add "no filler content" emphasis
- [ ] Add AI slop tropes to avoid
- [ ] Add appropriate scale guidelines (24px+ for slides)
- [ ] Add "create system upfront" guidance

---

## Priority Order

Apply improvements in this order:

1. **taixr-remotion** (most complex, HTML/React-based)
2. **taixr-ppt** (most used, Python-based)
3. **taixr-manim** (technical, Python-based)
4. **taixr** (router skill, needs workflow clarity)
5. **taixr-diagrams** (simpler, fewer changes needed)
6. **taixr-excalidraw** (simpler, fewer changes needed)
7. **taixr-three-js** (HTML/React-based)
8. **taixr-video-generation** (FFmpeg-based, simpler)
9. **taixr-audio** (audio-only, simpler)

---

## Key Principles from Claude Design Prompt

### Workflow Philosophy
- "Understand → Explore → Plan → Build → Verify → Summarize EXTREMELY BRIEFLY"
- Ask questions upfront, not during execution
- One round of focused questions is usually right
- Skip questions for small tweaks or when user gave everything

### Content Philosophy
- "Do not add filler content" - every element must earn its place
- "Ask before adding material" - user knows their audience better
- "Create a system upfront" - vocalize the visual system before building
- "Less is more" - one thousand no's for every yes

### Technical Philosophy
- Pin exact versions with integrity hashes
- Unique names for style objects (never `const styles = {...}`)
- Split files over 1000 lines into smaller components
- Register listeners before announcing availability

### Quality Philosophy
- Avoid AI slop tropes (gradients, emoji, rounded corners with accents)
- Use appropriate scales (24px+ for slides, 44px+ for mobile)
- Advanced CSS is your friend (text-wrap: pretty, CSS grid)
- Placeholders are better than bad attempts at real things

---

## Next Steps

1. Review this document
2. Start with taixr-remotion (highest priority)
3. Apply all 5 improvements systematically
4. Test each updated skill
5. Move to next skill in priority order
6. Update skill documentation as you go
