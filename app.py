
import streamlit as st

st.set_page_config(
    page_title="FinAI — Financial Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# State
# -----------------------------
if "left_collapsed" not in st.session_state:
    st.session_state.left_collapsed = False

if "ai_open" not in st.session_state:
    st.session_state.ai_open = True

# -----------------------------
# Demo data
# -----------------------------
metrics = [
    ("Total Assets", "190,510.7", "-1.98% vs last month"),
    ("Total Credit", "104,549.2", "-2.19% vs last month"),
    ("Total DPK", "158,545.5", "-2.82% vs last month"),
    ("Net Profit", "699.1", "-13.94% vs last month"),
]

sections = [
    ("ASSET", [
        ("Total Asset", "173,731.1", "194,349.9", "190,510.7", "192,871.1", "98.8%"),
        ("Total Credit", "122,208.6", "106,885.6", "104,549.2", "101,808.3", "102.7%"),
        ("Total Investment", "76,318.9", "79,825.3", "79,599.7", "80,855.6", "98.4%"),
    ]),
    ("FUNDING", [
        ("Total DPK", "146,764.4", "163,153.8", "158,545.5", "160,414.1", "98.8%"),
        ("Total Other Funding", "4,460.0", "4,980.0", "5,045.0", "5,040.0", "100.1%"),
        ("Low Cost Funding %", "88.3", "78.0", "77.4", "81.0", "95.6%"),
    ]),
    ("PROFITABILITY", [
        ("Revenue", "1,373.4", "1,274.2", "1,255.2", "1,378.0", "91.1%"),
        ("Operating Expense", "482.9", "461.8", "556.1", "535.4", "103.9%"),
        ("CKPN", "210.9", "106.9", "207.9", "198.0", "105.0%"),
        ("Net Profit", "890.5", "812.4", "699.1", "727.1", "96.1%"),
    ]),
    ("ASSET QUALITY", [
        ("NPL Ratio", "3.6", "0.0", "4.2", "2.2", "190.9%"),
        ("CKPN Coverage", "107.0", "114.3", "115.9", "110.0", "105.4%"),
    ]),
]

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
:root {
    --green:#005642;
    --green-2:#00705a;
    --lime:#b7f51d;
    --bg:#f4f7f5;
    --card:#ffffff;
    --text:#18211f;
    --muted:#8a9491;
    --line:#e8ecea;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: none !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] {
    display: none !important;
}

/* Remove Streamlit chrome around custom controls */
div[data-testid="stVerticalBlock"] > div:has(> div.finai-shell) {
    padding: 0 !important;
}

.finai-shell {
    min-height: 100vh;
    display: grid;
    grid-template-columns: var(--left-w) minmax(0,1fr) var(--ai-w);
    background: var(--bg);
    overflow: hidden;
    transition: grid-template-columns .24s ease;
}

.finai-shell.left-collapsed {
    grid-template-columns: 76px minmax(0,1fr) var(--ai-w);
}

.finai-shell.ai-closed {
    grid-template-columns: var(--left-w) minmax(0,1fr) 0px;
}

.finai-shell.left-collapsed.ai-closed {
    grid-template-columns: 76px minmax(0,1fr) 0px;
}

.left-panel {
    background: var(--green);
    color:#fff;
    position:relative;
    min-width:0;
    overflow:hidden;
    padding:24px 16px 18px;
}

.left-panel.collapsed {
    padding-left:12px;
    padding-right:12px;
}

.brand {
    display:flex;
    align-items:center;
    gap:10px;
    font-weight:800;
    font-size:20px;
    margin:2px 4px 30px;
    white-space:nowrap;
}

.brand-mark, .ai-mark {
    width:30px;
    height:30px;
    border-radius:9px;
    background:var(--lime);
    color:var(--green);
    display:grid;
    place-items:center;
    font-weight:900;
    flex:0 0 auto;
}

.left-panel.collapsed .brand-text,
.left-panel.collapsed .nav-text,
.left-panel.collapsed .config-text {
    display:none;
}

.left-panel.collapsed .brand {
    justify-content:center;
    margin-left:0;
    margin-right:0;
}

.nav {
    display:flex;
    flex-direction:column;
    gap:8px;
}

.nav-item {
    height:46px;
    border-radius:13px;
    display:flex;
    align-items:center;
    gap:12px;
    padding:0 12px;
    color:#d9ece6;
    font-size:14px;
    font-weight:650;
    white-space:nowrap;
}

.nav-item.active {
    background:#14765f;
    color:#fff;
}

.left-panel.collapsed .nav-item {
    justify-content:center;
    padding:0;
}

.nav-icon {
    width:22px;
    text-align:center;
    font-size:16px;
    flex:0 0 22px;
}

.left-toggle {
    position:absolute;
    top:76px;
    right:-13px;
    z-index:5;
    width:27px;
    height:27px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,.18);
    background:#fff;
    color:var(--green);
    box-shadow:0 4px 15px rgba(0,0,0,.15);
}

.left-panel.collapsed .left-toggle {
    right:-10px;
}

.config {
    position:absolute;
    left:16px;
    right:16px;
    bottom:18px;
    border-top:1px solid rgba(255,255,255,.12);
    padding-top:15px;
    color:#9ac3b8;
    font-size:9px;
    letter-spacing:1.3px;
}

.config-pill {
    margin-top:9px;
    padding:7px 9px;
    border-radius:7px;
    background:#fff;
    color:#60736e;
    letter-spacing:0;
    font-size:9px;
}

.status {
    margin-top:8px;
    letter-spacing:0;
    color:#d2e7e1;
    font-size:9px;
}

.status-dot {
    display:inline-block;
    width:5px;
    height:5px;
    border-radius:50%;
    background:var(--lime);
    margin-right:5px;
}

.main-panel {
    min-width:0;
    overflow:auto;
    padding:28px clamp(18px,3vw,44px) 42px;
}

.topbar {
    display:flex;
    align-items:flex-start;
    justify-content:space-between;
    gap:18px;
    margin-bottom:20px;
}

.eyebrow {
    color:#a3aaa7;
    font-size:9px;
    letter-spacing:2px;
    font-weight:700;
    margin-bottom:3px;
}

.page-title {
    font-size:31px;
    line-height:1.05;
    font-weight:800;
    margin:0;
    color:var(--text);
}

.page-subtitle {
    color:#9ba5a1;
    font-size:11px;
    margin-top:7px;
}

.period {
    background:#eff6d9;
    color:#6c7d42;
    border-radius:18px;
    padding:10px 15px;
    font-size:10px;
    white-space:nowrap;
    font-weight:700;
}

.metrics {
    display:grid;
    grid-template-columns:repeat(2,minmax(0,1fr));
    gap:12px;
    margin-bottom:14px;
}

.metric-card, .table-card, .small-card {
    background:var(--card);
    border:1px solid #edf0ef;
    border-radius:17px;
    box-shadow:0 7px 20px rgba(30,65,55,.045);
}

.metric-card {
    padding:17px;
}

.metric-label {
    color:#909b97;
    font-size:10px;
}

.metric-value {
    color:#17211f;
    font-size:22px;
    font-weight:800;
    margin-top:6px;
}

.metric-change {
    color:#a78282;
    font-size:8px;
    margin-top:5px;
}

.table-card {
    overflow:hidden;
}

.table-head {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:16px 17px 12px;
}

.table-title {
    font-size:14px;
    font-weight:800;
}

.table-caption {
    font-size:8px;
    color:#9ba5a1;
    margin-top:3px;
}

.switcher {
    background:#f0f6df;
    color:#718044;
    border-radius:18px;
    padding:8px 12px;
    font-size:9px;
    font-weight:700;
}

.data-wrap {
    overflow-x:auto;
}

table {
    width:100%;
    border-collapse:collapse;
    min-width:650px;
    font-size:8px;
}

th {
    color:#a1aaa7;
    font-weight:600;
    padding:8px 12px;
    text-align:right;
    border-top:1px solid var(--line);
}

th:first-child, td:first-child {
    text-align:left;
}

td {
    color:#737d79;
    padding:10px 12px;
    text-align:right;
    border-top:1px solid #edf0ef;
}

tr.section-row td {
    background:#eef5ef;
    color:#64806f;
    font-size:9px;
    letter-spacing:1.5px;
    font-weight:800;
    text-align:left;
    padding:8px 12px;
}

.bottom-cards {
    display:grid;
    grid-template-columns:repeat(2,minmax(0,1fr));
    gap:12px;
    margin-top:12px;
}

.small-card {
    padding:16px;
}

.small-title {
    font-size:12px;
    font-weight:800;
}

.small-caption {
    color:#9ca6a2;
    font-size:8px;
    margin-top:2px;
}

.kpi {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:15px;
    font-size:9px;
}

.kpi-label {
    color:#68736f;
}

.kpi-value {
    font-weight:800;
    font-size:11px;
}

.ai-panel {
    background:#fff;
    border-left:1px solid #e9eeeb;
    min-width:0;
    overflow:hidden;
    display:flex;
    flex-direction:column;
}

.ai-panel.closed {
    display:none;
}

.ai-header {
    padding:24px 20px 17px;
    border-bottom:1px solid #edf0ef;
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
}

.ai-title {
    font-size:16px;
    font-weight:800;
}

.ai-status {
    color:#9ba49f;
    font-size:8px;
    margin-top:5px;
}

.ai-status-dot {
    display:inline-block;
    width:5px;
    height:5px;
    border-radius:50%;
    background:var(--lime);
    margin-right:5px;
}

.ai-close {
    width:29px;
    height:29px;
    border-radius:50%;
    border:0;
    background:#f0f2f1;
    color:#7c8581;
    font-size:17px;
}

.ai-body {
    padding:24px 18px;
    overflow:auto;
    flex:1;
}

.msg {
    display:flex;
    gap:10px;
    margin-bottom:22px;
}

.msg.user {
    justify-content:flex-end;
}

.bot-icon {
    width:22px;
    height:22px;
    border-radius:50%;
    background:var(--green);
    color:var(--lime);
    display:grid;
    place-items:center;
    font-size:11px;
    flex:0 0 auto;
}

.msg-text {
    color:#293330;
    font-size:11px;
    line-height:1.45;
    max-width:270px;
}

.user-bubble {
    border:1px solid #e1e5e3;
    border-radius:9px;
    padding:10px 12px;
    color:#68716e;
    font-size:10px;
    max-width:230px;
}

.ai-footer {
    padding:12px 18px 18px;
    border-top:1px solid #edf0ef;
}

.ai-input {
    border:1px solid #e1e5e3;
    border-radius:9px;
    padding:11px 12px;
    color:#a6afab;
    font-size:9px;
    margin-bottom:8px;
}

.ai-send {
    width:100%;
    border:0;
    border-radius:9px;
    padding:10px;
    background:var(--lime);
    color:#25410d;
    font-size:9px;
    font-weight:800;
}

/* Header AI launcher */
.ai-launch {
    position:fixed;
    right:22px;
    top:18px;
    z-index:20;
    width:42px;
    height:42px;
    border-radius:50%;
    border:1px solid #e8ecea;
    background:#fff;
    color:var(--green);
    box-shadow:0 6px 18px rgba(0,0,0,.08);
    display:grid;
    place-items:center;
    font-size:17px;
}

/* Streamlit button normalization */
div[data-testid="stButton"] {
    margin:0 !important;
}
div[data-testid="stButton"] > button {
    font-family:inherit !important;
}

/* Desktop control buttons are transparent and positioned by containers */
.toggle-btn button {
    border:0 !important;
    background:transparent !important;
    color:inherit !important;
    box-shadow:none !important;
}

/* Mobile */
@media (max-width: 800px) {
    .finai-shell,
    .finai-shell.left-collapsed,
    .finai-shell.ai-closed,
    .finai-shell.left-collapsed.ai-closed {
        display:block;
        min-height:100vh;
        overflow:visible;
    }

    .left-panel {
        position:fixed;
        z-index:100;
        inset:0 auto 0 0;
        width:min(78vw,320px);
        transform:translateX(-105%);
        transition:transform .25s ease;
        box-shadow:12px 0 40px rgba(0,0,0,.18);
    }

    .left-panel.mobile-open {
        transform:translateX(0);
    }

    .left-panel.collapsed {
        padding:24px 16px 18px;
    }

    .left-panel.collapsed .brand-text,
    .left-panel.collapsed .nav-text,
    .left-panel.collapsed .config-text {
        display:inline;
    }

    .left-panel.collapsed .brand {
        justify-content:flex-start;
        margin-left:4px;
        margin-right:4px;
    }

    .left-panel.collapsed .nav-item {
        justify-content:flex-start;
        padding:0 12px;
    }

    .left-toggle {
        display:none;
    }

    .main-panel {
        padding:26px 18px 36px;
        overflow:visible;
    }

    .topbar {
        padding-top:46px;
    }

    .page-title {
        font-size:29px;
    }

    .metrics {
        grid-template-columns:repeat(2,minmax(0,1fr));
        gap:12px;
    }

    .metric-card {
        padding:17px;
    }

    .metric-value {
        font-size:20px;
    }

    .bottom-cards {
        grid-template-columns:1fr;
    }

    .ai-panel {
        position:fixed;
        z-index:120;
        inset:0;
        width:100vw;
        height:100dvh;
        border:0;
    }

    .ai-panel.closed {
        display:none;
    }

    .ai-launch {
        top:17px;
        right:18px;
    }

    .mobile-menu-btn {
        position:fixed;
        top:17px;
        left:18px;
        z-index:110;
        width:42px;
        height:42px;
        border-radius:50%;
        border:1px solid #e7ebe9;
        background:#fff;
        box-shadow:0 6px 18px rgba(0,0,0,.08);
    }

    .mobile-brand {
        position:fixed;
        top:24px;
        left:50%;
        transform:translateX(-50%);
        z-index:105;
        display:flex;
        align-items:center;
        gap:8px;
        font-weight:800;
        font-size:17px;
    }

    .mobile-overlay {
        position:fixed;
        inset:0;
        z-index:90;
        background:rgba(0,48,38,.28);
    }
}

@media (min-width: 801px) {
    .mobile-menu-btn, .mobile-brand, .mobile-overlay {
        display:none;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Render shell using HTML for visual structure
# -----------------------------
left_class = "left-panel collapsed" if st.session_state.left_collapsed else "left-panel"
ai_class = "ai-panel" if st.session_state.ai_open else "ai-panel closed"

# Desktop state is represented by CSS variables/classes.
shell_classes = "finai-shell"
if st.session_state.left_collapsed:
    shell_classes += " left-collapsed"
if not st.session_state.ai_open:
    shell_classes += " ai-closed"

# Mobile drawer controls are real Streamlit controls placed above the visual shell.
mobile_cols = st.columns([1, 5, 1])
with mobile_cols[0]:
    st.markdown('<div class="mobile-menu-btn">☰</div>', unsafe_allow_html=True)
with mobile_cols[1]:
    st.markdown('<div class="mobile-brand"><span class="brand-mark">✦</span> FinAI</div>', unsafe_allow_html=True)
with mobile_cols[2]:
    if not st.session_state.ai_open:
        if st.button("✦", key="mobile_ai_open"):
            st.session_state.ai_open = True
            st.rerun()

# Left toggle (desktop)
if st.session_state.left_collapsed:
    left_toggle_label = "▶"
else:
    left_toggle_label = "◀"

# Use a compact control row that remains visible on desktop.
toggle_col1, toggle_col2 = st.columns([1, 10])
with toggle_col1:
    if st.button(left_toggle_label, key="left_toggle"):
        st.session_state.left_collapsed = not st.session_state.left_collapsed
        st.rerun()

# Main shell
st.markdown(f'<div class="{shell_classes}">', unsafe_allow_html=True)

# Left sidebar
st.markdown(f'<aside class="{left_class}">', unsafe_allow_html=True)
st.markdown("""
<div class="brand">
    <span class="brand-mark">✦</span>
    <span class="brand-text">FinAI</span>
</div>
<div class="nav">
    <div class="nav-item active"><span class="nav-icon">▣</span><span class="nav-text">Dashboard Kinerja</span></div>
    <div class="nav-item"><span class="nav-icon">▤</span><span class="nav-text">Laporan Keuangan</span></div>
    <div class="nav-item"><span class="nav-icon">◉</span><span class="nav-text">Rincian Data</span></div>
    <div class="nav-item"><span class="nav-icon">⚙</span><span class="nav-text">Setting Parameter</span></div>
</div>
<div class="config">
    <span class="config-text">AI CONFIGURATION</span>
    <div class="config-pill">Gemma 4 · Python Evidence</div>
    <div class="status"><span class="status-dot"></span>Local Financial Intelligence</div>
</div>
""", unsafe_allow_html=True)
st.markdown("</aside>", unsafe_allow_html=True)

# Main content
st.markdown('<main class="main-panel">', unsafe_allow_html=True)
st.markdown("""
<div class="topbar">
  <div>
    <div class="eyebrow">FINANCIAL INTELLIGENCE</div>
    <div class="page-title">Overview</div>
    <div class="page-subtitle">Financial performance overview for September 2026</div>
  </div>
  <div class="period">September 2026⌄</div>
</div>
""", unsafe_allow_html=True)

metric_html = '<div class="metrics">'
for label, value, change in metrics:
    metric_html += f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-change">{change}</div>
    </div>
    """
metric_html += '</div>'
st.markdown(metric_html, unsafe_allow_html=True)

table_html = """
<div class="table-card">
  <div class="table-head">
    <div>
      <div class="table-title">Performance Overview</div>
      <div class="table-caption">Current position, historical context and target achievement</div>
    </div>
    <div class="switcher">Monthly · YTD · YoY</div>
  </div>
  <div class="data-wrap">
  <table>
    <thead>
      <tr>
        <th>Keterangan</th><th>Tahun Lalu</th><th>Bulan Lalu</th><th>Bulan Ini</th><th>Target</th><th>Ach.</th>
      </tr>
    </thead>
    <tbody>
"""
for section, rows in sections:
    table_html += f'<tr class="section-row"><td colspan="6">{section}</td></tr>'
    for row in rows:
        table_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
table_html += """
    </tbody>
  </table>
  </div>
</div>
"""
st.markdown(table_html, unsafe_allow_html=True)

st.markdown("""
<div class="bottom-cards">
  <div class="small-card">
    <div class="small-title">Profitability</div>
    <div class="small-caption">Revenue, expense and net profit</div>
    <div class="kpi"><span class="kpi-label">Revenue</span><span class="kpi-value">1,255.2</span></div>
    <div class="kpi"><span class="kpi-label">Operating Expense</span><span class="kpi-value">556.1</span></div>
    <div class="kpi"><span class="kpi-label">Net Profit</span><span class="kpi-value">699.1</span></div>
  </div>
  <div class="small-card">
    <div class="small-title">Asset Quality</div>
    <div class="small-caption">Risk indicators and coverage</div>
    <div class="kpi"><span class="kpi-label">NPL Ratio</span><span class="kpi-value">4.20%</span></div>
    <div class="kpi"><span class="kpi-label">CKPN Coverage</span><span class="kpi-value">115.93%</span></div>
    <div class="kpi"><span class="kpi-label">Low Cost Funding</span><span class="kpi-value">77.40%</span></div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</main>", unsafe_allow_html=True)

# AI panel
st.markdown(f'<aside class="{ai_class}">', unsafe_allow_html=True)
st.markdown("""
<div class="ai-header">
  <div>
    <div class="ai-title">AI Assistant</div>
    <div class="ai-status"><span class="ai-status-dot"></span>Ready to assist</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Real Streamlit close button, visually positioned with CSS via a small HTML overlay.
if st.session_state.ai_open:
    close_col = st.columns([8, 1])
    with close_col[1]:
        if st.button("×", key="ai_close"):
            st.session_state.ai_open = False
            st.rerun()

st.markdown("""
<div class="ai-body">
  <div class="msg">
    <div class="bot-icon">✦</div>
    <div class="msg-text"><b>Hi there! 👋</b><br><span style="color:#9ba49f">I'm your Financial AI Assistant.<br>How can I help you today?</span></div>
  </div>
  <div class="msg user"><div class="user-bubble">Hello</div></div>
  <div class="msg">
    <div class="bot-icon">✦</div>
    <div class="msg-text">Do you want to compare the current performance with the previous month?</div>
  </div>
  <div class="msg user"><div class="user-bubble">Yes, compare it with the previous month</div></div>
  <div class="msg">
    <div class="bot-icon">✦</div>
    <div class="msg-text">You spent <b>699.1 net profit</b> this month versus <b>812.4</b> previous month. That's a <b>13.94% decrease</b> compared to the previous month.</div>
  </div>
</div>
<div class="ai-footer">
  <div class="ai-input">Write a message...</div>
  <div class="ai-send">Send ↗</div>
</div>
""", unsafe_allow_html=True)
st.markdown("</aside>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Header AI launcher appears only when panel is closed.
if not st.session_state.ai_open:
    st.markdown('<div class="ai-launch">✦</div>', unsafe_allow_html=True)
    if st.button("✦", key="ai_open_desktop"):
        st.session_state.ai_open = True
        st.rerun()
