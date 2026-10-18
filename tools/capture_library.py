#!/usr/bin/env python3
"""Capture the reference library: above-the-fold screenshots + computed type/colour facts.

Usage: python3 tools/capture_library.py [--only key1,key2] [--out library/shots]
Writes library/shots/<key>_desk.png (1440x900 @1x), <key>_phone.png (390x844 @2x)
and library/shots/facts.json (fonts, sizes, tracking, colours, backdrop-filter use).
"""
import argparse
import json
import pathlib

from playwright.sync_api import sync_playwright

SITES = [
    ("apple_ios", "https://www.apple.com/os/ios/"),
    ("apple_iphone", "https://www.apple.com/iphone/"),
    ("linear", "https://linear.app/"),
    ("vercel", "https://vercel.com/"),
    ("stripe", "https://stripe.com/en-us"),
    ("raycast", "https://www.raycast.com/"),
    ("arc", "https://arc.net/"),
    ("framer", "https://www.framer.com/"),
    ("family", "https://family.co/"),
    ("rauno", "https://rauno.me/"),
    ("resend", "https://resend.com/"),
    ("cal", "https://cal.com/"),
    ("supabase", "https://supabase.com/"),
    ("mercury", "https://mercury.com/"),
    ("attio", "https://attio.com/"),
    ("tremor", "https://www.tremor.so/"),
    ("shadcn_dash", "https://ui.shadcn.com/examples/dashboard"),
    ("lusion", "https://lusion.co/"),
]

FACTS_JS = r"""
() => {
  const pick = (el) => {
    if (!el) return null;
    const s = getComputedStyle(el);
    return {tag: el.tagName.toLowerCase(), text: (el.innerText || '').trim().slice(0, 80),
      font: s.fontFamily.split(',').slice(0, 2).join(',').trim(), size: s.fontSize, weight: s.fontWeight,
      tracking: s.letterSpacing, leading: s.lineHeight, color: s.color};
  };
  // biggest visible text element above the fold
  let best = null, bestSize = 0;
  for (const el of document.querySelectorAll('h1,h2,h3,p,span,div,a')) {
    if (!el.childNodes.length) continue;
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2);
    if (!hasText) continue;
    const r = el.getBoundingClientRect();
    if (r.top > innerHeight || r.bottom < 0 || r.width === 0) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs > bestSize) { bestSize = fs; best = el; }
  }
  const bodyText = [...document.querySelectorAll('p')].find(p => {
    const r = p.getBoundingClientRect(); return r.top < innerHeight && r.width > 200 && p.innerText.trim().length > 40;
  });
  const btn = [...document.querySelectorAll('a,button')].find(b => {
    const s = getComputedStyle(b); const r = b.getBoundingClientRect();
    return r.top < innerHeight && r.height > 28 && r.height < 70 && s.backgroundColor !== 'rgba(0, 0, 0, 0)' && b.innerText.trim().length > 1;
  });
  let backdrop = 0;
  for (const el of document.querySelectorAll('*')) {
    const s = getComputedStyle(el);
    if ((s.backdropFilter && s.backdropFilter !== 'none') || (s.webkitBackdropFilter && s.webkitBackdropFilter !== 'none')) backdrop++;
  }
  const fonts = new Set(); document.fonts.forEach(f => { if (f.status === 'loaded') fonts.add(f.family.replace(/"/g, '')); });
  const btnStyle = btn ? (() => { const s = getComputedStyle(btn); return {text: btn.innerText.trim().slice(0, 40), bg: s.backgroundColor, color: s.color, radius: s.borderRadius, height: btn.getBoundingClientRect().height, font: s.fontSize + ' ' + s.fontWeight}; })() : null;
  return {title: document.title, bodyBg: getComputedStyle(document.body).backgroundColor,
    htmlBg: getComputedStyle(document.documentElement).backgroundColor,
    hero: pick(best), body: pick(bodyText), button: btnStyle, backdropFilterEls: backdrop,
    fontsLoaded: [...fonts].slice(0, 8)};
}
"""

CONSENT = ["Accept all", "Accept All", "Accept", "Allow all", "I agree", "Agree", "Got it", "OK"]


def dismiss(pg):
    for label in CONSENT:
        try:
            b = pg.get_by_role("button", name=label, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(timeout=1500)
                pg.wait_for_timeout(600)
                return
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parent.parent / "library" / "shots"))
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    facts_path = out / "facts.json"
    facts = json.loads(facts_path.read_text()) if facts_path.exists() else {}
    only = set(filter(None, a.only.split(",")))
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader"])  # without these, DPR 2 headless mis-renders backdrop-filter in the lower half
        for key, url in SITES:
            if only and key not in only:
                continue
            for tag, vp, dpr in [("desk", {"width": 1440, "height": 900}, 1), ("phone", {"width": 390, "height": 844}, 2)]:
                ctx = b.new_context(viewport=vp, device_scale_factor=dpr, locale="en-US",
                                    user_agent=None if tag == "desk" else
                                    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
                                    is_mobile=(tag == "phone"), has_touch=(tag == "phone"))
                pg = ctx.new_page()
                try:
                    pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                    try:
                        pg.wait_for_load_state("networkidle", timeout=12000)
                    except Exception:
                        pass
                    pg.wait_for_timeout(3500)
                    dismiss(pg)
                    pg.wait_for_timeout(800)
                    pg.screenshot(path=str(out / f"{key}_{tag}.png"), timeout=60000, animations="disabled")
                    if tag == "desk":
                        f = pg.evaluate(FACTS_JS)
                        f["url"] = url
                        facts[key] = f
                    print("ok", key, tag, pg.title()[:60], flush=True)
                except Exception as e:
                    print("ERR", key, tag, str(e)[:160], flush=True)
                ctx.close()
        b.close()
    facts_path.write_text(json.dumps(facts, indent=1))


if __name__ == "__main__":
    main()
