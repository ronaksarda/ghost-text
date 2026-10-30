// Content script: find ghosts on this page and remove the hostile ones before an AI assistant reads the page.
// Same detection as the server (gen.js is built from scanner/extract.js and rules/score.py).
// Removing hidden text changes nothing a person sees; it only changes what a machine reads.
(() => {
  const RULES = GHOST_RULES.map(([p, w, r]) => [new RegExp(p, 'is'), w, r]);
  const BASE64 = /[A-Za-z0-9+/]{40,}={0,2}/g;
  const TAGS = /[\u{E0000}-\u{E007F}]/gu, TAG = /[\u{E0000}-\u{E007F}]/u;  // TAG has no g flag: .test() keeps no state
  const ZW = '​‌‍‎‏⁠⁡⁢⁣⁤﻿';
  const BIDI = '‪‫‬‭‮⁦⁧⁨⁩';
  const RTL = /[֐-ࣿ]/;
  const CLASSIFIER = 'talks to the classifier itself';

  const decodeBase64 = (text) => (text.match(BASE64) || []).map((run) => {
    try {
      const s = new TextDecoder('utf-8', { fatal: true }).decode(Uint8Array.from(atob(run + '='.repeat((4 - run.length % 4) % 4)), (c) => c.charCodeAt(0)));
      return s.includes(' ') && !/[\x00-\x08\x0e-\x1f]/.test(s) ? s : '';
    } catch { return ''; }
  }).filter(Boolean).join(' ');

  // Mirrors rules/score.py score() and label().
  function score(text) {
    let miss = 1; const reasons = [];
    const decoded = decodeBase64(text);
    if (decoded) { text += ' ' + decoded; miss *= 0.7; reasons.push('hides base64-encoded text'); }
    for (const [re, w, r] of RULES) if (re.test(text)) { miss *= 1 - w; reasons.push(r); }
    if (text.split(/\s+/).filter(Boolean).length > 25) { miss *= 0.8; reasons.push('long hidden prose'); }
    return [1 - miss, reasons];
  }
  function label(text) {
    const [s, reasons] = score(text);
    let l = s >= GHOST_LIMITS.injection ? 'injection' : s >= GHOST_LIMITS.suspicious ? 'suspicious' : 'benign';
    if (l === 'benign' && reasons.includes(CLASSIFIER)) l = 'suspicious';  // PRD 7.4 floor
    return [l, l === 'benign' ? 'no instruction aimed at an AI' : reasons.join('; ')];
  }

  // Mirrors rules/unicode.py: decode tag smuggling, ignore emoji joiners and RTL marks.
  const decodeTags = (t) => [...t.matchAll(TAGS)].map((m) => m[0].codePointAt(0) - 0xE0000).filter((c) => c >= 0x20 && c <= 0x7E).map((c) => String.fromCharCode(c)).join('');
  const isEmoji = (ch) => /\p{So}/u.test(ch) || ch === '️' || (ch.codePointAt(0) >= 0x1F3FB && ch.codePointAt(0) <= 0x1F3FF);
  function suspiciousInvisibles(text) {
    const chars = [...text], rtl = RTL.test(text);
    return chars.some((ch, i) => {
      if (TAG.test(ch)) return true;
      if (ch === '‍' && i > 0 && i < chars.length - 1 && isEmoji(chars[i - 1]) && isEmoji(chars[i + 1])) return false;
      if (('‎‏' + BIDI).includes(ch) && rtl) return false;
      return (ZW + BIDI).includes(ch);
    });
  }
  const stripInvisibles = (t) => [...t].filter((c) => !(ZW + BIDI).includes(c)).join('').replace(TAGS, '');

  function neutralize(item) {
    const onlyH9 = item.technique.length === 1 && item.technique[0] === 'H9';
    for (const { node, attr } of item.targets) {
      if (!node.isConnected && node.nodeType !== Node.COMMENT_NODE) continue;
      if (attr) { node.removeAttribute(attr); if (attr === 'value') node.value = ''; }
      else if (node.nodeType === Node.COMMENT_NODE) node.remove();
      else if (node.nodeType === Node.TEXT_NODE) node.nodeValue = onlyH9 ? stripInvisibles(node.nodeValue) : '';
      else if (node.localName === 'template') node.content.replaceChildren();
      else node.replaceChildren();  // keep the element so page scripts that reference it keep working
    }
  }

  const blocked = [];
  let judgeState = 'unused', settings = { enabled: true, judge: true };

  function report() {
    chrome.runtime.sendMessage({ type: 'report', blocked, judge: judgeState, top: window === window.top }).catch(() => {});
  }

  function block(item, l, reason, by) {
    neutralize(item);
    blocked.push({ text: item.text.slice(0, 300), label: l, technique: item.technique, reason, by });
  }

  async function scan() {
    if (!settings.enabled) return;
    let result;
    try { result = ghostExtract(true); } catch { return; }
    const askJudge = [];
    result.ghosts.forEach((g, i) => {
      let text = g.text;
      if (g.technique.includes('H9')) {
        const hidden = decodeTags(text);
        if (hidden) text = hidden;
        else if (!suspiciousInvisibles(text)) { g.technique = g.technique.filter((t) => t !== 'H9'); if (!g.technique.length) return; }
        text = stripInvisibles(text).trim() || text;
      }
      const item = { text, technique: g.technique, targets: result.targets[i] };
      const [l, reason] = label(text);
      if (l !== 'benign') block(item, l, reason, 'rules');
      else if (settings.judge && text.split(/\s+/).length >= 6) askJudge.push(item);  // short labels never leave the browser
    });
    if (askJudge.length) {
      const batch = askJudge.slice(0, 50);
      const res = await chrome.runtime.sendMessage({ type: 'judge', ghosts: batch.map((x) => ({ text: x.text, technique: x.technique, context: '' })) }).catch(() => null);
      if (res && res.labels) {
        judgeState = 'online';
        res.labels.forEach(([l, reason], i) => { if (l !== 'benign') block(batch[i], l, reason, 'judge'); });
      } else judgeState = 'offline';  // rules already ran; the page is never left unscanned
    }
    report();
  }

  let timer = null, runs = 0;
  const later = () => { clearTimeout(timer); timer = setTimeout(() => { if (runs++ < 30) scan(); }, 900); };

  chrome.storage.local.get({ enabled: true, judge: true }).then((s) => {
    settings = s;
    scan();
    new MutationObserver(later).observe(document.documentElement, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['style', 'class', 'hidden'] });
  });
})();
