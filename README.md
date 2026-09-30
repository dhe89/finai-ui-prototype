# FinAI UI Prototype V1

Frontend-first Streamlit prototype.

## Architecture

- `app.py` — Streamlit host only.
- `finai_ui/frontend/index.html` — application shell.
- `finai_ui/frontend/pages/*.html` — page fragments.
- `finai_ui/frontend/layout/*.html` — persistent UI components.
- `finai_ui/frontend/css/*.css` — styles.
- `finai_ui/frontend/js/*.js` — navigation and UI behaviour.

There is intentionally no LLM integration in V1.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Navigation

The frontend uses one application shell and loads page fragments into `#main-content`.
It does not create an iframe for every page and does not reload Streamlit for navigation.
