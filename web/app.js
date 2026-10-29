// Ghost Text front end. Every string from a scan is hostile: it is only ever set with textContent.
const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };

const TECHNIQUE = {
  H1: 'hidden with display:none or visibility', H2: 'fully transparent', H3: 'text too small to see',
  H4: 'same colour as the background', H5: 'pushed off the screen', H6: 'clipped to nothing',
  H7: 'shrunk to zero size', H8: 'covered by another element', H9: 'invisible Unicode characters',
  H10: 'HTML comment', H11: 'attribute only machines read', H13: 'noscript, template or hidden input',
};
const LABEL = { injection: 'Attack', suspicious: 'Worth a look', benign: 'Harmless' };
const VIEW = { dom_text: 'in the page text', raw_html: 'in the HTML source only' };
const VERDICT = {
  haunted: ['Haunted', (n) => `This page hides ${n} instruction${n === 1 ? '' : 's'} aimed at AI. Don't let an agent read it raw.`],
  uneasy: ['Uneasy', () => 'Some hidden text looks odd. Nothing is clearly an attack, but read the flagged items.'],
  clean: ['Clean', () => 'No hidden instructions found in what we could scan.'],
};
const STEPS = ['Opening the page in a real browser', 'Finding text people can\'t see', 'Judging each hidden piece'];

let current = null;

// Tabs: web address or pasted HTML.
for (const [tab, other] of [['tab-url', 'tab-html'], ['tab-html', 'tab-url']]) {
  $(tab).addEventListener('click', () => {
    $(tab).setAttribute('aria-selected', 'true'); $(other).setAttribute('aria-selected', 'false');
    $(`panel-${tab.slice(4)}`).hidden = false; $(`panel-${other.slice(4)}`).hidden = true;
    $(tab === 'tab-url' ? 'url' : 'html').focus();
  });
}

$('scan').addEventListener('submit', (e) => {
  e.preventDefault();
  if (!$('panel-url').hidden) {
    let url = $('url').value.trim();
    if (!url) return showError('Type a web address to scan.');
    if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
    run({ url });
  } else {
    const html = $('html').value;
    if (!html.trim()) return showError('Paste some HTML to scan.');
    run({ html });
  }
});

for (const b of document.querySelectorAll('[data-demo]')) {
  b.addEventListener('click', () => run(null, b.dataset.demo));
}

async function run(body, demo) {
  const buttons = document.querySelectorAll('.go, [data-demo]');
  buttons.forEach((b) => (b.disabled = true));
  $('result').hidden = true;
  const stop = progress();
  try {
    const r = demo ? await fetch(`/demo-results/${demo}.json`)
      : await fetch('/scan', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    const data = await r.json().catch(() => ({}));
    stop();
    if (!r.ok) return showError(data.detail || `The scan failed (HTTP ${r.status}). Try again, or use Paste HTML.`);
    current = { data, body: demo ? { url: location.origin + `/demo/${demo}.html` } : body };
    render(data);
  } catch {
    stop();
    showError('Could not reach Ghost Text. Check your connection and try again.');
  } finally {
    buttons.forEach((b) => (b.disabled = false));
  }
}

// The scan is one request, so steps advance on typical timings; the list says what is happening, in order.
function progress() {
  const box = $('status');
  box.hidden = false; box.replaceChildren();
  const list = el('ol');
  const items = STEPS.map((s) => list.appendChild(el('li', null, s)));
  box.appendChild(list);
  let i = 0;
  const mark = () => items.forEach((li, j) => { li.className = j < i ? 'done' : ''; j === i ? li.setAttribute('aria-current', 'step') : li.removeAttribute('aria-current'); });
  mark();
  const t = setInterval(() => { if (i < STEPS.length - 1) { i++; mark(); } }, 3500);
  return () => { clearInterval(t); box.hidden = true; };
}

function showError(msg) {
  const box = $('status');
  box.hidden = false;
  box.replaceChildren(el('p', 'error', msg));
}

function render(d) {
  const hostile = d.ghosts.filter((g) => g.label !== 'benign').sort((a, b) => (a.label === 'injection' ? -1 : 1) - (b.label === 'injection' ? -1 : 1));
  const benign = d.ghosts.filter((g) => g.label === 'benign');
  const [word, line] = VERDICT[d.verdict];
  $('verdict').dataset.v = d.verdict;
  $('verdict-word').textContent = word;
  $('verdict-line').textContent = line(d.ghosts.filter((g) => g.label === 'injection').length);
  $('judge-note').hidden = d.judge !== 'offline';

  $('ghost-heading').textContent = hostile.length
    ? `${hostile.length} hidden piece${hostile.length === 1 ? '' : 's'} flagged`
    : 'Nothing flagged';
  $('ghost-list').replaceChildren(...hostile.map(item));
  $('benign-wrap').hidden = !benign.length;
  $('benign-summary').textContent = `${benign.length} harmless hidden piece${benign.length === 1 ? '' : 's'} (skip links, menus, image descriptions)`;
  $('benign-list').replaceChildren(...benign.map(item));

  const un = $('unscannable');
  un.hidden = !d.unscannable.length && !d.partial && !d.truncated;
  un.replaceChildren();
  if (d.partial) un.appendChild(el('p', null, 'The page kept loading past our 20 second limit, so this scan covers what had loaded.'));
  if (d.truncated) un.appendChild(el('p', null, 'This page has more hidden text than we check in one scan. Only the first 500 pieces are shown.'));
  if (d.unscannable.length) {
    un.appendChild(el('p', null, 'We could not look inside these parts of the page:'));
    const ul = el('ul');
    for (const u of d.unscannable) ul.appendChild(el('li', null, u.kind === 'cross_origin_iframe' ? `Embedded frame from ${u.src}` : `Sealed component at ${u.selector}`));
    un.appendChild(ul);
  }

  const img = $('shot'), inner = $('shot-inner');
  inner.querySelectorAll('.box').forEach((b) => b.remove());
  $('shot-wrap').hidden = !d.screenshot;
  if (d.screenshot) {
    img.onload = () => {
      for (const g of d.ghosts) {
        if (!g.box || !g.box.w) continue;
        const b = el('button', 'box' + (g.label === 'benign' ? '' : ' hostile'));
        b.type = 'button';
        b.dataset.id = g.id;
        b.setAttribute('aria-label', `Show hidden text: ${g.text.slice(0, 80)}`);
        Object.assign(b.style, {
          left: `${(g.box.x / img.naturalWidth) * 100}%`, top: `${(g.box.y / img.naturalHeight) * 100}%`,
          width: `${(g.box.w / img.naturalWidth) * 100}%`, height: `${(g.box.h / img.naturalHeight) * 100}%`,
        });
        b.addEventListener('click', () => select(g.id, 'list'));
        inner.appendChild(b);
      }
    };
    img.src = d.screenshot;
    img.alt = 'Screenshot of the scanned page';
    const boxed = d.ghosts.filter((g) => g.box && g.box.w).length;
    $('shot-caption').textContent = boxed
      ? `Outlined: ${boxed} piece${boxed === 1 ? '' : 's'} with a position on the page. The rest have no visible spot at all.`
      : 'None of the hidden text has a visible spot on the page: it lives in hidden elements, attributes or invisible characters.';
  }

  $('result').hidden = false;
  $('verdict-word').setAttribute('tabindex', '-1');
  $('verdict-word').focus({ preventScroll: true });
  $('result').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
}

function item(g) {
  const li = el('li', 'ghost');
  li.dataset.label = g.label; li.dataset.id = g.id; li.tabIndex = 0;
  li.appendChild(el('p', 'ghost-text', g.text));
  const meta = el('div', 'ghost-meta');
  meta.appendChild(el('span', 'tag', LABEL[g.label]));
  meta.appendChild(el('span', null, g.technique.map((t) => TECHNIQUE[t] || t).join(', ')));
  meta.appendChild(el('span', null, g.views.map((v) => VIEW[v] || v).join(', ')));
  if (g.decoded_from) meta.appendChild(el('span', 'decoded', 'decoded from invisible Unicode tags'));
  li.appendChild(meta);
  if (g.label !== 'benign') li.appendChild(el('p', 'ghost-reason', `Why: ${g.reason}.`));
  if (g.visible_text) li.appendChild(el('p', 'ghost-reason', `Hidden inside the visible sentence "${g.visible_text}"`));
  li.addEventListener('click', () => select(g.id, 'shot'));
  li.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(g.id, 'shot'); } });
  return li;
}

function select(id, scrollTo) {
  document.querySelectorAll('.ghost.on, .box.on').forEach((n) => n.classList.remove('on'));
  const row = document.querySelector(`.ghost[data-id="${id}"]`);
  const box = document.querySelector(`.box[data-id="${id}"]`);
  if (row) { row.classList.add('on'); if (row.closest('details')) row.closest('details').open = true; }
  if (box) box.classList.add('on');
  const target = scrollTo === 'shot' ? box : row;
  if (target) target.scrollIntoView({ block: 'center', behavior: 'smooth' });
}

function copy(text, what) {
  navigator.clipboard.writeText(text).then(() => { $('copied').textContent = `${what} copied.`; setTimeout(() => ($('copied').textContent = ''), 2500); },
    () => { $('copied').textContent = 'Copy failed. Select the text and copy it by hand.'; });
}
$('copy-clean').addEventListener('click', () => current && copy(current.data.clean_text, 'Clean text'));
$('copy-json').addEventListener('click', () => {
  if (!current) return;
  const { screenshot, ...rest } = current.data;  // a screenshot is megabytes of base64 nobody wants on the clipboard
  copy(JSON.stringify(rest, null, 2), 'JSON');
});
$('copy-curl').addEventListener('click', () => {
  if (!current) return;
  const payload = current.body.url ? JSON.stringify({ url: current.body.url }) : '{"html": "<paste your HTML here>"}';
  copy(`curl -X POST ${location.origin}/scan -H "Content-Type: application/json" -d '${payload.replace(/'/g, "'\\''")}'`, 'curl command');
});

$('api-example').textContent = $('api-example').textContent.replace('https://ghosttext.example', location.origin);
