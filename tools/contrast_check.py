#!/usr/bin/env python3
"""WCAG AA text-contrast check that understands glass.

For every visible text node it composites the background layers under the text. When it meets
a glass element (backdrop-filter set) it treats whatever is behind the glass as unknown and tests
the worst cases: pure black AND pure white behind the glass fill. Text passes only if both pass.
Thresholds: 4.5:1 normal text, 3:1 large text (>= 24px, or >= 18.66px bold).
Not covered (check by eye): background images and gradients (only the colour layer is used), text in
pseudo-elements (::before labels, arrows), placeholders, ancestor opacity, and anything inside
[aria-hidden=true] or [data-contrast-skip].

Usage: python3 tools/contrast_check.py URL [URL ...] [--themes light,dark] [--phone] [--accents all|blue,teal,...]
Exit 1 if any text fails. Works on any page, not only the kit's templates (theme via ?theme=, accent via ?accent=).
By default only the template's own accent is checked. --accents all repeats every run once per advertised accent
preset (blue is the default look; teal, green, orange, graphite are the data-accent presets in glass.css), because
an accent changes the text colour AND the chip tint behind it, so one preset passing says nothing about the others.
"""
import argparse
import sys
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const parse = (c) => {
    let m = c.match(/rgba?\(([^)]+)\)/);
    if (m) { const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; }
    m = c.match(/color\(srgb ([^)]+)\)/);   /* color-mix(in srgb, ...) serialises like this */
    if (m) { const p = m[1].split(/[ \/]+/).filter(Boolean).map(Number); return [p[0] * 255, p[1] * 255, p[2] * 255, p.length > 3 ? p[3] : 1]; }
    m = c.match(/okl(ab|ch)\(([^)]+)\)/);    /* color-mix(in oklab, ...) serialises as oklab() */
    if (m) {
      const p = m[2].split(/[ \/]+/).filter(Boolean).map(v => v.endsWith('%') ? parseFloat(v) / 100 : parseFloat(v));
      let L = p[0], A = p[1], B = p[2]; const alpha = p.length > 3 ? p[3] : 1;
      if (m[1] === 'ch') { const h = B * Math.PI / 180; const C = A; A = C * Math.cos(h); B = C * Math.sin(h); }
      const l = Math.pow(L + 0.3963377774 * A + 0.2158037573 * B, 3), mm = Math.pow(L - 0.1055613458 * A - 0.0638541728 * B, 3),
            s = Math.pow(L - 0.0894841775 * A - 1.2914855480 * B, 3);
      const lin = [4.0767416621 * l - 3.3077115913 * mm + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * mm - 0.3413193965 * s,
                   -0.0041960863 * l - 0.7034186147 * mm + 1.7076147010 * s];
      const enc = v => { v = Math.min(1, Math.max(0, v)); return 255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055); };
      return [enc(lin[0]), enc(lin[1]), enc(lin[2]), alpha];
    }
    return null;
  };
  const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const over = (top, base) => { const a = top[3]; return [0, 1, 2].map(i => top[i] * a + base[i] * (1 - a)).concat(1); };
  const pageBg = parse(getComputedStyle(document.body).backgroundColor) || [255, 255, 255, 1];
  const base = pageBg[3] === 0 ? (parse(getComputedStyle(document.documentElement).backgroundColor) || [255,255,255,1]) : pageBg;
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const el = t.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
    if (el.closest('[aria-hidden="true"],[data-contrast-skip],script,style,noscript,svg,dialog:not([open]),[hidden]')) continue;
    const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    let fg = parse(cs.color); if (!fg) continue;
    const layers = []; let glass = false; let n = el; let opaque = null;
    while (n && n.nodeType === 1) {
      const s = getComputedStyle(n);
      const bg = parse(s.backgroundColor);
      if (bg && bg[3] > 0) { if (bg[3] >= 0.999) { opaque = bg; break; } layers.push(bg); }
      const bf = s.backdropFilter || s.webkitBackdropFilter;
      if (bf && bf !== 'none') { glass = true; break; }
      n = n.parentElement;
    }
    const bases = opaque ? [opaque] : (glass ? [[0,0,0,1], [255,255,255,1]] : [base]);
    let worst = 99, worstBg = null;
    for (const b of bases) {
      let c = b; for (let i = layers.length - 1; i >= 0; i--) c = over(layers[i], c);
      const f = fg[3] < 1 ? over(fg, c) : fg;
      const k = ratio(f, c); if (k < worst) { worst = k; worstBg = c; }
    }
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10);
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    const cls = (el.className && typeof el.className === 'string') ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    out.push({ ok: worst >= need, ratio: Math.round(worst * 100) / 100, need, glass, el: el.tagName.toLowerCase() + cls,
      text: t.textContent.trim().slice(0, 40), fg: cs.color, bg: worstBg ? 'rgb(' + worstBg.slice(0, 3).map(Math.round).join(',') + ')' : '' });
  }
  return out;
}
"""


ACCENTS = ["blue", "teal", "green", "orange", "graphite"]   # the ?accent= values glass.js / glass.css support


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--themes", default="light,dark")
    ap.add_argument("--phone", action="store_true", help="390x844 instead of 1440x900")
    ap.add_argument("--all", action="store_true", help="print passing rows too")
    ap.add_argument("--accents", default="", help="'all' or a comma list of ?accent= values to run each page under (default: the page's own accent)")
    a = ap.parse_args()
    accents = ACCENTS if a.accents == "all" else [x for x in a.accents.split(",") if x]
    for x in accents:
        if x not in ACCENTS:
            ap.error(f"unknown accent '{x}' (supported: {', '.join(ACCENTS)})")
    fails = 0
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        vp = {"width": 390, "height": 844} if a.phone else {"width": 1440, "height": 900}
        for url in a.urls:
            for accent in (accents or [None]):
                for theme in a.themes.split(","):
                    pg = b.new_page(viewport=vp)
                    sep = "&" if "?" in url else "?"
                    q = f"theme={theme}" + (f"&accent={accent}" if accent else "")
                    pg.goto(f"{url}{sep}{q}", wait_until="networkidle")
                    pg.wait_for_timeout(1200)
                    rows = pg.evaluate(JS)
                    bad = [r for r in rows if not r["ok"]]
                    glass_rows = [r for r in rows if r["glass"]]
                    min_glass = min((r["ratio"] for r in glass_rows), default=None)
                    tag = f"[{theme}{', ' + accent if accent else ''}]"
                    print(f"{url} {tag} {len(rows)} text nodes, {len(bad)} below AA; on glass: {len(glass_rows)} (min {min_glass})")
                    for r in (rows if a.all else bad):
                        print(f"   {'ok ' if r['ok'] else 'FAIL'} {r['ratio']:>5} / {r['need']}  {'glass ' if r['glass'] else ''}{r['el']}  '{r['text']}'  fg {r['fg']} on {r['bg']}")
                    fails += len(bad)
                    pg.close()
        b.close()
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
