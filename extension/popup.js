// Popup: what the shield removed from the current tab. Page text is shown with textContent only.
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };

(async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const settings = await chrome.storage.local.get({ enabled: true, judge: true });
  for (const k of ['enabled', 'judge']) {
    const box = document.getElementById(k);
    box.checked = settings[k];
    box.addEventListener('change', () => chrome.storage.local.set({ [k]: box.checked }));
  }

  const key = `tab${tab.id}`;
  const store = await chrome.storage.session.get({ [key]: { frames: {} } });
  const frames = Object.values(store[key].frames);
  const blocked = frames.flatMap((f) => f.blocked);
  const offline = frames.some((f) => f.judge === 'offline');
  const summary = document.getElementById('summary');
  const list = document.getElementById('list');

  if (!settings.enabled) summary.textContent = 'Shield is off.';
  else if (!frames.length) summary.textContent = 'Nothing scanned here yet. Reload the page.';
  else if (!blocked.length) summary.textContent = 'No hidden instructions found on this page.';
  else {
    summary.textContent = `Removed ${blocked.length} hidden instruction${blocked.length === 1 ? '' : 's'} before your AI could read ${blocked.length === 1 ? 'it' : 'them'}.`;
    summary.className = 'bad';
  }
  if (offline) summary.textContent += ' AI judge offline: rules only.';

  if (!blocked.length) list.replaceWith(el('p', 'empty', 'Ghosts this shield removes from the page show up here.'));
  for (const b of blocked) {
    const li = el('li');
    li.appendChild(el('div', 'text', b.text));
    const meta = el('div', 'meta');
    meta.appendChild(el('span', `tag ${b.label}`, b.label === 'injection' ? 'Attack' : 'Worth a look'));
    meta.appendChild(document.createTextNode(` · found by ${b.by === 'judge' ? 'the AI judge' : 'rules'} · ${b.reason}`));
    li.appendChild(meta);
    list.appendChild(li);
  }
})();
