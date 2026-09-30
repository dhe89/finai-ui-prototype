# FinAI UI Prototype — V3

This version keeps the current Streamlit Components V2 architecture while adopting the visual language of `app_fix_chat_v6.py`.

## Architecture
- One Streamlit Components V2 component.
- No nested iframe and no page-created component.
- `index.html` is the shell only.
- Sidebar, header and AI chat are separate layout fragments.
- Dashboard pages are separate HTML fragments under `frontend/pages/`.
- `app.py` owns session state and the chat event gateway.
- `main.css` owns the visual system and responsive layout.
- `app.js` owns navigation, responsive mode, sidebar and AI interactions.

## Visual baseline
- Deep green sidebar `#005642`.
- Lime accent `#b7f51d`.
- Soft financial dashboard background `#f4f7f5`.
- Rounded white cards with subtle shadows.
- Two-column KPI layout, matching the approved visual model.
- AI assistant as a right-side desktop panel and full-screen mobile overlay.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
