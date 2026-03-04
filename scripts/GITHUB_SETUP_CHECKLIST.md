# GitHub Actions Setup Checklist

## ✅ Code Changes Complete
- [x] Updated `fetch_arxiv.py` with dual provider support
- [x] Added `anthropic` to pip install in `.github/workflows/arxiv.yml`
- [x] Updated README.md with provider instructions

## 🔧 GitHub Secrets Required

Go to your repository → Settings → Secrets and variables → Actions

### For Claude (Anthropic API)
```
LLM_API_KEY = sk-ant-api03-...
LLM_MODEL_NAME = claude-sonnet-4-6
LLM_BASE_URL = (leave empty or set custom endpoint)
```

### For OpenAI-compatible APIs
```
LLM_API_KEY = your-openai-key
LLM_MODEL_NAME = gpt-4
LLM_BASE_URL = https://api.openai.com/v1
```

## 📋 What the Workflow Does

1. **Triggers**: Every 8 hours or manually via workflow_dispatch
2. **Installs**: `requests`, `openai`, `anthropic`, `manim` + system deps (ffmpeg, cairo)
3. **Runs**: `python scripts/fetch_arxiv.py`
4. **Commits**: New MDX files and visuals to main branch
5. **Deploys**: Rebuilds and deploys site if new posts were added

## 🧪 Testing

### Test locally first:
```bash
pip install requests openai anthropic manim
export LLM_API_KEY="your-key"
export LLM_MODEL_NAME="claude-sonnet-4-6"
# export LLM_BASE_URL="..." # optional for Claude
python scripts/fetch_arxiv.py
```

### Test on GitHub:
1. Go to Actions tab
2. Select "Fetch Arxiv Papers" workflow
3. Click "Run workflow" → "Run workflow"
4. Monitor the logs

## ⚠️ Important Notes

- **LLM_BASE_URL is optional for Claude** - only set it if using a custom endpoint
- **LLM_BASE_URL is required for OpenAI** - must be set to your API endpoint
- The script auto-detects provider from model name (starts with "claude" = Anthropic)
- Max tokens: 8192 for blog posts (suitable for Sonnet 4.5+)
