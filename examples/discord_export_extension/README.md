# Discord Chat Exporter Extension

This directory contains a minimal Chrome extension that exports the currently open Discord chat as an HTML file. It uses your logged-in session so you don't need to manually enter any credentials.

## Files
- `manifest.json` – extension manifest declaring permissions and scripts.
- `content.js` – injected into Discord pages to obtain the auth token and add an **Export Chat** button.
- `background.js` – service worker that fetches messages and saves them as an HTML file.

## Loading the Extension in Chrome
1. Download or clone this repository so you have these files on your computer.
2. Open Chrome and go to `chrome://extensions/`.
3. Enable **Developer mode** (toggle in the top right).
4. Click **Load unpacked** and select this `discord_export_extension` folder.
5. Open Discord in a new tab, navigate to the chat you want to save, then click the **Export Chat** button that appears in the toolbar.
6. The extension will download an HTML file with your chat history in reverse order (newest messages first).

No other setup is required.
