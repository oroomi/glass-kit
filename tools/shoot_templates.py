#!/usr/bin/env python3
"""Screenshot templates at 1440x900 and 390x844, light and dark, above the fold.

Usage: python3 tools/shoot_templates.py [--base http://127.0.0.1:8152] [--pages dashboard,landing] [--out docs/shots] [--full]
Extra: --click "#orb" clicks a selector before the shot (for overlay states), --suffix _pilot names it.

Animations: shots normally use Playwright animations="disabled" so nothing is caught mid-transition. Observed: once a
<dialog> is open that setting never returns under the software GL this tool launches with (the screenshot times out), while
animations="allow" does. So the default --animations auto switches to "allow" whenever the --click opened a dialog
(data-g-open buttons: sheets and modals) and waits for the open transition itself. A dialog shot is slow under software
GL (minutes on a busy machine), so those shots get a longer timeout. Force a mode with --animations allow|disabled.
"""
import argparse
import pathlib
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://127.0.0.1:8152")
ap.add_argument("--pages", default="landing,dashboard,detail,gallery")
ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parent.parent / "docs" / "shots"))
ap.add_argument("--themes", default="light,dark")
ap.add_argument("--full", action="store_true")
ap.add_argument("--click", default="")
ap.add_argument("--suffix", default="")
ap.add_argument("--wait", type=int, default=1200)
ap.add_argument("--animations", choices=["auto", "allow", "disabled"], default="auto",
                help="auto = disabled, except allow when --click opened a <dialog> (disabled never returns with a dialog open)")
a = ap.parse_args()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader"])  # without these, DPR 2 headless mis-renders backdrop-filter in the lower half
    for page in a.pages.split(","):
        for theme in a.themes.split(","):
            for tag, vp, dpr in [("desk", {"width": 1440, "height": 900}, 1), ("phone", {"width": 390, "height": 844}, 2)]:
                ctx = b.new_context(viewport=vp, device_scale_factor=dpr, is_mobile=(tag == "phone"), has_touch=(tag == "phone"))
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.goto(f"{a.base}/templates/{page}.html?theme={theme}", wait_until="networkidle")
                pg.wait_for_timeout(a.wait)
                dialog_open = False
                if a.click:
                    pg.click(a.click); pg.wait_for_timeout(900)
                    dialog_open = pg.evaluate("!!document.querySelector('dialog[open]')")
                    if dialog_open:
                        pg.wait_for_timeout(700)   # animations are left on for the shot, so let the open transition finish first
                anim = a.animations if a.animations != "auto" else ("allow" if dialog_open else "disabled")
                f = out / f"{page}{a.suffix}_{tag}_{theme}.png"
                try:
                    pg.screenshot(path=str(f), full_page=a.full, timeout=240000 if dialog_open else 90000, animations=anim)
                except Exception as e:  # noqa: BLE001  (software GL can be slow; keep going)
                    print(f.name, "SCREENSHOT FAILED", str(e)[:80], flush=True); ctx.close(); continue
                sw = pg.evaluate("document.documentElement.scrollWidth")
                print(f.name, "hscroll!" if sw > vp["width"] else "", ("ERR " + "; ".join(errs)[:200]) if errs else "", flush=True)
                ctx.close()
    b.close()
