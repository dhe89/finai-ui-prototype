export default function(component) {
  const { parentElement, data, setTriggerValue } = component;
  const root = parentElement.querySelector('#finai-root');
  if (!root) return;

  const sidebarSlot = root.querySelector('#sidebar-slot');
  const headerSlot = root.querySelector('#header-slot');
  const mainContent = root.querySelector('#main-content');
  const aiSlot = root.querySelector('#ai-slot');
  const overlay = root.querySelector('#mobile-overlay');

  const pages = data?.pages || {};
  const history = Array.isArray(data?.chat_history) ? data.chat_history : [];
  const responseVersion = data?.response_version || 0;

  // Render static layout once. Never create another component/iframe here.
  if (!sidebarSlot.dataset.ready) {
    sidebarSlot.innerHTML = data?.sidebar_html || '';
    headerSlot.innerHTML = data?.header_html || '';
    aiSlot.innerHTML = data?.ai_html || '';
    sidebarSlot.dataset.ready = '1';
  }

  const state = window.__finaiState || (window.__finaiState = {
    page: 'kinerja',
    sidebarCollapsed: false,
    mobileSidebarOpen: false,
    aiOpen: false,
    lastResponseVersion: -1,
    handlersBound: false,
  });

  function applyResponsiveMode() {
    const isMobile = root.clientWidth <= 800;
    root.classList.toggle('is-mobile', isMobile);
    if (!isMobile) {
      state.mobileSidebarOpen = false;
      root.classList.remove('mobile-sidebar-open');
    }
  }

  function esc(value) {
    return String(value ?? '').replace(/[&<>"']/g, ch => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'
    }[ch]));
  }

  function renderPage(page) {
    if (!pages[page]) page = 'kinerja';
    state.page = page;
    mainContent.innerHTML = pages[page] || '<div class="card error-card">Halaman tidak tersedia.</div>';
    root.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.page === page);
    });
  }

  function renderHistory() {
    const body = root.querySelector('#ai-body');
    if (!body) return;
    let html = `
      <div class="msg">
        <div class="bot">✦</div>
        <div class="msgtext"><b>Hi there! 👋</b><br><span class="muted">I'm your Financial AI Assistant.<br>Ask me about the dashboard.</span></div>
      </div>`;

    for (const item of history) {
      if (item.role === 'user') {
        html += `<div class="msg user"><div class="bubble">${esc(item.content)}</div></div>`;
      } else if (item.role === 'assistant') {
        html += `<div class="msg"><div class="bot">✦</div><div class="msgtext">${formatText(item.content)}</div></div>`;
      }
    }
    body.innerHTML = html;
    body.scrollTop = body.scrollHeight;
  }

  function formatText(text) {
    // Safe, lightweight formatting for the prototype. No innerHTML from user text.
    return esc(text).replace(/\n/g, '<br>');
  }

  function setAI(open) {
    state.aiOpen = open;
    root.classList.toggle('ai-open', open);
    root.classList.toggle('ai-viewport-mode', open);
    const panel = root.querySelector('.ai-panel');
    if (panel) panel.setAttribute('aria-hidden', String(!open));
    if (open) setTimeout(() => root.querySelector('#ai-input')?.focus(), 50);
  }

  function toggleSidebar() {
    if (root.clientWidth <= 800) {
      state.mobileSidebarOpen = !state.mobileSidebarOpen;
      root.classList.toggle('mobile-sidebar-open', state.mobileSidebarOpen);
      return;
    }
    state.sidebarCollapsed = !state.sidebarCollapsed;
    root.classList.toggle('sidebar-collapsed', state.sidebarCollapsed);
  }

  function closeMobileSidebar() {
    state.mobileSidebarOpen = false;
    root.classList.remove('mobile-sidebar-open');
  }

  function sendMessage() {
    const input = root.querySelector('#ai-input');
    const text = input?.value?.trim();
    if (!text) return;
    input.value = '';
    input.disabled = true;
    const send = root.querySelector('#ai-send');
    if (send) send.disabled = true;

    // One event -> one Streamlit rerun -> Python updates chat_history.
    setTriggerValue('chat_submit', {
      message: text,
      page: state.page,
      ts: Date.now(),
    });
  }

  if (!state.handlersBound) {
    state.handlersBound = true;

    root.addEventListener('click', (event) => {
      const nav = event.target.closest('.nav-item');
      if (nav) {
        renderPage(nav.dataset.page);
        closeMobileSidebar();
        return;
      }
      if (event.target.closest('#sidebar-toggle')) { toggleSidebar(); return; }
      if (event.target.closest('#desktop-menu-button')) { toggleSidebar(); return; }
      if (event.target.closest('#mobile-menu-button')) { toggleSidebar(); return; }
      if (event.target.closest('#desktop-ai-button')) { setAI(true); return; }
      if (event.target.closest('#mobile-ai-button')) { setAI(true); return; }
      if (event.target.closest('#ai-close')) { setAI(false); return; }
      if (event.target.closest('#ai-send')) { sendMessage(); return; }
      if (event.target === overlay) { closeMobileSidebar(); }
    });

    root.addEventListener('keydown', (event) => {
      if (event.target?.id === 'ai-input' && event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
      }
    });

    const resizeObserver = new ResizeObserver(() => applyResponsiveMode());
    resizeObserver.observe(root);
    state.resizeObserver = resizeObserver;
  }

  // If Python reran, keep the same component instance and only refresh data-driven content.
  if (state.lastResponseVersion !== responseVersion) {
    state.lastResponseVersion = responseVersion;
    renderHistory();
    const input = root.querySelector('#ai-input');
    const send = root.querySelector('#ai-send');
    if (input) input.disabled = false;
    if (send) send.disabled = false;
  }

  applyResponsiveMode();
  renderPage(state.page);
  root.classList.toggle('sidebar-collapsed', state.sidebarCollapsed);
  root.classList.toggle('mobile-sidebar-open', state.mobileSidebarOpen);
  root.classList.toggle('ai-open', state.aiOpen);
}
