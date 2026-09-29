# FinAI Streamlit UI Prototype — Fixed

Prototype UI only; no LLM/backend.

The UI is rendered as one self-contained HTML component so CSS/JS interactions are not broken by Streamlit's DOM rendering.

## Features
- Desktop left sidebar collapse: full menu -> icon rail.
- Desktop AI sidebar close/open using X and AI button in header.
- Main area automatically expands when either sidebar is closed.
- Mobile left menu becomes a drawer.
- Mobile AI opens/closes from the header AI button and X, matching the requested behavior.
- Responsive dashboard/table/cards.

## Streamlit Cloud
Set the main file to `app.py`.
