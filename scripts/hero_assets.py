#!/usr/bin/env python3
"""
hero_assets.py - generate dark developer-themed SVG assets for the README hero.

Reads assets/ghibli_me.png without modifying it and writes:
  - assets/portrait-card.svg   (rounded-corner portrait with neon-green / electric-blue frame)
  - assets/badge-github.svg    (dark GitHub link badge with neon-green accent)
  - assets/badge-linkedin.svg  (dark LinkedIn link badge with electric-blue accent)
"""

from __future__ import annotations

import base64
from pathlib import Path

GITHUB_ICON_PATH = (
    "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 "
    "0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13"
    "-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66"
    ".07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15"
    "-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27"
    ".68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12"
    ".51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 "
    "0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
)

LINKEDIN_ICON_PATH = (
    "M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708"
    "c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 "
    "12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248"
    "-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 "
    "1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 "
    "1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184"
    "-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169"
    "h-2.4c.03.678 0 7.225 0 7.225z"
)

FONT = 'ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'


def build_portrait_svg(png_path: Path) -> str:
    """Wrap the portrait PNG in a rounded dark card with a subtle neon border."""
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 260" width="260" height="260" role="img" aria-label="Harsh developer portrait">
  <defs>
    <linearGradient id="neon-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#39d353" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#30363d" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#58a6ff" stop-opacity="0.85"/>
    </linearGradient>
    <clipPath id="portrait-clip">
      <rect x="6" y="6" width="248" height="248" rx="16" ry="16"/>
    </clipPath>
  </defs>
  <rect x="1" y="1" width="258" height="258" rx="20" ry="20" fill="#0d1117" stroke="url(#neon-border)" stroke-width="2"/>
  <image href="data:image/png;base64,{b64}" x="6" y="6" width="248" height="248" preserveAspectRatio="xMidYMid slice" clip-path="url(#portrait-clip)"/>
  <rect x="6" y="6" width="248" height="248" rx="16" ry="16" fill="none" stroke="#30363d" stroke-opacity="0.7" stroke-width="1"/>
</svg>
"""


def build_badge_svg(label: str, icon_path: str, accent: str, width: int) -> str:
    """Render a compact dark-themed link badge with a subtle colored accent."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 32" width="{width}" height="32" role="img" aria-label="{label}" font-family='{FONT}'>
  <defs>
    <linearGradient id="badge-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
  </defs>
  <rect x="0.75" y="0.75" width="{width - 1.5}" height="30.5" rx="7" ry="7" fill="url(#badge-bg)" stroke="{accent}" stroke-opacity="0.55" stroke-width="1.2"/>
  <path d="{icon_path}" transform="translate(12, 8)" fill="{accent}"/>
  <text x="36" y="20.5" font-size="12.5" font-weight="600" fill="#e6edf3" letter-spacing="0.2">{label}</text>
</svg>
"""


def main() -> None:
    assets = Path("assets")
    portrait_src = assets / "ghibli_me.png"
    if not portrait_src.exists():
        raise SystemExit(f"Missing portrait image: {portrait_src}")

    (assets / "portrait-card.svg").write_text(build_portrait_svg(portrait_src), encoding="utf-8")
    (assets / "badge-github.svg").write_text(
        build_badge_svg("GitHub", GITHUB_ICON_PATH, "#39d353", 98), encoding="utf-8"
    )
    (assets / "badge-linkedin.svg").write_text(
        build_badge_svg("LinkedIn", LINKEDIN_ICON_PATH, "#58a6ff", 106), encoding="utf-8"
    )
    print("Generated portrait-card.svg, badge-github.svg, and badge-linkedin.svg")


if __name__ == "__main__":
    main()

