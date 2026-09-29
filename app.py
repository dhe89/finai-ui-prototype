import json
import requests
import streamlit as st

# ============================================================
# FinAI — Financial Intelligence
# Native Streamlit version
# - Responsive desktop/mobile via native Streamlit layout
# - Sidebar via st.sidebar
# - AI Assistant via st.dialog
# - Chat connected directly to OpenRouter
# - API key comes ONLY from Streamlit Secrets
# ============================================================

st.set_page_config(
    page_title="FinAI — Financial Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemma-3-12b-it:free"

# Demo financial data — kept from the previous UI prototype.
FINANCIAL_DATA = {
    "period": "September 2026",
    "metrics": {
        "Total Assets": "190,510.7",
        "Total Credit": "104,549.2",
        "Total DPK": "158,545.5",
        "Net Profit": "699.1",
    },
    "rows": [
        ("ASSET", None, None, None, None, None),
        ("Total Asset", "173,731.1", "194,349.9", "190,510.7", "192,871.1", "98.8%"),
        ("Total Credit", "122,208.6", "106,885.6", "104,549.2", "101,808.3", "102.7%"),
        ("Total Investment", "76,318.9", "79,825.3", "79,599.7", "80,855.6", "98.4%"),
        ("FUNDING", None, None, None, None, None),
        ("Total DPK", "146,764.4", "163,153.8", "158,545.5", "160,414.1", "98.8%"),
        ("Total Other Funding", "4,460.0", "4,980.0", "5,045.0", "5,040.0", "100.1%"),
        ("Low Cost Funding %", "88.3", "78.0", "77.4", "81.0", "95.6%"),
        ("PROFITABILITY", None, None, None, None, None),
        ("Revenue", "1,373.4", "1,274.2", "1,255.2", "1,378.0", "91.1%"),
        ("Operating Expense", "482.9", "461.8", "556.1", "535.4", "103.9%"),
        ("CKPN", "210.9", "106.9", "207.9", "198.0", "105.0%"),
        ("Net Profit", "890.5", "812.4", "699.1", "727.1", "96.1%"),
        ("ASSET QUALITY", None, None, None, None, None),
        ("NPL Ratio", "3.6", "0.0", "4.2", "2.2", "190.9%"),
        ("CKPN Coverage", "107.0", "114.3", "115.9", "110.0", "105.4%"),
    ],
}

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown(
    """
<style>
/* Global */
.stApp {
    background: #f4f7f5;
    color: #18211f;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

:root {
    --fin-green: #005642;
    --fin-green-2: #08735d;
    --fin-lime: #b7f51d;
    --fin-bg: #f4f7f5;
    --fin-line: #e7ece9;
    --fin-muted: #8d9793;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--fin-green);
}

section[data-testid="stSidebar"] > div {
    background: var(--fin-green);
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 4px 0 28px 4px;
}

.brand-mark {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: var(--fin-lime);
    color: var(--fin-green);
    display: grid;
    place-items: center;
    font-weight: 900;
}

.brand-name {
    font-size: 20px;
    font-weight: 800;
}

.sidebar-section {
    color: #9ac3b8;
    font-size: 9px;
    letter-spacing: 1.3px;
    margin-top: 28px;
    margin-bottom: 8px;
}

.sidebar-status {
    color: #d2e7e1;
    font-size: 9px;
    margin-top: 8px;
}

.sidebar-dot {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--fin-lime);
    margin-right: 5px;
}

/* Header */
.desktop-appbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.desktop-app-name {
    font-size: 13px;
    font-weight: 800;
    color: #65716c;
}

.ai-open-button button {
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    padding: 0 !important;
    background: #ffffff !important;
    color: var(--fin-green) !important;
    border: 1px solid #e4e9e6 !important;
    box-shadow: 0 4px 12px #0000000d !important;
}

/* Hero */
.hero {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 22px;
}

.eyebrow {
    color: #a0aaa6;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
}

.page-title {
    font-size: clamp(32px, 4vw, 48px);
    line-height: 1.05;
    font-weight: 800;
    margin: 4px 0 0;
}

.subtitle {
    color: #9aa49f;
    font-size: 12px;
    margin-top: 8px;
}

.period-pill {
    background: #eff6d9;
    color: #6c7d42;
    border-radius: 22px;
    padding: 11px 16px;
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #edf0ef;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 7px 20px #1e41370b;
    min-height: 125px;
}

.metric-label {
    color: #909b97;
    font-size: 11px;
}

.metric-value {
    font-size: 26px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-change {
    color: #a78282;
    font-size: 9px;
    margin-top: 6px;
}

/* Section cards */
.fin-card {
    background: #ffffff;
    border: 1px solid #edf0ef;
    border-radius: 18px;
    box-shadow: 0 7px 20px #1e41370b;
    overflow: hidden;
}

.card-header {
    padding: 18px 18px 13px;
}

.card-title {
    font-size: 15px;
    font-weight: 800;
}

.card-caption {
    color: #9ba5a1;
    font-size: 9px;
    margin-top: 4px;
}

.switch-pill {
    background: #f0f6df;
    color: #718044;
    border-radius: 18px;
    padding: 8px 12px;
    font-size: 9px;
    font-weight: 700;
}

/* Table */
.fin-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
}

.fin-table th {
    color: #a1aaa7;
    font-weight: 600;
    padding: 10px 12px;
    text-align: right;
    border-top: 1px solid var(--fin-line);
}

.fin-table th:first-child,
.fin-table td:first-child {
    text-align: left;
}

.fin-table td {
    color: #737d79;
    padding: 11px 12px;
    text-align: right;
    border-top: 1px solid #edf0ef;
}

.fin-table tr.section td {
    background: #eef5ef;
    color: #64806f;
    font-size: 9px;
    letter-spacing: 1.5px;
    font-weight: 800;
    text-align: left;
    padding: 8px 12px;
}

/* Bottom cards */
.kpi-card {
    background: #ffffff;
    border: 1px solid #edf0ef;
    border-radius: 18px;
    padding: 17px;
    box-shadow: 0 7px 20px #1e41370b;
}

.kpi-title {
    font-size: 13px;
    font-weight: 800;
}

.kpi-caption {
    color: #9ba5a1;
    font-size: 9px;
    margin-top: 4px;
}

.kpi-row {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    font-size: 10px;
}

.kpi-label {
    color: #68736f;
}

.kpi-value {
    font-size: 11px;
    font-weight: 800;
}

/* AI dialog */
div[data-testid="stDialog"] {
    background: #ffffff;
}

div[data-testid="stDialog"] > div {
    border-radius: 18px;
}

.ai-dialog-title {
    font-size: 19px;
    font-weight: 800;
    color: #18211f;
}

.ai-dialog-status {
    color: #8d9793;
    font-size: 9px;
    margin-top: 4px;
}

.ai-dialog-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--fin-green-2);
    margin-right: 5px;
}

.ai-note {
    background: #f4f7f5;
    border: 1px solid #e7ece9;
    border-radius: 12px;
    padding: 11px 13px;
    color: #68716e;
    font-size: 10px;
    line-height: 1.5;
}

/* Chat */
[data-testid="stChatMessage"] {
    background: transparent;
}

[data-testid="stChatMessageContent"] {
    font-size: 12px;
    line-height: 1.55;
}

[data-testid="stChatInput"] {
    padding-bottom: 4px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

/* Mobile */
@media (max-width: 800px) {
    .block-container {
        padding: 1.0rem 0.85rem 2rem;
    }

    .desktop-appbar {
        margin-bottom: 20px;
    }

    .hero {
        gap: 10px;
    }

    .page-title {
        font-size: 34px;
    }

    .period-pill {
        font-size: 10px;
        padding: 9px 12px;
    }

    .metric-card {
        min-height: 115px;
        padding: 16px;
    }

    .metric-value {
        font-size: 22px;
    }

    .fin-table {
        font-size: 9px;
    }

    .fin-table th,
    .fin-table td {
        padding: 9px 8px;
    }

    /* Streamlit's sidebar becomes the mobile navigation drawer */
    section[data-testid="stSidebar"] {
        width: min(82vw, 320px);
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# OPENROUTER
# ------------------------------------------------------------

def get_api_key():
    try:
        key = st.secrets.get("OPENROUTER_API_KEY", "")
    except Exception:
        key = ""

    if not key:
        return None

    return str(key).strip()


def build_financial_context():
    lines = [
        f"Reporting period: {FINANCIAL_DATA['period']}",
        "",
        "Headline metrics:",
    ]

    for name, value in FINANCIAL_DATA["metrics"].items():
        lines.append(f"- {name}: {value}")

    lines.append("")
    lines.append("Detailed performance table:")

    for row in FINANCIAL_DATA["rows"]:
        if row[1] is None:
            lines.append(f"[{row[0]}]")
        else:
            lines.append(
                f"- {row[0]} | Last year: {row[1]} | "
                f"Last month: {row[2]} | Current: {row[3]} | "
                f"Target: {row[4]} | Achievement: {row[5]}"
            )

    return "\n".join(lines)


def call_openrouter(messages):
    api_key = get_api_key()

    if not api_key:
        return (
            "API key OpenRouter belum ditemukan. "
            "Pastikan `OPENROUTER_API_KEY` sudah disimpan di Streamlit Secrets."
        )

    # IMPORTANT:
    # HTTP headers must remain ASCII-safe. Do not put emoji or characters
    # such as em-dash (—) into headers.
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://demuy89.streamlit.app",
        "X-Title": "FinAI",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 800,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )

        if response.status_code != 200:
            try:
                detail = response.json()
                message = detail.get("error", {}).get("message", response.text)
            except Exception:
                message = response.text

            return f"LLM API error {response.status_code}: {message}"

        data = response.json()

        choices = data.get("choices", [])
        if not choices:
            return "LLM tidak mengembalikan jawaban."

        content = choices[0].get("message", {}).get("content", "")

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            content = "".join(parts)

        return str(content).strip() or "LLM mengembalikan jawaban kosong."

    except requests.exceptions.Timeout:
        return "Request ke LLM timeout. Silakan coba lagi."
    except requests.exceptions.RequestException as exc:
        return f"Gagal menghubungi OpenRouter: {exc}"
    except Exception as exc:
        return f"Terjadi error saat memproses jawaban LLM: {exc}"


def make_messages(chat_history):
    system_prompt = """You are FinAI, a financial intelligence assistant.

Answer based primarily on the financial data supplied in the context.
Do not invent figures that are not present in the context.
If the user asks for a calculation, calculate from the supplied figures when possible.
If information is unavailable, say so clearly.

Keep answers concise, practical and easy to understand.
Use Indonesian unless the user asks in another language.
For financial performance questions, explain the relevant numbers and comparisons.
Do not present assumptions as facts.
"""

    context = build_financial_context()

    messages = [
        {
            "role": "system",
            "content": system_prompt
            + "\n\nFINANCIAL DATA CONTEXT:\n"
            + context,
        }
    ]

    for item in chat_history:
        messages.append(
            {
                "role": item["role"],
                "content": item["content"],
            }
        )

    return messages


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "ai_open" not in st.session_state:
    st.session_state.ai_open = False


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark">✦</div>
            <div class="brand-name">FinAI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ▣  Dashboard Kinerja")
    st.markdown("### ▤  Laporan Keuangan")
    st.markdown("### ◉  Rincian Data")
    st.markdown("### ⚙  Setting Parameter")

    st.markdown("---")
    st.markdown(
        """
        <div class="sidebar-section">AI CONFIGURATION</div>
        <div style="background:white;color:#60736e;border-radius:7px;padding:7px 9px;font-size:9px;">
            OpenRouter · Free LLM
        </div>
        <div class="sidebar-status">
            <span class="sidebar-dot"></span>Financial Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# AI DIALOG
# ------------------------------------------------------------

@st.dialog("AI Assistant", width="large")
def ai_assistant():
    st.markdown(
        """
        <div class="ai-dialog-title">Financial AI Assistant</div>
        <div class="ai-dialog-status">
            <span class="ai-dialog-dot"></span>Ready to assist
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="ai-note">
            Saya akan menjawab berdasarkan data keuangan yang tersedia di dashboard.
            Kamu bisa bertanya tentang perbandingan bulan lalu, target achievement,
            profitability, asset quality, dan indikator lainnya.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.chat_history:
        st.chat_message("assistant").write(
            "Hi! 👋 Saya FinAI. Silakan tanyakan sesuatu tentang kinerja keuangan."
        )

    for message in st.session_state.chat_history:
        with st.chat_message(
            "user" if message["role"] == "user" else "assistant"
        ):
            st.markdown(message["content"])

    prompt = st.chat_input("Tanyakan sesuatu tentang kinerja keuangan...")

    if prompt:
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Menganalisis..."):
                answer = call_openrouter(
                    make_messages(st.session_state.chat_history)
                )
            st.markdown(answer)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()


# ------------------------------------------------------------
# TOP HEADER
# ------------------------------------------------------------

col_header_1, col_header_2 = st.columns([8, 1])

with col_header_1:
    st.markdown(
        '<div class="desktop-app-name">FinAI</div>',
        unsafe_allow_html=True,
    )

with col_header_2:
    if st.button("✦", key="open_ai", help="Open AI Assistant"):
        ai_assistant()


# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="hero">
        <div>
            <div class="eyebrow">FINANCIAL INTELLIGENCE</div>
            <div class="page-title">Overview</div>
            <div class="subtitle">
                Financial performance overview for {FINANCIAL_DATA['period']}
            </div>
        </div>
        <div class="period-pill">{FINANCIAL_DATA['period']}⌄</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------

metric_cols = st.columns(4)

changes = {
    "Total Assets": "-1.98% vs last month",
    "Total Credit": "-2.19% vs last month",
    "Total DPK": "-2.82% vs last month",
    "Net Profit": "-13.94% vs last month",
}

for col, (name, value) in zip(
    metric_cols, FINANCIAL_DATA["metrics"].items()
):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{name}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-change">{changes[name]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.write("")


# ------------------------------------------------------------
# PERFORMANCE TABLE
# ------------------------------------------------------------

st.markdown(
    """
    <div class="fin-card">
        <div class="card-header">
            <div class="card-title">Performance Overview</div>
            <div class="card-caption">
                Current position, historical context and target achievement
            </div>
        </div>
    """,
    unsafe_allow_html=True,
)

table_html = """
<table class="fin-table">
<thead>
<tr>
<th>Keterangan</th>
<th>Tahun Lalu</th>
<th>Bulan Lalu</th>
<th>Bulan Ini</th>
<th>Target</th>
<th>Ach.</th>
</tr>
</thead>
<tbody>
"""

for row in FINANCIAL_DATA["rows"]:
    if row[1] is None:
        table_html += f'<tr class="section"><td colspan="6">{row[0]}</td></tr>'
    else:
        table_html += (
            "<tr>"
            f"<td>{row[0]}</td>"
            f"<td>{row[1]}</td>"
            f"<td>{row[2]}</td>"
            f"<td>{row[3]}</td>"
            f"<td>{row[4]}</td>"
            f"<td>{row[5]}</td>"
            "</tr>"
        )

table_html += "</tbody></table></div>"

st.markdown(table_html, unsafe_allow_html=True)


# ------------------------------------------------------------
# BOTTOM KPI
# ------------------------------------------------------------

st.write("")

bottom_1, bottom_2 = st.columns(2)

with bottom_1:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Profitability</div>
            <div class="kpi-caption">Revenue, expense and net profit</div>
            <div class="kpi-row">
                <span class="kpi-label">Revenue</span>
                <span class="kpi-value">1,255.2</span>
            </div>
            <div class="kpi-row">
                <span class="kpi-label">Operating Expense</span>
                <span class="kpi-value">556.1</span>
            </div>
            <div class="kpi-row">
                <span class="kpi-label">Net Profit</span>
                <span class="kpi-value">699.1</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with bottom_2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Asset Quality</div>
            <div class="kpi-caption">Risk indicators and coverage</div>
            <div class="kpi-row">
                <span class="kpi-label">NPL Ratio</span>
                <span class="kpi-value">4.20%</span>
            </div>
            <div class="kpi-row">
                <span class="kpi-label">CKPN Coverage</span>
                <span class="kpi-value">115.93%</span>
            </div>
            <div class="kpi-row">
                <span class="kpi-label">Low Cost Funding</span>
                <span class="kpi-value">77.40%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
