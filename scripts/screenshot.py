#!/usr/bin/env python3
"""Make static PNG images of the interactive views, for the essay.

Opens each HTML view in headless Google Chrome and saves a screenshot next to
it. The views load map tiles and Cytoscape.js from the internet, so this needs
a network connection, and it runs outside Claude Code's command sandbox
(Chrome is outside the project folder).

  analysis/maps/routes_print.html -> analysis/maps/routes.png   (OpenStreetMap base; map_routes.py --print)
  analysis/surplus/surplus.html  -> analysis/surplus/surplus.png

Usage (from the project folder):
  python3 scripts/screenshot.py
  python3 scripts/screenshot.py --wait 40000     # give slow map tiles longer

Standard library only; needs google-chrome on the PATH.
"""

import argparse
import shutil
import subprocess

from corpus import ANALYSIS, ROOT

VIEWS = [
    ("maps/routes_print.html", "maps/routes.png", (1500, 1150)),
    ("surplus/surplus.html", "surplus/surplus.png", (1400, 2050)),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--wait", type=int, default=30000, help="virtual time budget in ms for the page to load")
    args = ap.parse_args()
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("google-chrome not found on the PATH")
    for src, out, (w, h) in VIEWS:
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
               f"--window-size={w},{h}", f"--virtual-time-budget={args.wait}",
               f"--screenshot={ANALYSIS / out}", (ANALYSIS / src).as_uri()]
        subprocess.run(cmd, check=True, capture_output=True, timeout=180)
        print(f"{(ANALYSIS / out).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
