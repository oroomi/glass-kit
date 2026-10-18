#!/usr/bin/env python3
"""Self-host Geist + Geist Mono for offline expo wifi (fonts are SIL OFL, fetched from Google Fonts).

Usage: python3 tools/vendor_fonts.py <app-static-dir>
Writes <dir>/fonts/*.woff2 and <dir>/fonts/geist.css. Then in your copy of glass.css replace the
Google Fonts @import line with:  @import url("fonts/geist.css");   (path relative to glass.css)
"""
import pathlib
import re
import sys
import urllib.request

CSS_URL = "https://fonts.googleapis.com/css2?family=Geist:wght@400..700&family=Geist+Mono:wght@400..600&display=swap"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    out = pathlib.Path(sys.argv[1]) / "fonts"
    out.mkdir(parents=True, exist_ok=True)
    css = get(CSS_URL).decode()
    urls = sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", css)))
    for i, u in enumerate(urls):
        name = f"geist-{i}.woff2"
        (out / name).write_bytes(get(u))
        css = css.replace(u, name)
    (out / "geist.css").write_text("/* Geist + Geist Mono, SIL Open Font License 1.1, vendored from Google Fonts */\n" + css)
    print(f"wrote {len(urls)} font files and {out / 'geist.css'}")


if __name__ == "__main__":
    main()
