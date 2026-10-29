// Runs inside the page. Returns every piece of text an AI reader gets but a human can't see.
// No judgement here: rules/ and judge/ decide what the ghosts mean.
() => {
  const INVIS = /[​-‏‪-‮⁠-⁤⁦-⁩﻿]|[\u{E0000}-\u{E007F}]/u;
  const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'HEAD', 'TITLE']);
  const styles = new Map();
  const cs = (el) => { let s = styles.get(el); if (!s) { s = getComputedStyle(el); styles.set(el, s); } return s; };
  const up = (el) => el.parentElement || (el.getRootNode() instanceof ShadowRoot ? el.getRootNode().host : null);
  const doc = document.documentElement;
  const docW = Math.max(doc.scrollWidth, innerWidth), docH = Math.max(doc.scrollHeight, innerHeight);

  const selector = (el) => {
    const parts = [];
    for (let e = el; e && e.nodeType === 1 && parts.length < 5; e = up(e)) {
      if (e.id) { parts.unshift(`${e.localName}#${e.id}`); break; }
      const same = e.parentElement ? [...e.parentElement.children].filter((c) => c.localName === e.localName) : [];
      parts.unshift(same.length > 1 ? `${e.localName}:nth-of-type(${same.indexOf(e) + 1})` : e.localName);
    }
    return parts.join(' > ');
  };
  const box = (r) => ({ x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height) });

  const rgba = (c) => { const m = c.match(/[\d.]+/g) || [0, 0, 0, 0]; return [+m[0], +m[1], +m[2], m[3] === undefined ? 1 : +m[3]]; };
  const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  // Effective background colour, or null when a background image makes it unknowable.
  const background = (el) => {
    for (let e = el; e; e = up(e)) {
      const s = cs(e);
      if (s.backgroundImage !== 'none') return null;
      const c = rgba(s.backgroundColor);
      if (c[3] > 0.5) return c;
    }
    return [255, 255, 255, 1];
  };

  // Hidden by the element or an ancestor: returns [technique, the element that hides it].
  const hiddenBy = (el) => {
    let opacity = 1;
    for (let e = el; e; e = up(e)) {
      const s = cs(e);
      if (s.display === 'none') return ['H1', e];
      opacity *= parseFloat(s.opacity);
      if (opacity < 0.05) return ['H2', e];
      if (s.clip === 'rect(0px, 0px, 0px, 0px)' || /inset\(\s*(50|100)%/.test(s.clipPath)) return ['H6', e];
      if (/^matrix\(0, 0, 0, 0,/.test(s.transform)) return ['H7', e];
    }
    if (cs(el).visibility === 'hidden') return ['H1', el];
    return null;
  };

  // Techniques that apply to the text itself rather than an ancestor.
  const hiddenText = (node, el) => {
    const s = cs(el), found = [];
    const range = document.createRange();
    range.selectNodeContents(node);
    const r = range.getBoundingClientRect(), b = box(r);
    if (parseFloat(s.fontSize) < 2) found.push('H3');
    else if (r.width * r.height < 4) found.push('H6');
    if (b.x + b.w <= 0 || b.y + b.h <= 0 || b.x >= docW || b.y >= docH) found.push('H5');
    const fg = rgba(s.color);
    if (fg[3] < 0.05) found.push('H2');
    else {
      const bg = background(el);
      if (bg) {
        const [a, c] = [lum(fg), lum(bg)].sort((x, y) => y - x);
        if ((a + 0.05) / (c + 0.05) < 1.2) found.push('H4');
      }
    }
    // Covered by another element. Only checked on screen, and fixed/sticky bars are ignored: they cover text only until you scroll.
    if (!found.length && r.width && r.top >= 0 && r.bottom <= innerHeight && el.getRootNode() === document) {
      const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      if (top && top !== el && !el.contains(top) && !top.contains(el)) {
        let fixed = false;
        for (let e = top; e; e = up(e)) if (/fixed|sticky/.test(cs(e).position)) { fixed = true; break; }
        if (!fixed) found.push('H8');
      }
    }
    return [found, b];
  };

  const roots = [document];
  for (let i = 0; i < roots.length; i++) for (const el of roots[i].querySelectorAll('*')) if (el.shadowRoot) roots.push(el.shadowRoot);

  const ghosts = [], grouped = new Map();
  const add = (key, g) => {
    const prev = key && grouped.get(key);
    if (prev) { prev.text += ' ' + g.text; return ghosts.indexOf(prev); }
    ghosts.push(g);
    if (key) grouped.set(key, g);
    return ghosts.length - 1;
  };

  // Page text in reading order, each piece tagged with its ghost (or -1), so the cleaner can rebuild the page without the bad ones.
  const reading = [];
  const isBlock = (e) => !/^inline/.test(cs(e).display) && cs(e).display !== 'contents';
  const blockOf = (el) => { for (let e = el; e; e = up(e)) if (isBlock(e)) return e; return null; };
  let lastBlock = null;
  const read = (text, el, ghost) => {
    const b = blockOf(el);
    reading.push({ text, ghost, sep: b === lastBlock ? ' ' : '\n' });
    lastBlock = b;
  };

  let textNodes = 0;
  for (const root of roots) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_COMMENT);
    for (let node; (node = walker.nextNode());) {
      const text = node.nodeValue.trim();
      if (!text) continue;
      const el = node.parentElement || root.host;
      if (node.nodeType === Node.COMMENT_NODE) {
        add(null, { text, technique: ['H10'], views: ['raw_html'], selector: el ? selector(el) : '', box: null });
        continue;
      }
      if (!el || el.closest('script,style,noscript,template,head')) continue;
      textNodes++;
      const invisible = INVIS.test(text);
      const ancestor = hiddenBy(el);
      if (ancestor) {
        const [t, by] = ancestor;
        read(text, el, add(by, { text, technique: invisible ? [t, 'H9'] : [t], views: ['dom_text'], selector: selector(by), box: null }));
        continue;
      }
      const [found, b] = hiddenText(node, el);
      if (invisible) found.push('H9');
      read(text, el, found.length ? add(null, { text, technique: found, views: ['dom_text'], selector: selector(el), box: b }) : -1);
    }

    for (const el of root.querySelectorAll('noscript')) {
      const text = el.textContent.trim();
      if (text) add(null, { text, technique: ['H13'], views: ['dom_text', 'raw_html'], selector: selector(el), box: null });
    }
    for (const el of root.querySelectorAll('template')) {
      const text = el.content.textContent.trim();
      if (text) add(null, { text, technique: ['H13'], views: ['raw_html'], selector: selector(el), box: null });
    }
    for (const el of root.querySelectorAll('input[type=hidden]')) {
      const text = el.value.trim();
      if (/\s/.test(text)) add(null, { text, technique: ['H13'], views: ['raw_html'], selector: selector(el), box: null });
    }
    for (const el of root.querySelectorAll('[alt],[title],[aria-label],[aria-description]')) {
      if (el.closest('head')) continue;
      for (const a of ['alt', 'title', 'aria-label', 'aria-description']) {
        const text = (el.getAttribute(a) || '').trim();
        if (text) add(null, { text, technique: ['H11'], attribute: a, views: ['raw_html'], selector: selector(el), box: null });
      }
    }
  }
  for (const el of document.querySelectorAll('meta[name=description],meta[property="og:description"],meta[name="twitter:description"]')) {
    const text = (el.content || '').trim();
    if (text) add(null, { text, technique: ['H11'], attribute: 'content', views: ['raw_html'], selector: selector(el), box: null });
  }

  return { ghosts, reading, stats: { elements: document.querySelectorAll('*').length, text_nodes: textNodes, shadow_roots: roots.length - 1 } };
}
