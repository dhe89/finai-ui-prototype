import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FinAI — Financial Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = r"""*{box-sizing:border-box} :root{--green:#004b3a;--green2:#075c48;--lime:#b8f226;--bg:#f5f7f6;--text:#17201d;--muted:#8a9490;--line:#e7ebe9}
html,body{margin:0;min-height:100%;font-family:Inter,Arial,sans-serif;color:var(--text);background:#eef1ef}
body{overflow-x:hidden}
.app-shell{min-height:100vh;display:grid;grid-template-columns:190px minmax(0,1fr) 310px;background:#fff}
.sidebar{position:sticky;top:0;height:100vh;min-height:100vh;background:var(--green);color:#fff;padding:34px 18px 22px;display:flex;flex-direction:column;z-index:30}
.brand{display:flex;align-items:center;gap:9px;font-weight:700;font-size:18px;margin:0 4px 30px}.brand-mark{width:23px;height:23px;border-radius:7px;background:var(--lime);color:var(--green);display:grid;place-items:center;font-weight:800;font-size:15px}
.nav{display:flex;flex-direction:column;gap:7px}.nav-item{border:0;background:transparent;color:#fff;text-align:left;padding:11px 10px;border-radius:11px;display:flex;gap:10px;align-items:flex-start;font:600 12px Inter;cursor:pointer;opacity:.92}.nav-item span:first-child{font-size:8px;margin-top:4px}.nav-item.active{background:#126a53}.nav-item:hover{background:#0c604b}
.sidebar-bottom{margin-top:auto;border-top:1px solid rgba(255,255,255,.12);padding-top:18px}.section-label{font-size:7px;letter-spacing:1.2px;color:#9eb5ad;margin-bottom:9px}.config-pill{background:#fff;color:#58625e;border-radius:7px;padding:10px 9px;font-size:8px;margin-bottom:10px}.status{font-size:8px;color:#d0ded9}.status i,.ai-head i{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--lime);margin-right:5px}
.main-content{min-width:0;background:var(--bg);min-height:100vh}.content-inner{padding:34px 22px 40px;max-width:1500px;margin:auto}.eyebrow{font-size:8px;letter-spacing:2px;color:#a2aaa6}.page-heading{display:flex;justify-content:space-between;align-items:flex-end;margin:5px 0 22px}.page-heading h1{font-size:27px;line-height:1;margin:0 0 6px;letter-spacing:-1px}.page-heading p{margin:0;color:#929b97;font-size:9px}.period,.filter-pill{background:#f0f5df;color:#728346;padding:9px 13px;border-radius:20px;font-size:8px;font-weight:600}
.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:13px}.kpi-card{background:#fff;border:1px solid #edf0ee;border-radius:15px;padding:16px 15px;box-shadow:0 5px 18px rgba(22,45,38,.035)}.kpi-card span{display:block;font-size:8px;color:#8d9692;margin-bottom:8px}.kpi-card strong{display:block;font-size:19px;letter-spacing:-.5px}.kpi-card small{font-size:7px;margin-top:5px;display:block}.negative{color:#b96b6b}.positive{color:#6b9a31}.warn{color:#c99a29;font-weight:700}
.panel,.summary-card{background:#fff;border:1px solid #edf0ee;border-radius:15px;box-shadow:0 5px 18px rgba(22,45,38,.035)}.panel{overflow:hidden}.panel-head{padding:15px 15px 12px;display:flex;justify-content:space-between;align-items:center}.panel-head h2,.summary-card h2{font-size:11px;margin:0 0 4px}.panel-head p,.summary-card>p{font-size:7px;color:#a0a8a5;margin:0}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;min-width:760px;font-size:7px}th{text-align:right;color:#9ca5a1;font-weight:500;padding:8px 10px;border-top:1px solid var(--line);white-space:nowrap}th:first-child,td:first-child{text-align:left}td{padding:9px 10px;text-align:right;border-top:1px solid #edf0ee;color:#68716d;white-space:nowrap}.group td{background:#f2f7f2;color:#64806e;font-weight:700;letter-spacing:1px;font-size:7px;padding:7px 10px}
.summary-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:13px}.summary-card{padding:16px}.summary-row{display:flex;justify-content:space-between;align-items:center;padding:11px 0;border-bottom:1px solid #edf0ee;font-size:8px}.summary-row:last-child{border-bottom:0}.summary-row small{display:block;color:#a2aaa6;font-size:6px;margin-top:3px}.summary-row b{font-size:10px}
.ai-panel{position:sticky;top:0;height:100vh;min-height:100vh;background:#fff;border-left:1px solid #e7ebe9;display:flex;flex-direction:column;z-index:40}.ai-head{padding:28px 18px 17px;border-bottom:1px solid #edf0ee;display:flex;justify-content:space-between}.ai-head h2{font-size:14px;margin:0 0 5px}.ai-head span{font-size:7px;color:#929b97}.close-btn,.icon-btn{border:0;background:#f2f4f3;color:#8d9692;width:30px;height:30px;border-radius:50%;font-size:18px;cursor:pointer}.chat{flex:1;overflow-y:auto;padding:18px 15px}.message{display:flex;gap:9px;margin-bottom:22px;font-size:9px;line-height:1.55}.message.assistant{align-items:flex-start}.avatar{flex:0 0 18px;width:18px;height:18px;border-radius:50%;background:var(--green);color:var(--lime);display:grid;place-items:center;font-size:10px}.message p{margin:3px 0 0;color:#8c9691}.message.user{justify-content:flex-end}.message.user div{max-width:85%;border:1px solid #e3e7e5;border-radius:9px;padding:10px;color:#69716e}.chat-input{padding:12px;border-top:1px solid #edf0ee;background:#fff}.chat-input input{width:100%;height:38px;border:1px solid #e1e6e3;border-radius:9px;padding:0 10px;font:9px Inter;outline:none;margin-bottom:8px}.chat-input button{width:100%;height:38px;border:0;border-radius:9px;background:var(--lime);color:#264000;font:600 9px Inter;cursor:pointer}
.mobile-header{display:none}.mobile-backdrop{display:none}
@media(max-width:1100px){.app-shell{grid-template-columns:175px minmax(0,1fr) 285px}.content-inner{padding-left:16px;padding-right:16px}.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:768px){
  body{background:#fff}
  .app-shell{display:block;min-height:100vh}
  .main-content{min-height:100vh;width:100%}
  .content-inner{padding:18px 14px 30px}
  .mobile-header{height:58px;display:flex;align-items:center;justify-content:space-between;padding:0 14px;background:#fff;border-bottom:1px solid #edf0ee;position:sticky;top:0;z-index:20}
  .mobile-brand{font-size:15px;font-weight:700;display:flex;align-items:center;gap:7px}.mobile-brand .brand-mark{width:20px;height:20px;font-size:12px}
  .icon-btn{background:#f4f6f5;width:34px;height:34px}
  .sidebar{position:fixed;left:0;top:0;width:245px;height:100dvh;min-height:0;transform:translateX(-105%);transition:transform .22s ease;box-shadow:12px 0 30px rgba(0,0,0,.12);padding-top:28px}
  .sidebar.open{transform:translateX(0)}
  .ai-panel{position:fixed;right:0;top:0;width:min(92vw,390px);height:100dvh;min-height:0;transform:translateX(105%);transition:transform .22s ease;box-shadow:-12px 0 30px rgba(0,0,0,.12)}
  .ai-panel.open{transform:translateX(0)}
  .mobile-backdrop{position:fixed;inset:0;background:rgba(0,25,18,.32);z-index:25;display:block;opacity:0;pointer-events:none;transition:opacity .2s}
  .mobile-backdrop.show{opacity:1;pointer-events:auto}
  .page-heading{align-items:flex-start}.page-heading h1{font-size:24px}.period{font-size:7px;padding:8px 10px}
  .kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.kpi-card{padding:13px 12px;border-radius:13px}.kpi-card strong{font-size:17px}
  .panel-head{padding:13px}.filter-pill{font-size:7px;padding:7px 9px}
  .summary-grid{grid-template-columns:1fr;gap:9px}
  table{min-width:720px}
}
@media(max-width:430px){
  .content-inner{padding:16px 10px 25px}.eyebrow{font-size:7px}.page-heading{margin-bottom:16px}.page-heading h1{font-size:22px}.page-heading p{font-size:8px}
  .period{font-size:6px}.kpi-card span{font-size:7px}.kpi-card strong{font-size:15px}.kpi-card small{font-size:6px}
  .panel-head h2{font-size:10px}.filter-pill{display:none}.summary-card{padding:13px}
}

"""

JS = r"""const sidebar=document.getElementById('sidebar');
const aiPanel=document.getElementById('aiPanel');
const backdrop=document.getElementById('backdrop');
const menuBtn=document.getElementById('menuBtn');
const aiBtn=document.getElementById('aiBtn');
const closeAi=document.getElementById('closeAi');

function openSidebar(){sidebar.classList.add('open'); backdrop.classList.add('show')}
function openAI(){aiPanel.classList.add('open'); backdrop.classList.add('show')}
function closeDrawers(){sidebar.classList.remove('open'); aiPanel.classList.remove('open'); backdrop.classList.remove('show')}

menuBtn?.addEventListener('click',openSidebar);
aiBtn?.addEventListener('click',openAI);
closeAi?.addEventListener('click',closeDrawers);
backdrop?.addEventListener('click',closeDrawers);

document.querySelectorAll('.nav-item').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    if(window.innerWidth<=768) closeDrawers();
  });
});

document.getElementById('sendBtn')?.addEventListener('click',()=>{
  const input=document.getElementById('chatInput');
  const text=input.value.trim();
  if(!text)return;
  const chat=document.querySelector('.chat');
  const msg=document.createElement('div');
  msg.className='message user';
  msg.innerHTML=`<div>${text.replace(/[<>&"]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]))}</div>`;
  chat.appendChild(msg);
  input.value='';
  chat.scrollTop=chat.scrollHeight;
});
document.getElementById('chatInput')?.addEventListener('keydown',e=>{
  if(e.key==='Enter') document.getElementById('sendBtn').click();
});
window.addEventListener('resize',()=>{
  if(window.innerWidth>768) closeDrawers();
});

"""

BODY = r"""<div class="app-shell">
    <div class="mobile-backdrop" id="backdrop"></div>

    <aside class="sidebar" id="sidebar">
      <div class="brand">
        <div class="brand-mark">✦</div>
        <span>FinAI</span>
      </div>

      <nav class="nav">
        <button class="nav-item active" data-page="dashboard">
          <span>●</span><span>Dashboard Kinerja</span>
        </button>
        <button class="nav-item" data-page="financial">
          <span>●</span><span>Laporan Keuangan</span>
        </button>
        <button class="nav-item" data-page="data">
          <span>●</span><span>Rincian Data</span>
        </button>
        <button class="nav-item" data-page="settings">
          <span>●</span><span>Setting Parameter</span>
        </button>
      </nav>

      <div class="sidebar-bottom">
        <div class="section-label">AI CONFIGURATION</div>
        <div class="config-pill">Gemma 4 · Python Evidence</div>
        <div class="status"><i></i> Local Financial Intelligence</div>
      </div>
    </aside>

    <main class="main-content">
      <header class="mobile-header">
        <button class="icon-btn" id="menuBtn" aria-label="Open menu">☰</button>
        <div class="mobile-brand"><span class="brand-mark">✦</span> FinAI</div>
        <button class="icon-btn" id="aiBtn" aria-label="Open AI Assistant">✦</button>
      </header>

      <div class="content-inner">
        <div class="eyebrow">FINANCIAL INTELLIGENCE</div>
        <div class="page-heading">
          <div>
            <h1>Overview</h1>
            <p>Financial performance overview for September 2026</p>
          </div>
          <div class="period">September 2026⌄</div>
        </div>

        <section class="kpi-grid">
          <article class="kpi-card"><span>Total Assets</span><strong>190,510.7</strong><small class="negative">-1.98% vs last month</small></article>
          <article class="kpi-card"><span>Total Credit</span><strong>104,549.2</strong><small class="negative">-2.19% vs last month</small></article>
          <article class="kpi-card"><span>Total DPK</span><strong>158,545.5</strong><small class="negative">-2.82% vs last month</small></article>
          <article class="kpi-card"><span>Net Profit</span><strong>699.1</strong><small class="negative">-13.94% vs last month</small></article>
        </section>

        <section class="panel performance">
          <div class="panel-head">
            <div><h2>Performance Overview</h2><p>Current position, historical context and target achievement</p></div>
            <span class="filter-pill">Monthly · YTD · YoY</span>
          </div>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Keterangan</th><th>Tahun Lalu</th><th>Bulan Lalu</th><th>Bulan Ini</th><th>Target Bulan</th><th>Ach. Bulan</th><th>Growth MoM</th><th>Growth YoY</th><th>Ach. Tahun</th></tr></thead>
              <tbody>
                <tr class="group"><td colspan="9">ASSET</td></tr>
                <tr><td>Total Asset</td><td>173,731.1</td><td>194,349.9</td><td>190,510.7</td><td>192,873.1</td><td class="warn">98.78%</td><td class="negative">-1.98%</td><td class="positive">26.36%</td><td>91.46%</td></tr>
                <tr><td>Total Credit</td><td>122,208.6</td><td>106,885.6</td><td>104,549.2</td><td>105,908.3</td><td class="warn">98.72%</td><td class="negative">-2.19%</td><td class="negative">-11.73%</td><td>91.40%</td></tr>
                <tr><td>Total Investment</td><td>76,318.9</td><td>79,825.3</td><td>79,599.7</td><td>80,395.6</td><td class="warn">99.01%</td><td class="negative">-0.28%</td><td class="positive">9.89%</td><td>91.68%</td></tr>
                <tr class="group"><td colspan="9">FUNDING</td></tr>
                <tr><td>Total DPK</td><td>146,764.4</td><td>163,153.8</td><td>158,545.5</td><td>160,448.1</td><td class="warn">98.81%</td><td class="negative">-2.82%</td><td class="positive">25.15%</td><td>91.49%</td></tr>
                <tr><td>Total Other Funding</td><td>4,460.0</td><td>4,980.0</td><td>5,045.0</td><td>—</td><td>—</td><td class="positive">1.31%</td><td class="positive">18.29%</td><td>—</td></tr>
                <tr><td>Low Cost Funding %</td><td>88.3</td><td>78.0</td><td>77.4</td><td>64.8</td><td class="positive">119.44%</td><td class="negative">-0.76%</td><td class="negative">-10.52%</td><td>99.23%</td></tr>
                <tr class="group"><td colspan="9">PROFITABILITY</td></tr>
                <tr><td>Revenue</td><td>1,373.4</td><td>1,274.2</td><td>1,255.2</td><td>1,318.0</td><td class="warn">95.24%</td><td class="negative">-1.49%</td><td class="negative">-4.93%</td><td>71.43%</td></tr>
                <tr><td>Operating Expense</td><td>482.9</td><td>461.8</td><td>556.1</td><td>539.4</td><td class="positive">103.09%</td><td class="positive">20.43%</td><td class="positive">50.40%</td><td>77.32%</td></tr>
                <tr><td>CKPN</td><td>210.9</td><td>106.9</td><td>207.9</td><td>—</td><td>—</td><td class="positive">94.53%</td><td class="positive">75.56%</td><td>—</td></tr>
                <tr><td>Net Profit</td><td>890.5</td><td>812.4</td><td>699.1</td><td>727.1</td><td class="warn">96.15%</td><td class="negative">-13.94%</td><td class="negative">-26.45%</td><td>72.12%</td></tr>
                <tr class="group"><td colspan="9">ASSET QUALITY</td></tr>
                <tr><td>NPL Ratio</td><td>3.6</td><td>0.0</td><td>4.2</td><td>2.2</td><td class="positive">190.79%</td><td>—</td><td>—</td><td>190.79%</td></tr>
                <tr><td>CKPN Coverage</td><td>107.0</td><td>114.3</td><td>115.9</td><td>115.0</td><td class="positive">100.81%</td><td class="positive">1.39%</td><td class="positive">6.41%</td><td>100.81%</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="summary-grid">
          <article class="summary-card"><h2>Profitability</h2><p>Revenue, expense and net profit</p><div class="summary-row"><span>Revenue<small>Target 1,318.0</small></span><b>1,255.2</b></div><div class="summary-row"><span>Operating Expense<small>Target 539.4</small></span><b>556.1</b></div><div class="summary-row"><span>Net Profit<small>Target 727.1</small></span><b>699.1</b></div></article>
          <article class="summary-card"><h2>Asset Quality</h2><p>Risk indicators and coverage</p><div class="summary-row"><span>NPL Ratio<small>Target 2.20%</small></span><b>4.20%</b></div><div class="summary-row"><span>CKPN Coverage<small>Target 115.00%</small></span><b>115.93%</b></div><div class="summary-row"><span>Low Cost Funding<small>Current funding mix</small></span><b>77.40%</b></div></article>
        </section>
      </div>
    </main>

    <aside class="ai-panel" id="aiPanel">
      <div class="ai-head">
        <div><h2>AI Assistant</h2><span><i></i> Ready to assist</span></div>
        <button class="close-btn" id="closeAi">×</button>
      </div>
      <div class="chat">
        <div class="message assistant"><span class="avatar">✦</span><div><b>Hi there! 👋</b><p>I'm your Financial AI Assistant.<br>How can I help you today?</p></div></div>
        <div class="message user"><div>Hello</div></div>
        <div class="message assistant"><span class="avatar">✦</span><div>Do you want to compare the current performance with the previous month?</div></div>
        <div class="message user"><div>Yes, compare it with the previous month</div></div>
        <div class="message assistant"><span class="avatar">✦</span><div>You spent <b>699.1</b> net profit this month versus <b>812.4</b> previous month. That's a <b>13.94% decrease</b> compared to the previous month.</div></div>
      </div>
      <div class="chat-input"><input placeholder="Write a message..." id="chatInput"><button id="sendBtn">Send ↗</button></div>
    </aside>
  </div>
  
"""

# Hide Streamlit chrome and give the prototype maximum available space.
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
header[data-testid="stHeader"] {visibility:hidden; height:0;}
footer {visibility:hidden;}
.block-container {padding:0 !important; max-width:none !important;}
[data-testid="stAppViewContainer"] > .main {padding:0 !important;}
[data-testid="stDecoration"] {display:none;}
</style>
""", unsafe_allow_html=True)

document = f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{CSS}
/* Streamlit iframe normalization */
html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100%;
  min-height: 100%;
  background: #eef1ef;
}
</style>
</head>
<body>
{BODY}
<script>
{JS}
</script>
</body>
</html>
""".replace("{CSS}", CSS).replace("{BODY}", BODY).replace("{JS}", JS)

# A generous iframe height allows the complete desktop dashboard to be tested,
# while mobile browsers can scroll naturally.
components.html(document, height=1250, scrolling=True)
