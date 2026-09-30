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
    boundRoot: null,
    resizeObserver: null,
  });

  function isMobile() {
    return root.clientWidth <= 800;
  }

  function applyResponsiveMode() {
    const mobile = isMobile();
    root.classList.toggle('is-mobile', mobile);
    if (!mobile) {
      state.mobileSidebarOpen = false;
      root.classList.remove('mobile-sidebar-open');
    }
  }

  function esc(value) {
    return String(value ?? '').replace(/[&<>"']/g, ch => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'
    }[ch]));
  }

  function formatText(text) {
    return esc(text).replace(/
/g, '<br>');
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
    let html = `<div class="msg"><div class="bot">✦</div><div class="msgtext"><b>Hi there! 👋</b><br><span class="muted">I'm your Financial AI Assistant.<br>Ask me about the dashboard.</span></div></div>`;
    for (const item of history) {
      if (item.role === 'user') html += `<div class="msg user"><div class="bubble">${esc(item.content)}</div></div>`;
      else if (item.role === 'assistant') html += `<div class="msg"><div class="bot">✦</div><div class="msgtext">${formatText(item.content)}</div></div>`;
    }
    body.innerHTML = html;
    body.scrollTop = body.scrollHeight;
  }

  function setAI(open) {
    state.aiOpen = !!open;
    root.classList.toggle('ai-open', state.aiOpen);
    root.classList.toggle('ai-viewport-mode', state.aiOpen);
    const panel = root.querySelector('.ai-panel');
    if (panel) panel.setAttribute('aria-hidden', String(!state.aiOpen));
    if (state.aiOpen) setTimeout(() => root.querySelector('#ai-input')?.focus(), 80);
  }

  function toggleSidebar() {
    if (isMobile()) {
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
    setTriggerValue('chat_submit', { message: text, page: state.page, ts: Date.now() });
  }

  function bindHandlers() {
    if (state.boundRoot === root) return;
    state.boundRoot = root;

    // Direct button handlers avoid lost delegation when Streamlit remounts the component.
    root.querySelector('#sidebar-toggle')?.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleSidebar();
    });
    root.querySelector('#desktop-ai-button')?.addEventListener('click', () => setAI(true));
    root.querySelector('#mobile-ai-button')?.addEventListener('click', () => setAI(true));
    root.querySelector('#ai-close')?.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      setAI(false);
    });
    root.querySelector('#ai-send')?.addEventListener('click', sendMessage);

    root.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', () => {
        renderPage(item.dataset.page);
        closeMobileSidebar();
      });
    });

    overlay?.addEventListener('click', closeMobileSidebar);

    root.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        if (state.aiOpen) { setAI(false); return; }
        if (state.mobileSidebarOpen) { closeMobileSidebar(); return; }
      }
      if (event.target?.id === 'ai-input' && event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
      }
    });

    state.resizeObserver?.disconnect();
    state.resizeObserver = new ResizeObserver(applyResponsiveMode);
    state.resizeObserver.observe(root);
  }

  bindHandlers();

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
