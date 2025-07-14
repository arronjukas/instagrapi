// Store Discord auth token received from content script
let authToken = null;

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'token') {
    authToken = msg.token;
  } else if (msg.type === 'export') {
    if (!authToken) {
      console.error('No token available');
      return;
    }
    exportChannel(msg.channelId);
  }
});

async function exportChannel(channelId) {
  const fileName = `discord-${channelId}.html`;
  // Accumulate HTML chunks in memory and download when complete
  const chunks = [];

  const header = `<!doctype html><meta charset="utf-8"><body>`;
  const footer = `</body>`;
  chunks.push(header);

  let before = null;
  while (true) {
    const url = `https://discord.com/api/v9/channels/${channelId}/messages?limit=100` + (before ? `&before=${before}` : '');
    const res = await fetch(url, { headers: { authorization: authToken } });
    if (res.status === 429) {
      const data = await res.json();
      await delay((data.retry_after || 1) * 1000);
      continue;
    }
    const messages = await res.json();
    if (!messages.length) break;
    before = messages[messages.length - 1].id;
    const html = messages.map(renderMessage).join('\n');
    chunks.push(html);
    await delay(100); // gentle pacing
  }

  chunks.push(footer);
  const blob = new Blob(chunks, { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  chrome.downloads.download({ url, filename: fileName, saveAs: true });
}

function renderMessage(m) {
  const time = new Date(m.timestamp).toLocaleString();
  const content = escapeHtml(m.content || '');
  return `<div><span>[${time}]</span> <b>${escapeHtml(m.author.username)}</b>: ${content}</div>`;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}
