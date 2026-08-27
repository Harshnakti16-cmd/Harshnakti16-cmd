#!/usr/bin/env python3
"""
marquee.py - generate animated horizontal scrolling tech stack SVG.
"""

from pathlib import Path

DARK_MARQUEE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 65" width="850" height="65" font-family="ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="badge-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#21262d"/>
    </linearGradient>
  </defs>

  <style>
    .bg { fill: #0d1117; rx: 10px; stroke: #30363d; stroke-width: 1px; }
    .badge { fill: url(#badge-grad); stroke: #30363d; stroke-width: 1px; rx: 16px; }
    .text { font-size: 13px; font-weight: 600; fill: #e6edf3; }
    .dot { font-size: 16px; }

    @keyframes scroll-left {
      0% { transform: translateX(0px); }
      100% { transform: translateX(-450px); }
    }

    .track {
      animation: scroll-left 15s linear infinite;
    }
    .track:hover {
      animation-play-state: paused;
    }
  </style>

  <rect x="0" y="0" width="850" height="65" class="bg"/>

  <g transform="translate(10, 16)">
    <g class="track">
      <!-- Set 1 -->
      <g transform="translate(0,0)"><rect width="90" height="32" class="badge"/><text x="45" y="20" text-anchor="middle" class="text">☕ Java</text></g>
      <g transform="translate(105,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">🐍 Python</text></g>
      <g transform="translate(220,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">⚛️ React</text></g>
      <g transform="translate(330,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">💙 Flutter</text></g>
      <g transform="translate(440,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">⚡ FastAPI</text></g>
      <g transform="translate(555,0)"><rect width="80" height="32" class="badge"/><text x="40" y="20" text-anchor="middle" class="text">🐙 Git</text></g>
      <g transform="translate(650,0)"><rect width="110" height="32" class="badge"/><text x="55" y="20" text-anchor="middle" class="text">🧩 Data Structures</text></g>
      <g transform="translate(775,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">💡 Algorithms</text></g>

      <!-- Set 2 (for smooth infinite looping) -->
      <g transform="translate(890,0)"><rect width="90" height="32" class="badge"/><text x="45" y="20" text-anchor="middle" class="text">☕ Java</text></g>
      <g transform="translate(995,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">🐍 Python</text></g>
      <g transform="translate(1110,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">⚛️ React</text></g>
      <g transform="translate(1220,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">💙 Flutter</text></g>
      <g transform="translate(1330,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">⚡ FastAPI</text></g>
    </g>
  </g>
</svg>
"""

LIGHT_MARQUEE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 65" width="850" height="65" font-family="ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="badge-grad-light" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f6f8fa"/>
    </linearGradient>
  </defs>

  <style>
    .bg { fill: #ffffff; rx: 10px; stroke: #d0d7de; stroke-width: 1px; }
    .badge { fill: url(#badge-grad-light); stroke: #d0d7de; stroke-width: 1px; rx: 16px; }
    .text { font-size: 13px; font-weight: 600; fill: #1f2328; }

    @keyframes scroll-left {
      0% { transform: translateX(0px); }
      100% { transform: translateX(-450px); }
    }

    .track {
      animation: scroll-left 15s linear infinite;
    }
    .track:hover {
      animation-play-state: paused;
    }
  </style>

  <rect x="0" y="0" width="850" height="65" class="bg"/>

  <g transform="translate(10, 16)">
    <g class="track">
      <g transform="translate(0,0)"><rect width="90" height="32" class="badge"/><text x="45" y="20" text-anchor="middle" class="text">☕ Java</text></g>
      <g transform="translate(105,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">🐍 Python</text></g>
      <g transform="translate(220,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">⚛️ React</text></g>
      <g transform="translate(330,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">💙 Flutter</text></g>
      <g transform="translate(440,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">⚡ FastAPI</text></g>
      <g transform="translate(555,0)"><rect width="80" height="32" class="badge"/><text x="40" y="20" text-anchor="middle" class="text">🐙 Git</text></g>
      <g transform="translate(650,0)"><rect width="110" height="32" class="badge"/><text x="55" y="20" text-anchor="middle" class="text">🧩 Data Structures</text></g>
      <g transform="translate(775,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">💡 Algorithms</text></g>

      <g transform="translate(890,0)"><rect width="90" height="32" class="badge"/><text x="45" y="20" text-anchor="middle" class="text">☕ Java</text></g>
      <g transform="translate(995,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">🐍 Python</text></g>
      <g transform="translate(1110,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">⚛️ React</text></g>
      <g transform="translate(1220,0)"><rect width="95" height="32" class="badge"/><text x="47" y="20" text-anchor="middle" class="text">💙 Flutter</text></g>
      <g transform="translate(1330,0)"><rect width="100" height="32" class="badge"/><text x="50" y="20" text-anchor="middle" class="text">⚡ FastAPI</text></g>
    </g>
  </g>
</svg>
"""

def main():
    out_dir = Path("assets")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "marquee-tech-dark.svg").write_text(DARK_MARQUEE, encoding="utf-8")
    (out_dir / "marquee-tech-light.svg").write_text(LIGHT_MARQUEE, encoding="utf-8")
    print("Generated marquee-tech-dark.svg and marquee-tech-light.svg")

if __name__ == "__main__":
    main()
