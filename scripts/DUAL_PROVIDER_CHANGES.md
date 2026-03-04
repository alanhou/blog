# Dual Provider Support Changes

## Summary

Updated `fetch_arxiv.py` to support both Claude (Anthropic API) and OpenAI-compatible APIs.

## Key Changes

### 1. Provider Detection
- Detects provider based on model name (models starting with "claude" use Anthropic API)
- Returns `(client, model, provider)` tuple from `get_llm_client()`

### 2. Unified LLM Call Function
Added `call_llm()` function that handles both APIs:
- **Anthropic**: Uses `client.messages.create()` with `max_tokens` parameter
- **OpenAI**: Uses `client.chat.completions.create()` (no max_tokens needed)

### 3. Max Tokens Configuration
- `select_papers()`: 1024 tokens (just returning paper numbers)
- `generate_blog_post()`: 8192 tokens (full bilingual content)
- `generate_manim_code()`: 2048 tokens (code generation)

### 4. System Message Handling
For Manim code generation:
- **OpenAI**: Supports separate system/user messages
- **Anthropic**: Prepends system prompt to user message (Anthropic doesn't support system messages the same way)

## Environment Variables

### For Claude (Anthropic)
```bash
export LLM_API_KEY="sk-ant-..."
export LLM_MODEL_NAME="claude-sonnet-4-6"
# LLM_BASE_URL is optional (for custom endpoints)
```

### For OpenAI-compatible APIs
```bash
export LLM_API_KEY="your-key"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL_NAME="gpt-4"
```

## Dependencies

Updated requirements:
```bash
pip install requests openai anthropic manim
```

## Testing

To test the changes:
1. Install dependencies: `pip install requests openai anthropic`
2. Set environment variables for your chosen provider
3. Run: `python scripts/fetch_arxiv.py`
