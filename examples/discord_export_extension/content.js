// Grab token from Discord's localStorage and send to background
(function() {
  const tokenRaw = window.localStorage.getItem('token');
  if (tokenRaw) {
    try {
      const token = JSON.parse(tokenRaw);
      chrome.runtime.sendMessage({ type: 'token', token });
    } catch (e) {
      console.error('Token parse failed');
    }
  }

  // Add a simple button into the UI for demonstration
  function addExportButton() {
    if (document.getElementById('dcc-export-btn')) return;
    const toolbar = document.querySelector('[class*="toolbar-"], header');
    if (!toolbar) return;
    const btn = document.createElement('button');
    btn.id = 'dcc-export-btn';
    btn.textContent = 'Export Chat';
    btn.style.marginLeft = '8px';
    btn.onclick = () => {
      const parts = location.pathname.split('/');
      const channelId = parts[parts.length - 1];
      chrome.runtime.sendMessage({ type: 'export', channelId });
    };
    toolbar.appendChild(btn);
  }

  const observer = new MutationObserver(addExportButton);
  observer.observe(document.body, { childList: true, subtree: true });
  addExportButton();
})();
