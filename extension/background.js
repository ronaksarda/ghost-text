// Service worker: keeps each tab's report, sets the badge, and talks to the Ghost Text judge
// (only here, so page CORS rules don't apply and pages never see the API).
importScripts('gen.js');

chrome.runtime.onMessage.addListener((msg, sender, reply) => {
  if (msg.type === 'report' && sender.tab) {
    const key = `tab${sender.tab.id}`;
    chrome.storage.session.get({ [key]: { frames: {} } }).then((store) => {
      const tab = store[key];
      tab.frames[sender.frameId] = { blocked: msg.blocked, judge: msg.judge };
      const n = Object.values(tab.frames).reduce((s, f) => s + f.blocked.length, 0);
      chrome.action.setBadgeText({ tabId: sender.tab.id, text: n ? String(n) : '' });
      chrome.action.setBadgeBackgroundColor({ tabId: sender.tab.id, color: '#e0142f' });
      chrome.storage.session.set({ [key]: tab });
    });
    return false;
  }
  if (msg.type === 'judge') {
    fetch(`${GHOST_API}/judge`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ghosts: msg.ghosts }) })
      .then((r) => (r.ok ? r.json() : null)).then(reply, () => reply(null));
    return true;  // answer asynchronously
  }
  return false;
});

// A new page in the tab starts a new report.
chrome.tabs.onUpdated.addListener((tabId, info) => {
  if (info.status === 'loading') chrome.storage.session.remove(`tab${tabId}`);
});
chrome.tabs.onRemoved.addListener((tabId) => chrome.storage.session.remove(`tab${tabId}`));
