const root = document.getElementById("finai-root");
const sidebarSlot = document.getElementById("sidebar-slot");
const headerSlot = document.getElementById("header-slot");
const mainContent = document.getElementById("main-content");
const aiSlot = document.getElementById("ai-slot");
const mobileOverlay = document.getElementById("mobile-overlay");

const state = {
  page: "kinerja",
  sidebarCollapsed: false,
  mobileSidebarOpen: false,
  aiOpen: false
};

async function loadText(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Unable to load ${path}: ${response.status}`);
  return response.text();
}

async function loadLayout() {
  sidebarSlot.innerHTML = await loadText("layout/sidebar.html");
  headerSlot.innerHTML = await loadText("layout/header.html");
  aiSlot.innerHTML = await loadText("layout/ai_chat.html");
  bindLayoutEvents();
}

async function loadPage(page) {
  const allowed = ["kinerja", "financial_report", "data_detail", "setting"];
  if (!allowed.includes(page)) page = "kinerja";

  state.page = page;
  mainContent.classList.add("loading-page");

  try {
    mainContent.innerHTML = await loadText(`pages/${page}.html`);
    document.querySelectorAll(".nav-item").forEach(item => {
      item.classList.toggle("active", item.dataset.page === page);
    });
  } catch (error) {
    mainContent.innerHTML = `
      <section class="page">
        <div class="card error-card">
          <b>Page gagal dimuat</b>
          <div>${escapeHtml(error.message)}</div>
        </div>
      </section>`;
  } finally {
    mainContent.classList.remove("loading-page");
  }
}

function bindLayoutEvents() {
  document.getElementById("sidebar-toggle").addEventListener("click", toggleSidebar);
  document.getElementById("mobile-menu-button").addEventListener("click", toggleMobileSidebar);
  document.getElementById("desktop-ai-button").addEventListener("click", () => setAI(true));
  document.getElementById("mobile-ai-button").addEventListener("click", () => setAI(true));
  document.getElementById("ai-close").addEventListener("click", () => setAI(false));

  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      loadPage(item.dataset.page);
      if (window.innerWidth <= 800) closeMobileSidebar();
    });
  });

  document.getElementById("ai-send").addEventListener("click", sendDemoMessage);
  document.getElementById("ai-input").addEventListener("keydown", event => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendDemoMessage();
    }
  });

  mobileOverlay.addEventListener("click", closeMobileSidebar);
}

function toggleSidebar() {
  if (window.innerWidth <= 800) {
    toggleMobileSidebar();
    return;
  }
  state.sidebarCollapsed = !state.sidebarCollapsed;
  root.classList.toggle("sidebar-collapsed", state.sidebarCollapsed);
}

function toggleMobileSidebar() {
  state.mobileSidebarOpen = !state.mobileSidebarOpen;
  root.classList.toggle("mobile-sidebar-open", state.mobileSidebarOpen);
}

function closeMobileSidebar() {
  state.mobileSidebarOpen = false;
  root.classList.remove("mobile-sidebar-open");
}

function setAI(open) {
  state.aiOpen = open;
  root.classList.toggle("ai-open", open);
}

function sendDemoMessage() {
  const input = document.getElementById("ai-input");
  const body = document.getElementById("ai-body");
  const text = input.value.trim();
  if (!text) return;

  body.insertAdjacentHTML("beforeend", `
    <div class="msg user">
      <div class="bubble">${escapeHtml(text)}</div>
    </div>
  `);

  input.value = "";

  const thinkingId = `thinking-${Date.now()}`;
  body.insertAdjacentHTML("beforeend", `
    <div class="msg" id="${thinkingId}">
      <div class="bot">✦</div>
      <div class="msgtext thinking">
        <span>FinAI sedang menganalisis</span>
        <span class="thinking-dots"><i></i><i></i><i></i></span>
      </div>
    </div>
  `);

  body.scrollTop = body.scrollHeight;

  setTimeout(() => {
    const thinking = document.getElementById(thinkingId);
    if (thinking) {
      thinking.outerHTML = `
        <div class="msg">
          <div class="bot">✦</div>
          <div class="msgtext">
            Untuk prototype UI, pesan sudah diterima. Integrasi LLM akan kita pasang pada tahap berikutnya.
          </div>
        </div>
      `;
      body.scrollTop = body.scrollHeight;
    }
  }, 900);
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[char]));
}

async function init() {
  try {
    await loadLayout();
    await loadPage(state.page);
  } catch (error) {
    mainContent.innerHTML = `
      <section class="page">
        <div class="card error-card">
          <b>FinAI gagal diinisialisasi</b>
          <div>${escapeHtml(error.message)}</div>
        </div>
      </section>`;
  }
}

window.addEventListener("resize", () => {
  if (window.innerWidth > 800) closeMobileSidebar();
});

init();
