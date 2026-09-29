
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="FinAI — Financial Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HTML = r"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root{
  --green:#004d3b;
  --green-2:#00664f;
  --lime:#b8f21c;
  --lime-soft:#eef8dc;
  --bg:#f6f7f6;
  --card:#ffffff;
  --text:#17201d;
  --muted:#89928e;
  --line:#e7ebe8;
  --red:#b85c5c;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:#e9ebe9;
  font-family:Inter,Arial,sans-serif;
  color:var(--text);
}
.app{
  width:100%;
  min-height:760px;
  background:#f7f8f7;
  display:grid;
  grid-template-columns:220px minmax(0,1fr) 360px;
  overflow:hidden;
  border-radius:18px;
}
.sidebar{
  background:var(--green);
  color:#fff;
  padding:28px 18px 18px;
  display:flex;
  flex-direction:column;
  min-height:760px;
}
.brand{display:flex;align-items:center;gap:9px;font-size:18px;font-weight:700;margin:0 0 38px 8px}
.logo{width:22px;height:22px;border-radius:7px;background:var(--lime);color:var(--green);display:grid;place-items:center;font-weight:800}
.nav{display:flex;flex-direction:column;gap:7px}
.nav button{
  border:0;background:transparent;color:#d7e5df;text-align:left;
  padding:12px 12px;border-radius:10px;font:500 13px Inter;cursor:pointer;
}
.nav button.active{background:#17634f;color:#fff}
.nav button:hover{background:#125b49}
.sidebar-bottom{margin-top:auto;border-top:1px solid rgba(255,255,255,.10);padding-top:18px}
.label{font-size:8px;letter-spacing:1.4px;color:#86a59a;text-transform:uppercase;margin-bottom:8px}
.badge{background:#fff;color:#34413c;border-radius:8px;padding:10px;font-size:9px}
.status{font-size:9px;color:#a9c4ba;margin-top:9px}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--lime);margin-right:5px}

.main{
  padding:28px 24px 36px;
  min-width:0;
  overflow:auto;
  background:#f8f9f8;
}
.topline{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:22px}
.eyebrow{font-size:8px;letter-spacing:2px;color:#9ba49f;text-transform:uppercase}
h1{font-size:28px;margin:5px 0 3px;letter-spacing:-.8px}
.subtitle{font-size:10px;color:#9aa29f}
.period{font-size:9px;background:var(--lime-soft);color:#6d812d;padding:8px 12px;border-radius:14px;font-weight:600}

.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}
.card{
  background:var(--card);border:1px solid #eef0ef;border-radius:15px;padding:15px;
  box-shadow:0 3px 14px rgba(22,39,32,.04)
}
.kpi-title{font-size:9px;color:#7e8883}
.kpi{font-size:22px;font-weight:700;margin-top:6px}
.delta{font-size:8px;color:#a56a6a;margin-top:6px}

.panel{background:#fff;border:1px solid #ecefed;border-radius:15px;box-shadow:0 3px 14px rgba(22,39,32,.035);overflow:hidden}
.panel-head{display:flex;justify-content:space-between;padding:15px 16px 10px}
.panel-title{font-size:12px;font-weight:700}
.panel-sub{font-size:8px;color:#a0a8a4;margin-top:3px}
.pill{font-size:8px;background:var(--lime-soft);color:#6c812d;border-radius:12px;padding:7px 10px;font-weight:600}

table{width:100%;border-collapse:collapse;font-size:8px}
th{color:#89918e;font-weight:500;background:#fbfcfb}
th,td{padding:8px 9px;border-top:1px solid #eef1ef;text-align:right;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
.section td{background:#f1f7ee;color:#66805d;font-weight:700;letter-spacing:1px;text-transform:uppercase;font-size:7px}
.good{color:#629d42;font-weight:600}.warn{color:#b88a2d;font-weight:600}.bad{color:#b85c5c;font-weight:600}

.bottom-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.metric-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #eef1ef}
.metric-row:last-child{border-bottom:0}
.metric-name{font-size:9px}.metric-small{font-size:7px;color:#a0a7a4;margin-top:3px}.metric-value{font-size:10px;font-weight:700}

.ai{
  background:#fff;border-left:1px solid #e3e7e4;display:flex;flex-direction:column;min-height:760px;
}
.ai-head{padding:25px 20px 17px;border-bottom:1px solid #edf0ee;display:flex;justify-content:space-between}
.ai-title{font-size:14px;font-weight:700}.ready{font-size:8px;color:#8b9791;margin-top:6px}
.close{border:0;background:#f0f2ef;width:25px;height:25px;border-radius:50%;cursor:pointer;color:#7c8581}
.chat{padding:18px 18px;overflow:auto;flex:1}
.msg{font-size:10px;line-height:1.5;margin-bottom:20px}
.ai-msg{display:flex;gap:9px}.avatar{width:19px;height:19px;border-radius:50%;background:var(--green);color:var(--lime);display:grid;place-items:center;font-size:9px;font-weight:700;flex:none}
.bubble-user{margin-left:auto;background:#fff;border:1px solid #e4e8e5;border-radius:7px;padding:10px;max-width:82%;box-shadow:0 2px 8px rgba(0,0,0,.025)}
.quick{display:flex;justify-content:flex-end;margin:8px 0 18px}.quick button{
 border:1px solid #e2e7e3;background:#fff;border-radius:7px;padding:10px 12px;font-size:9px;color:#4f5a55
}
.ai-foot{padding:12px;border-top:1px solid #edf0ee}
.input{display:flex;gap:8px}
input{flex:1;border:1px solid #e1e6e3;border-radius:8px;padding:11px;font:9px Inter;outline:none}
.send{border:0;background:var(--lime);color:#274100;border-radius:8px;padding:0 15px;font:600 9px Inter;cursor:pointer}
.new{width:100%;margin-top:8px;border:1px solid #e1e6e3;background:#fff;border-radius:8px;padding:9px;font-size:9px}

.hidden{display:none}
@media(max-width:900px){
  .app{grid-template-columns:170px minmax(0,1fr) 300px}
  .cards{grid-template-columns:1fr 1fr}
}
@media(max-width:650px){
  .app{grid-template-columns:74px minmax(0,1fr)}
  .sidebar{padding:22px 9px}
  .brand span,.nav button span,.sidebar-bottom{display:none}
  .nav button{text-align:center;padding:12px 5px}
  .ai{position:fixed;right:0;top:0;width:88vw;max-width:360px;height:100vh;z-index:10;box-shadow:-8px 0 30px rgba(0,0,0,.12)}
  .ai.closed{display:none}
  .main{padding:20px 12px}
  .cards{grid-template-columns:1fr 1fr}
  h1{font-size:22px}
}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="brand"><div class="logo">✦</div><span>FinAI</span></div>
    <nav class="nav">
      <button class="active" onclick="showPage('dashboard',this)">● <span>Dashboard<br>Kinerja</span></button>
      <button onclick="showPage('laporan',this)">● <span>Laporan<br>Keuangan</span></button>
      <button onclick="showPage('rincian',this)">● <span>Rincian Data</span></button>
      <button onclick="showPage('setting',this)">● <span>Setting<br>Parameter</span></button>
    </nav>
    <div class="sidebar-bottom">
      <div class="label">AI Configuration</div>
      <div class="badge">Gemma 4 · Python Evidence</div>
      <div class="status"><span class="dot"></span>Local Financial Intelligence</div>
    </div>
  </aside>

  <main class="main">
    <section id="dashboard">
      <div class="topline">
        <div><div class="eyebrow">Financial Intelligence</div><h1>Overview</h1><div class="subtitle">Financial performance overview for September 2026</div></div>
        <div class="period">September 2026⌄</div>
      </div>
      <div class="cards">
        <div class="card"><div class="kpi-title">Total Assets</div><div class="kpi">190,510.7</div><div class="delta">-1.98% vs last month</div></div>
        <div class="card"><div class="kpi-title">Total Credit</div><div class="kpi">104,549.2</div><div class="delta">-2.19% vs last month</div></div>
        <div class="card"><div class="kpi-title">Total DPK</div><div class="kpi">158,545.5</div><div class="delta">-2.82% vs last month</div></div>
        <div class="card"><div class="kpi-title">Net Profit</div><div class="kpi">699.1</div><div class="delta">-13.94% vs last month</div></div>
      </div>
      <div class="panel">
        <div class="panel-head"><div><div class="panel-title">Performance Overview</div><div class="panel-sub">Current position, historical context and target achievement</div></div><div class="pill">Monthly · YTD · YoY</div></div>
        <table>
          <thead><tr><th>Keterangan</th><th>Tahun Lalu</th><th>Bulan Lalu</th><th>Bulan Ini</th><th>Target Bulan</th><th>Ach. Bulan</th><th>Growth MoM</th><th>Growth YoY</th><th>Ach. Tahun</th></tr></thead>
          <tbody>
            <tr class="section"><td colspan="9">ASSET</td></tr>
            <tr><td>Total Asset</td><td>173,731.1</td><td>194,349.9</td><td>190,510.7</td><td>192,873.1</td><td class="warn">98.78%</td><td class="bad">-1.98%</td><td class="good">26.36%</td><td>91.46%</td></tr>
            <tr><td>Total Credit</td><td>122,208.6</td><td>106,885.6</td><td>104,549.2</td><td>105,908.3</td><td class="warn">98.72%</td><td class="bad">-2.19%</td><td class="bad">-11.73%</td><td>91.40%</td></tr>
            <tr><td>Total Investment</td><td>76,318.9</td><td>79,825.3</td><td>79,599.7</td><td>80,395.6</td><td class="warn">99.01%</td><td class="bad">-0.28%</td><td class="good">9.89%</td><td>91.68%</td></tr>
            <tr class="section"><td colspan="9">FUNDING</td></tr>
            <tr><td>Total DPK</td><td>146,764.4</td><td>163,153.8</td><td>158,545.5</td><td>160,448.1</td><td class="warn">98.81%</td><td class="bad">-2.82%</td><td class="good">25.15%</td><td>91.49%</td></tr>
            <tr><td>Total Other Funding</td><td>4,460.0</td><td>4,980.0</td><td>5,045.0</td><td>-</td><td>-</td><td class="good">1.31%</td><td class="good">18.29%</td><td>-</td></tr>
            <tr><td>Low Cost Funding %</td><td>88.3</td><td>78.0</td><td>77.4</td><td>64.8</td><td class="good">119.44%</td><td class="bad">-0.76%</td><td class="bad">-10.52%</td><td>99.23%</td></tr>
            <tr class="section"><td colspan="9">PROFITABILITY</td></tr>
            <tr><td>Revenue</td><td>1,373.4</td><td>1,274.2</td><td>1,255.2</td><td>1,318.0</td><td class="warn">95.24%</td><td class="bad">-1.49%</td><td class="bad">-4.93%</td><td>71.43%</td></tr>
            <tr><td>Operating Expense</td><td>482.9</td><td>461.8</td><td>556.1</td><td>539.4</td><td class="good">103.09%</td><td class="good">20.43%</td><td class="good">50.40%</td><td>77.32%</td></tr>
            <tr><td>CKPN</td><td>210.9</td><td>106.9</td><td>207.9</td><td>-</td><td>-</td><td class="good">94.53%</td><td class="good">75.56%</td><td>-</td></tr>
            <tr><td>Net Profit</td><td>890.5</td><td>812.4</td><td>699.1</td><td>727.1</td><td class="warn">96.15%</td><td class="bad">-13.94%</td><td class="bad">-26.45%</td><td>72.12%</td></tr>
            <tr class="section"><td colspan="9">ASSET QUALITY</td></tr>
            <tr><td>NPL Ratio</td><td>3.6</td><td>0.0</td><td>4.2</td><td>2.2</td><td class="good">190.79%</td><td>-</td><td>-</td><td>190.79%</td></tr>
            <tr><td>CKPN Coverage</td><td>107.0</td><td>114.3</td><td>115.9</td><td>115.0</td><td class="good">100.81%</td><td class="good">1.39%</td><td class="good">6.41%</td><td>100.81%</td></tr>
          </tbody>
        </table>
      </div>
      <div class="bottom-grid">
        <div class="card"><div class="panel-title">Profitability</div><div class="panel-sub">Revenue, expense and net profit</div>
          <div class="metric-row"><div><div class="metric-name">Revenue</div><div class="metric-small">Target 1,318.0</div></div><div class="metric-value">1,255.2</div></div>
          <div class="metric-row"><div><div class="metric-name">Operating Expense</div><div class="metric-small">Target 539.4</div></div><div class="metric-value">556.1</div></div>
          <div class="metric-row"><div><div class="metric-name">Net Profit</div><div class="metric-small">Target 727.1</div></div><div class="metric-value">699.1</div></div>
        </div>
        <div class="card"><div class="panel-title">Asset Quality</div><div class="panel-sub">Risk indicators and coverage</div>
          <div class="metric-row"><div><div class="metric-name">NPL Ratio</div><div class="metric-small">Target 2.20%</div></div><div class="metric-value">4.20%</div></div>
          <div class="metric-row"><div><div class="metric-name">CKPN Coverage</div><div class="metric-small">Target 115.00%</div></div><div class="metric-value">115.93%</div></div>
          <div class="metric-row"><div><div class="metric-name">Low Cost Funding</div><div class="metric-small">Current funding mix</div></div><div class="metric-value">77.40%</div></div>
        </div>
      </div>
    </section>

    <section id="laporan" class="hidden">
      <div class="topline"><div><div class="eyebrow">Financial Statements</div><h1>Laporan Keuangan</h1><div class="subtitle">Prototype laporan neraca dan laba rugi</div></div><div class="period">September 2026⌄</div></div>
      <div class="cards"><div class="card"><div class="kpi-title">Total Assets</div><div class="kpi">190,510.7</div></div><div class="card"><div class="kpi-title">Total Liabilities</div><div class="kpi">177,200.4</div></div><div class="card"><div class="kpi-title">Equity</div><div class="kpi">13,310.3</div></div><div class="card"><div class="kpi-title">Net Profit</div><div class="kpi">699.1</div></div></div>
      <div class="bottom-grid">
        <div class="panel"><div class="panel-head"><div><div class="panel-title">Neraca</div><div class="panel-sub">Posisi keuangan periode terpilih</div></div></div><table><tbody>
          <tr class="section"><td colspan="2">ASET</td></tr><tr><td>Kas dan Setara Kas</td><td>12,840.2</td></tr><tr><td>Kredit yang Diberikan</td><td>104,549.2</td></tr><tr><td>Investasi</td><td>79,599.7</td></tr><tr class="section"><td colspan="2">LIABILITAS & EKUITAS</td></tr><tr><td>DPK</td><td>158,545.5</td></tr><tr><td>Liabilitas Lainnya</td><td>18,654.9</td></tr><tr><td>Ekuitas</td><td>13,310.3</td></tr>
        </tbody></table></div>
        <div class="panel"><div class="panel-head"><div><div class="panel-title">Laba Rugi</div><div class="panel-sub">Kinerja selama periode terpilih</div></div></div><table><tbody>
          <tr><td>Revenue</td><td>1,255.2</td></tr><tr><td>Operating Expense</td><td>556.1</td></tr><tr><td>CKPN</td><td>207.9</td></tr><tr><td>Net Profit</td><td><b>699.1</b></td></tr>
        </tbody></table></div>
      </div>
    </section>

    <section id="rincian" class="hidden"><div class="topline"><div><div class="eyebrow">Data Explorer</div><h1>Rincian Data</h1><div class="subtitle">Prototype eksplorasi data pendukung</div></div></div><div class="panel"><div class="panel-head"><div class="panel-title">Data Detail</div></div><table><tr><th>Produk</th><th>Outstanding</th><th>Growth</th><th>Status</th></tr><tr><td>KPR Subsidi</td><td>64,210.5</td><td class="good">4.2%</td><td>Active</td></tr><tr><td>KPR Non Subsidi</td><td>28,114.7</td><td class="good">2.1%</td><td>Active</td></tr><tr><td>Cicil Emas</td><td>2,850.4</td><td class="good">8.7%</td><td>Active</td></tr></table></div></section>

    <section id="setting" class="hidden"><div class="topline"><div><div class="eyebrow">Configuration</div><h1>Setting Parameter</h1><div class="subtitle">Prototype konfigurasi indikator dan target</div></div></div><div class="panel"><div class="panel-head"><div class="panel-title">Parameter</div></div><table><tr><th>Parameter</th><th>Value</th><th>Unit</th></tr><tr><td>Target Net Profit</td><td>727.12</td><td>Rp miliar</td></tr><tr><td>Target NPL</td><td>2.20</td><td>%</td></tr><tr><td>Target CKPN Coverage</td><td>115.00</td><td>%</td></tr></table></div></section>
  </main>

  <aside class="ai" id="ai">
    <div class="ai-head"><div><div class="ai-title">AI Assistant</div><div class="ready"><span class="dot"></span>Ready to assist</div></div><button class="close" onclick="toggleAI()">×</button></div>
    <div class="chat" id="chat">
      <div class="msg ai-msg"><div class="avatar">✦</div><div>Hi there! 👋<br><span style="color:#929a96">I'm your Financial AI Assistant.<br>How can I help you today?</span></div></div>
      <div class="quick"><button onclick="ask('Hello')">Hello</button></div>
      <div class="msg ai-msg"><div class="avatar">✦</div><div>Do you want to compare the current performance with the previous month?</div></div>
      <div class="quick"><button onclick="ask('Yes, compare it with the previous month')">Yes, compare it with the previous month</button></div>
      <div class="msg ai-msg"><div class="avatar">✦</div><div>You spent <b>699.1</b> net profit this month versus <b>812.4</b> previous month. That's a <b>13.94% decrease</b> compared to the previous month.</div></div>
    </div>
    <div class="ai-foot"><div class="input"><input id="input" placeholder="Write a message..." onkeydown="if(event.key==='Enter')send()"><button class="send" onclick="send()">Send ↗</button></div><button class="new" onclick="newChat()">＋ New Chat</button></div>
  </aside>
</div>
<script>
function showPage(id,btn){
  document.querySelectorAll('main section').forEach(x=>x.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
  document.querySelectorAll('.nav button').forEach(x=>x.classList.remove('active'));
  btn.classList.add('active');
}
function toggleAI(){document.getElementById('ai').classList.toggle('closed')}
function ask(text){document.getElementById('input').value=text;send()}
function send(){
 const input=document.getElementById('input'); const text=input.value.trim(); if(!text)return;
 const chat=document.getElementById('chat');
 chat.insertAdjacentHTML('beforeend',`<div class="quick"><div class="bubble-user">${text}</div></div>`);
 let reply='Untuk prototype UI ini, AI belum diaktifkan. Data dan percakapan hanya simulasi.';
 if(text.toLowerCase().includes('laba')) reply='Net Profit September 2026 sebesar 699,1, turun 26,45% YoY dan 13,94% MoM. Ini hanya respons simulasi UI.';
 if(text.toLowerCase().includes('cicil emas')) reply='Performa Cicil Emas pada prototype: outstanding 2.850,4 dengan pertumbuhan 8,7%. Ini data dummy untuk uji tampilan.';
 setTimeout(()=>{chat.insertAdjacentHTML('beforeend',`<div class="msg ai-msg"><div class="avatar">✦</div><div>${reply}</div></div>`);chat.scrollTop=chat.scrollHeight},250);
 input.value='';
}
function newChat(){document.getElementById('chat').innerHTML='<div class="msg ai-msg"><div class="avatar">✦</div><div>New chat started. 👋<br><span style="color:#929a96">Ask about performance, products, or financial statements.</span></div></div>'}
</script>
</body>
</html>
"""

components.html(HTML, height=800, scrolling=False)
