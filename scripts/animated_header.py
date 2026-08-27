#!/usr/bin/env python3
"""
animated_header.py - generate dark/light terminal typing header SVG animations for GitHub README.
Uses step-start animation on staggered <tspan> elements so letters pop into existence instantly (authentic terminal typing).
"""

from pathlib import Path

def generate_typing_text(text: str, fill_color: str, char_w: float = 9.6) -> tuple[str, str]:
    """
    Generates <tspan> elements with step-start animation delays
    so letters appear instantly as the cursor steps across them.
    """
    tspans = []
    css_rules = []

    total_chars = len(text)
    duration = 7.0  # seconds total loop
    type_duration = 2.2  # seconds to type out all characters

    css_rules.append("""
    @keyframes char-appear {
      0% { opacity: 0; }
      10%, 85% { opacity: 1; }
      95%, 100% { opacity: 0; }
    }
    """)

    for i, char in enumerate(text):
        escaped_char = char.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        # Delay starts after 0.2s pause and finishes at 0.2s + type_duration
        delay = round(0.2 + (i / total_chars) * type_duration, 2)
        tspans.append(f'<tspan class="tc-{i}">{escaped_char}</tspan>')
        # step-start ensures zero fade - letter appears 100% instantly
        css_rules.append(f'.tc-{i} {{ opacity: 0; animation: char-appear {duration}s step-start infinite; animation-delay: {delay}s; }}')

    cursor_max_x = round(total_chars * char_w, 1)
    cursor_css = f"""
    @keyframes cursor-type {{
      0%, 3% {{ transform: translateX(0px); }}
      35%, 85% {{ transform: translateX({cursor_max_x}px); }}
      95%, 100% {{ transform: translateX(0px); }}
    }}
    .cursor-wrap {{
      animation: cursor-type {duration}s steps({total_chars}, end) infinite;
    }}
    """

    full_css = "\n".join(css_rules) + "\n" + cursor_css
    full_tspans = "".join(tspans)
    return full_tspans, full_css

def build_svg(theme: str) -> str:
    is_dark = theme == "dark"
    bg_grad_id = "grad-dark" if is_dark else "grad-light"
    bg_start = "#0d1117" if is_dark else "#ffffff"
    bg_end = "#161b22" if is_dark else "#f6f8fa"
    border_col = "#30363d" if is_dark else "#d0d7de"
    hdr_fill = "#161b22" if is_dark else "#f3f4f6"
    hdr_text_col = "#8b949e" if is_dark else "#57606a"
    user_col = "#58a6ff" if is_dark else "#0969da"
    prompt_col = "#39d353" if is_dark else "#1a7f37"
    title_col = "#e6edf3" if is_dark else "#1f2328"
    text_fill = "#39d353" if is_dark else "#1a7f37"

    text_to_type = "Building software • Java, Python, React & Flutter"
    tspans_html, typing_css = generate_typing_text(text_to_type, text_fill, char_w=9.6)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 140" width="850" height="140" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">
  <defs>
    <linearGradient id="{bg_grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_start}"/>
      <stop offset="100%" stop-color="{bg_end}"/>
    </linearGradient>
  </defs>

  <style>
    .prompt {{ fill: {prompt_col}; font-weight: bold; font-size: 15px; }}
    .user {{ fill: {user_col}; font-weight: bold; font-size: 15px; }}
    .text-title {{ fill: {title_col}; font-weight: 600; font-size: 22px; }}
    .type-text {{ fill: {text_fill}; font-size: 16px; font-weight: 700; }}

    @keyframes cursor-blink {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
    .cursor {{ fill: {prompt_col}; animation: cursor-blink 0.8s infinite; }}

{typing_css}
  </style>

  <!-- Background Card -->
  <rect x="0" y="0" width="850" height="140" rx="12" ry="12" fill="url(#{bg_grad_id})" stroke="{border_col}" stroke-width="1"/>

  <!-- Window Header Bar -->
  <path d="M 0,0 L 850,0 A 12,12 0 0,1 850,32 L 0,32 L 0,0 Z" fill="{hdr_fill}"/>
  <circle cx="20" cy="16" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="16" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="16" r="6" fill="#27c93f"/>
  <text x="425" y="21" text-anchor="middle" fill="{hdr_text_col}" font-size="12" font-weight="600">terminal — bash — 85x14</text>

  <!-- Terminal Line 1 -->
  <g transform="translate(25, 62)">
    <text class="user" x="0" y="0">harsh@developer</text>
    <text class="prompt" x="145" y="0">:~$</text>
    <text class="text-title" x="180" y="0">Hi, I'm Harsh 👋</text>
  </g>

  <!-- Terminal Line 2: Authentic Terminal Typing -->
  <g transform="translate(25, 102)">
    <text class="prompt" x="0" y="0">></text>
    <text class="type-text" x="20" y="0">{tspans_html}</text>
    <g class="cursor-wrap" transform="translate(20, 0)">
      <rect class="cursor" x="0" y="-16" width="9" height="20"/>
    </g>
  </g>
</svg>
"""
    return svg

def main():
    out_dir = Path("assets")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "card-header-dark.svg").write_text(build_svg("dark"), encoding="utf-8")
    (out_dir / "card-header-light.svg").write_text(build_svg("light"), encoding="utf-8")
    print("Generated card-header-dark.svg and card-header-light.svg with step-start terminal typing")

if __name__ == "__main__":
    main()
