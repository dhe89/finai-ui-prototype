from pathlib import Path
import streamlit as st
import streamlit.components.v2 as components

st.set_page_config(
    page_title="FinAI — Financial Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).parent / "finai_ui" / "frontend"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# Keep HTML/CSS/JS in separate files. Python only assembles trusted assets
# into ONE Streamlit V2 component. V2 is not iframe-based.
index_html = read_text(BASE / "index.html")
css = read_text(BASE / "css" / "main.css")
js = read_text(BASE / "js" / "app.js")
sidebar_html = read_text(BASE / "layout" / "sidebar.html")
header_html = read_text(BASE / "layout" / "header.html")
ai_html = read_text(BASE / "layout" / "ai_chat.html")

page_names = ["kinerja", "financial_report", "data_detail", "setting"]
pages = {name: read_text(BASE / "pages" / f"{name}.html") for name in page_names}

# Chat state lives in the Streamlit session, not in a new iframe/component.
if "finai_chat_history" not in st.session_state:
    st.session_state.finai_chat_history = []
if "finai_response_version" not in st.session_state:
    st.session_state.finai_response_version = 0


def answer_question(message: str) -> str:
    """Temporary local gateway.

    Replace this function with llm_gateway.ask(...) when the real provider
    credentials and business-data retrieval layer are ready.
    """
    q = message.lower()
    if "net profit" in q or "laba" in q:
        return (
            "Net Profit bulan ini 699,1, turun dari 812,4 bulan lalu atau sekitar "
            "-13,9%. Dari dashboard, Revenue turun menjadi 1.255,2 sementara "
            "Operating Expense naik menjadi 556,1 dan CKPN menjadi 207,9. "
            "Ketiga perubahan tersebut adalah data yang perlu dilihat lebih lanjut "
            "untuk menentukan driver penurunan laba."
        )
    return (
        "Pertanyaan sudah diterima. Untuk saat ini gateway LLM masih menggunakan "
        "respons lokal prototype. Struktur chat, history, sidebar, dan halaman "
        "sudah dipisahkan sehingga integrasi LLM berikutnya tidak perlu mengubah UI."
    )


def on_chat_submit():
    event = st.session_state.get("finai_main", {}).get("chat_submit")
    if not event or not event.get("message"):
        return
    message = str(event["message"]).strip()
    st.session_state.finai_chat_history.append({"role": "user", "content": message})
    answer = answer_question(message)
    st.session_state.finai_chat_history.append({"role": "assistant", "content": answer})
    st.session_state.finai_response_version += 1


finai_component = components.component(
    "finai_ui",
    html=index_html,
    css=css,
    js=js,
    isolate_styles=True,
)

finai_component(
    key="finai_main",
    width="stretch",
    height="stretch",
    data={
        "sidebar_html": sidebar_html,
        "header_html": header_html,
        "ai_html": ai_html,
        "pages": pages,
        "chat_history": st.session_state.finai_chat_history,
        "response_version": st.session_state.finai_response_version,
    },
    on_chat_submit_change=on_chat_submit,
)
