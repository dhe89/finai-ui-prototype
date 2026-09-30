import streamlit as st
import streamlit.components.v2 as components
from pathlib import Path

st.set_page_config(
    page_title="FinAI — Financial Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

FRONTEND = Path(__file__).parent / "finai_ui" / "frontend"

# The UI is a single Streamlit Custom Component V2.
# Pages are HTML fragments loaded by JavaScript into #main-content.
# No iframe-per-page and no query-parameter navigation.
components.component(
    "finai_ui",
    html=FRONTEND / "index.html",
    css=FRONTEND / "css" / "main.css",
    js=FRONTEND / "js" / "app.js",
    width="stretch",
    height=1500,
)
