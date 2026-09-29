# FinAI LLM Integration Addendum

Extends the existing web reference without changing its visual baseline.

- Keep the existing dashboard/sidebar/AI visual design unchanged.
- Use Streamlit Custom Components v2 for bidirectional communication.
- UI-only open/close/sidebar actions remain client-side and do not rerun Python.
- Only Send/Enter submits a chat event to Python.
- Python reads `OPENROUTER_API_KEY` from Streamlit Secrets; the key is never sent to the browser.
- Primary model: `google/gemma-3-12b-it:free`.
- On HTTP 429, retry once with `qwen/qwen3-4b:free`.
- LLM errors are rendered inside the existing AI panel, not below the dashboard.
- Conversation history is maintained in Streamlit session state and rendered inside the existing AI body.
- Do not introduce `st.chat_input`, `st.dialog`, Streamlit columns, or extra UI outside the baseline component.
