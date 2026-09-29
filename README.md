# FinAI — Overlay LLM Integration v2

Built directly from `finai_streamlit_overlay_v1`. The dashboard/sidebar/overlay visual baseline is preserved.

This version uses Streamlit Custom Components v2 for bidirectional communication so chat stays inside the existing AI overlay.

## Secret
`OPENROUTER_API_KEY = "sk-or-v1-..."` in Streamlit Secrets.

## Models
Primary: `google/gemma-3-12b-it:free`
Fallback on HTTP 429: `qwen/qwen3-4b:free`
