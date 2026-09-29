import streamlit as st
import streamlit.components.v1 as components
import json
import urllib.request
import urllib.error

st.set_page_config(page_title="FinAI — Financial Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

# ---------- ONLINE LLM ----------
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

try:
    MODEL = st.secrets.get("OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free)
except Exception:
    MODEL = "google/gemma-4-26b-a4b-it:free"

FINANCIAL_CONTEXT = """
Periode: September 2026
Total Assets 190,510.7; Total Credit 104,549.2; Total DPK 158,545.5; Net Profit 699.1.
Bulan lalu: Assets 194,349.9; Credit 106,885.6; DPK 163,153.8; Net Profit 812.4.
Target: Assets 192,871.1; Credit 101,808.3; DPK 160,414.1; Net Profit 727.1.
Investment 79,599.7; Other Funding 5,045.0; Low Cost Funding 77.4%; Revenue 1,255.2;
Operating Expense 556.1; CKPN 207.9; NPL Ratio 4.2%; CKPN Coverage 115.9%.
"""

SYSTEM_PROMPT = """You are FinAI, a Financial Intelligence Assistant for a banking dashboard.
Answer in Indonesian unless requested otherwise. Use only the supplied dashboard data.
Do not invent numbers. Explain comparisons/calculations briefly. If data is unavailable, say so.
Be concise, analytical, and suitable for management reporting."""

def ask_llm(question):
    if not API_KEY:
        return "API key belum ditemukan. Pastikan OPENROUTER_API_KEY sudah ada di Streamlit Secrets."
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "DATA DASHBOARD:\n" + FINANCIAL_CONTEXT + "\n\nPERTANYAAN:\n" + question},
        ],
        "temperature": 0.2,
        "max_tokens": 500,
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + API_KEY,
            "HTTP-Referer": "https://demuy89.streamlit.app",
            "X-Title": "FinAI",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
        choices = result.get("choices", [])
        if not choices:
            return "LLM tidak mengembalikan jawaban."
        return choices[0]["message"]["content"]
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            detail = str(e)
        return f"LLM API error {e.code}: {detail}"
    except Exception as e:
        return f"Gagal menghubungi LLM: {e}"

# ---------- UI ----------
HTML = r'''<!doctype html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<style>
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#f4f7f5;font-family:Inter,system-ui,sans-serif;color:#18211f}button{font:inherit;cursor:pointer}:root{--g:#005642;--l:#b7f51d;--bg:#f4f7f5}
.app{min-height:100vh;display:grid;grid-template-columns:250px minmax(0,1fr);background:var(--bg);overflow:hidden}.app.collapsed{grid-template-columns:72px minmax(0,1fr)}
.left{position:relative;background:var(--g);color:#fff;padding:18px 14px;overflow:hidden}.head{height:42px;display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}.brand{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800;white-space:nowrap}.mark{width:30px;height:30px;border-radius:9px;background:var(--l);color:var(--g);display:grid;place-items:center;font-weight:900}.toggle{width:34px;height:34px;border-radius:10px;border:1px solid #ffffff22;background:#ffffff12;color:#fff}.nav{display:flex;flex-direction:column;gap:8px}.item{height:46px;border-radius:13px;display:flex;align-items:center;gap:12px;padding:0 12px;color:#d9ece6;font-size:14px;font-weight:650;white-space:nowrap}.item.active{background:#14765f;color:#fff}.icon{width:22px;text-align:center}.collapsed .brandtext,.collapsed .navtext,.collapsed .configtext,.collapsed .configpill,.collapsed .status{display:none}.collapsed .head{justify-content:center}.collapsed .brand{justify-content:center}.collapsed .toggle{position:absolute;right:7px;top:22px;width:26px;height:26px}.collapsed .item{justify-content:center;padding:0}.config{position:absolute;left:14px;right:14px;bottom:18px;border-top:1px solid #ffffff1f;padding-top:15px;color:#9ac3b8;font-size:9px}.configpill{margin-top:9px;padding:7px 9px;border-radius:7px;background:#fff;color:#60736e;font-size:9px}.status{margin-top:8px;color:#d2e7e1;font-size:9px}.dot{display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--l);margin-right:5px}
.main{min-width:0;overflow:auto;padding:28px clamp(20px,3vw,44px) 44px}.dh{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}.appname{font-size:13px;font-weight:800;color:#65716c}.aitrigger{width:40px;height:40px;border-radius:50%;border:1px solid #e4e9e6;background:#fff;color:var(--g);font-size:18px}.top{display:flex;justify-content:space-between;gap:18px;margin-bottom:20px}.ey{color:#a0aaa6;font-size:9px;letter-spacing:2px;font-weight:700}.title{font-size:31px;font-weight:800}.sub{color:#9aa49f;font-size:11px;margin-top:7px}.period{background:#eff6d9;color:#6c7d42;border-radius:18px;padding:10px 15px;font-size:10px}.metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-bottom:14px}.card{background:#fff;border:1px solid #edf0ef;border-radius:17px;box-shadow:0 7px 20px #1e41370b}.metric{padding:17px}.label{color:#909b97;font-size:10px}.value{font-size:22px;font-weight:800;margin-top:6px}.change{color:#a78282;font-size:8px;margin-top:5px}.tablecard{overflow:hidden}.thd{display:flex;justify-content:space-between;align-items:center;padding:16px 17px 12px}.tt{font-size:14px;font-weight:800}.cap{font-size:8px;color:#9ba5a1;margin-top:3px}.switch{background:#f0f6df;color:#718044;border-radius:18px;padding:8px 12px;font-size:9px}.wrap{overflow-x:auto}table{width:100%;min-width:680px;border-collapse:collapse;font-size:8px}th{color:#a1aaa7;padding:8px 12px;text-align:right;border-top:1px solid #e7ece9}th:first-child,td:first-child{text-align:left}td{color:#737d79;padding:10px 12px;text-align:right;border-top:1px solid #edf0ef}tr.sec td{background:#eef5ef;color:#64806f;font-size:9px;letter-spacing:1.5px;font-weight:800;text-align:left;padding:8px 12px}.bottom{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:12px}.small{padding:16px}.smalltitle{font-size:12px;font-weight:800}.kpi{display:flex;justify-content:space-between;margin-top:15px;font-size:9px}.kv{font-size:11px;font-weight:800}
.ai{position:fixed;z-index:200;top:0;right:0;width:min(390px,42vw);height:100dvh;background:#fff;border-left:1px solid #e2e9e5;display:flex;flex-direction:column;box-shadow:-14px 0 40px #00000016;transform:translateX(105%);opacity:0;visibility:hidden;pointer-events:none;transition:.24s ease}.ai.open{transform:translateX(0);opacity:1;visibility:visible;pointer-events:auto}.aihead{padding:24px 20px 17px;border-bottom:1px solid #edf0ef;display:flex;justify-content:space-between}.aititle{font-size:16px;font-weight:800}.aistatus{color:#9ba49f;font-size:8px;margin-top:5px}.close{width:38px;height:38px;border:0;border-radius:50%;background:#f0f2f1;color:#7c8581;font-size:22px}.aibody{padding:24px 18px;overflow:auto;flex:1}.msg{display:flex;gap:10px;margin-bottom:22px}.bot{width:22px;height:22px;border-radius:50%;background:var(--g);color:var(--l);display:grid;place-items:center;flex:none;font-size:11px}.msgtext{font-size:11px;line-height:1.45;max-width:280px}.muted{color:#9ba49f}.bubble{border:1px solid #e1e5e3;border-radius:9px;padding:10px 12px;color:#68716e;font-size:10px}.aifoot{padding:12px 18px 18px;border-top:1px solid #edf0ef}.note{font-size:8px;color:#9ba49f}.mobilehead{display:none}
@media(max-width:800px){.app,.app.collapsed{display:block;min-height:100vh}.left{position:fixed;z-index:300;inset:0 auto 0 0;width:min(78vw,320px);height:100dvh;transform:translateX(-105%);transition:.25s ease;box-shadow:12px 0 40px #0003}.left.open{transform:translateX(0)}.main{padding:96px 18px 38px}.dh{display:none}.title{font-size:29px}.bottom{grid-template-columns:1fr}.mobilehead{display:flex;position:fixed;top:0;left:0;right:0;height:74px;z-index:250;background:#fff;border-bottom:1px solid #edf0ef;align-items:center;justify-content:center}.mobilemenu,.mobileai{position:absolute;top:16px;width:42px;height:42px;border-radius:50%;border:1px solid #e7ebe9;background:#fff}.mobilemenu{left:18px}.mobileai{right:18px;color:var(--g)}.mobilebrand{display:flex;align-items:center;gap:8px;font-size:17px;font-weight:800}.ai{z-index:500;inset:0;width:100vw;height:100dvh;border:0}.overlay{display:none;position:fixed;inset:0;z-index:280;background:#00302655}.overlay.show{display:block}}
</style></head><body>
<div id="app" class="app">
<aside id="left" class="left"><div class="head"><div class="brand"><span class="mark">✦</span><span class="brandtext">FinAI</span></div><button id="toggle" class="toggle">☰</button></div><nav class="nav"><div class="item active"><span class="icon">▣</span><span class="navtext">Dashboard Kinerja</span></div><div class="item"><span class="icon">▤</span><span class="navtext">Laporan Keuangan</span></div><div class="item"><span class="icon">◉</span><span class="navtext">Rincian Data</span></div><div class="item"><span class="icon">⚙</span><span class="navtext">Setting Parameter</span></div></nav><div class="config"><span class="configtext">AI CONFIGURATION</span><div class="configpill">Online LLM · Python Evidence</div><div class="status"><span class="dot"></span>Financial Intelligence</div></div></aside>
<main class="main"><div class="dh"><div class="appname">FinAI</div><button id="openAI" class="aitrigger">✦</button></div><div class="top"><div><div class="ey">FINANCIAL INTELLIGENCE</div><div class="title">Overview</div><div class="sub">Financial performance overview for September 2026</div></div><div class="period">September 2026⌄</div></div>
<div class="metrics"><div class="card metric"><div class="label">Total Assets</div><div class="value">190,510.7</div><div class="change">-1.98% vs last month</div></div><div class="card metric"><div class="label">Total Credit</div><div class="value">104,549.2</div><div class="change">-2.19% vs last month</div></div><div class="card metric"><div class="label">Total DPK</div><div class="value">158,545.5</div><div class="change">-2.82% vs last month</div></div><div class="card metric"><div class="label">Net Profit</div><div class="value">699.1</div><div class="change">-13.94% vs last month</div></div></div>
<section class="card tablecard"><div class="thd"><div><div class="tt">Performance Overview</div><div class="cap">Current position, historical context and target achievement</div></div><div class="switch">Monthly · YTD · YoY</div></div><div class="wrap"><table><thead><tr><th>Keterangan</th><th>Tahun Lalu</th><th>Bulan Lalu</th><th>Bulan Ini</th><th>Target</th><th>Ach.</th></tr></thead><tbody>
<tr class="sec"><td colspan="6">ASSET</td></tr><tr><td>Total Asset</td><td>173,731.1</td><td>194,349.9</td><td>190,510.7</td><td>192,871.1</td><td>98.8%</td></tr><tr><td>Total Credit</td><td>122,208.6</td><td>106,885.6</td><td>104,549.2</td><td>101,808.3</td><td>102.7%</td></tr><tr><td>Total Investment</td><td>76,318.9</td><td>79,825.3</td><td>79,599.7</td><td>80,855.6</td><td>98.4%</td></tr>
<tr class="sec"><td colspan="6">FUNDING</td></tr><tr><td>Total DPK</td><td>146,764.4</td><td>163,153.8</td><td>158,545.5</td><td>160,414.1</td><td>98.8%</td></tr><tr><td>Total Other Funding</td><td>4,460.0</td><td>4,980.0</td><td>5,045.0</td><td>5,040.0</td><td>100.1%</td></tr><tr><td>Low Cost Funding %</td><td>88.3</td><td>78.0</td><td>77.4</td><td>81.0</td><td>95.6%</td></tr>
<tr class="sec"><td colspan="6">PROFITABILITY</td></tr><tr><td>Revenue</td><td>1,373.4</td><td>1,274.2</td><td>1,255.2</td><td>1,378.0</td><td>91.1%</td></tr><tr><td>Operating Expense</td><td>482.9</td><td>461.8</td><td>556.1</td><td>535.4</td><td>103.9%</td></tr><tr><td>CKPN</td><td>210.9</td><td>106.9</td><td>207.9</td><td>198.0</td><td>105.0%</td></tr><tr><td>Net Profit</td><td>890.5</td><td>812.4</td><td>699.1</td><td>727.1</td><td>96.1%</td></tr>
<tr class="sec"><td colspan="6">ASSET QUALITY</td></tr><tr><td>NPL Ratio</td><td>3.6</td><td>0.0</td><td>4.2</td><td>2.2</td><td>190.9%</td></tr><tr><td>CKPN Coverage</td><td>107.0</td><td>114.3</td><td>115.9</td><td>110.0</td><td>105.4%</td></tr>
</tbody></table></div></section>
<div class="bottom"><div class="card small"><div class="smalltitle">Profitability</div><div class="cap">Revenue, expense and net profit</div><div class="kpi"><span>Revenue</span><span class="kv">1,255.2</span></div><div class="kpi"><span>Operating Expense</span><span class="kv">556.1</span></div><div class="kpi"><span>Net Profit</span><span class="kv">699.1</span></div></div><div class="card small"><div class="smalltitle">Asset Quality</div><div class="cap">Risk indicators and coverage</div><div class="kpi"><span>NPL Ratio</span><span class="kv">4.20%</span></div><div class="kpi"><span>CKPN Coverage</span><span class="kv">115.93%</span></div><div class="kpi"><span>Low Cost Funding</span><span class="kv">77.40%</span></div></div></div></main>
<aside id="ai" class="ai"><div class="aihead"><div><div class="aititle">AI Assistant</div><div class="aistatus"><span class="dot"></span>Online LLM</div></div><button id="closeAI" class="close">×</button></div><div class="aibody"><div class="msg"><div class="bot">✦</div><div class="msgtext"><b>Hi there! 👋</b><br><span class="muted">I'm your Financial AI Assistant.<br>Ask me about the dashboard.</span></div></div><div class="msg"><div class="bot">✦</div><div class="msgtext"><span class="muted">Contoh:</span><br><b>Kenapa net profit turun dibanding bulan lalu?</b></div></div></div><div class="aifoot"><div class="note">LLM connection sedang diuji melalui panel Streamlit.</div></div></aside></div>
<div class="mobilehead"><button id="mobileMenu" class="mobilemenu">☰</button><div class="mobilebrand"><span class="mark">✦</span>FinAI</div><button id="mobileAI" class="mobileai">✦</button></div><div id="overlay" class="overlay"></div>
<script>
const app=document.getElementById('app'),left=document.getElementById('left'),ai=document.getElementById('ai'),overlay=document.getElementById('overlay');let collapsed=false;
function mobile(){return innerWidth<=800}function closeDrawer(){left.classList.remove('open');overlay.classList.remove('show')}
function setAI(v){ai.classList.toggle('open',v)}
document.getElementById('toggle').onclick=()=>{if(mobile()){left.classList.toggle('open');overlay.classList.toggle('show',left.classList.contains('open'))}else{collapsed=!collapsed;app.classList.toggle('collapsed',collapsed)}};
document.getElementById('mobileMenu').onclick=()=>{left.classList.toggle('open');overlay.classList.toggle('show',left.classList.contains('open'))};overlay.onclick=closeDrawer;document.getElementById('openAI').onclick=()=>setAI(true);document.getElementById('mobileAI').onclick=()=>setAI(true);document.getElementById('closeAI').onclick=()=>setAI(false);setAI(false);window.onresize=()=>{if(!mobile())closeDrawer()};
</script></body></html>'''

components.html(HTML, height=1550, scrolling=False)

# ---------- FIRST LLM TEST ----------
st.divider()
st.caption(f"FinAI LLM Test · Model: {MODEL}")
question = st.text_input("Pertanyaan untuk LLM", placeholder="Contoh: Kenapa net profit turun dibanding bulan lalu?", label_visibility="collapsed")
if st.button("Test LLM", type="primary"):
    if not question.strip():
        st.warning("Masukkan pertanyaan terlebih dahulu.")
    else:
        with st.spinner("Menghubungkan ke online LLM..."):
            answer = ask_llm(question.strip())
        st.markdown("**Jawaban LLM:**")
        st.write(answer)
