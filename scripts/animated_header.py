#!/usr/bin/env python3
"""
animated_header.py - generate dark/light terminal typing SVG animations for GitHub README.
Uses pure SVG + CSS @keyframes so it renders natively without external API dependencies.
"""

from pathlib import Path

DARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 140" width="850" height="140" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">
  <defs>
    <linearGradient id="grad-dark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="accent-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#39d353"/>
      <stop offset="50%" stop-color="#26a641"/>
      <stop offset="100%" stop-color="#00f2fe"/>
    </linearGradient>
  </defs>

  <style>
    .bg { fill: url(#grad-dark); stroke: #30363d; stroke-width: 1px; rx: 12px; }
    .header-bar { fill: #161b22; rx: 12px; }
    .prompt { fill: #39d353; font-weight: bold; font-size: 15px; }
    .user { fill: #58a6ff; font-weight: bold; font-size: 15px; }
    .text-title { fill: #e6edf3; font-weight: 600; font-size: 22px; }
    .subtext { font-weight: 500; font-size: 16px; }
    
    @keyframes cursor-blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    .cursor { fill: #39d353; animation: cursor-blink 0.8s infinite; }

    @keyframes text-cycle {
      0%, 22% { opacity: 1; content: "Software Developer"; }
      25%, 47% { opacity: 1; content: "Java & Python Enthusiast"; }
      50%, 72% { opacity: 1; content: "React & Flutter Builder"; }
      75%, 97% { opacity: 1; content: "DSA & Problem Solver"; }
      100% { opacity: 1; content: "Software Developer"; }
    }

    @keyframes typing1 {
      0% { width: 0; }
      20%, 80% { width: 280px; }
      100% { width: 0; }
    }
    
    .animated-text {
      fill: url(#accent-grad);
      font-size: 20px;
      font-weight: 700;
    }
    
    @keyframes pulse-glow {
      0%, 100% { filter: drop-shadow(0 0 2px rgba(57, 211, 83, 0.4)); }
      50% { filter: drop-shadow(0 0 8px rgba(57, 211, 83, 0.8)); }
    }
    .glow { animation: pulse-glow 3s infinite; }
  </style>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="140" class="bg glow"/>
  
  <!-- Window Controls Bar -->
  <path d="M 0,0 L 850,0 A 12,12 0 0,1 850,32 L 0,32 Z" fill="#161b22"/>
  <circle cx="20" cy="16" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="16" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="16" r="6" fill="#27c93f"/>
  <text x="425" y="21" text-anchor="middle" fill="#8b949e" font-size="12" font-weight="600">terminal — bash — 85x14</text>

  <!-- Terminal Content -->
  <g transform="translate(25, 62)">
    <text class="user" x="0" y="0">harsh@developer</text>
    <text class="prompt" x="145" y="0">:~$</text>
    <text class="text-title" x="180" y="0">Hi, I'm Harsh 👋</text>
  </g>

  <g transform="translate(25, 102)">
    <text class="prompt" x="0" y="0">></text>
    <text class="animated-text" x="20" y="0">
      <tspan>Building software • Solving problems with Java, Python, React &amp; Flutter</tspan>
    </text>
    <rect class="cursor" x="735" y="-16" width="9" height="20"/>
  </g>
</svg>
"""

LIGHT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 140" width="850" height="140" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">
  <defs>
    <linearGradient id="grad-light" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f6f8fa"/>
    </linearGradient>
    <linearGradient id="accent-grad-light" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1a7f37"/>
      <stop offset="50%" stop-color="#116329"/>
      <stop offset="100%" stop-color="#0969da"/>
    </linearGradient>
  </defs>

  <style>
    .bg { fill: url(#grad-light); stroke: #d0d7de; stroke-width: 1px; rx: 12px; }
    .prompt { fill: #1a7f37; font-weight: bold; font-size: 15px; }
    .user { fill: #0969da; font-weight: bold; font-size: 15px; }
    .text-title { fill: #1f2328; font-weight: 600; font-size: 22px; }
    
    @keyframes cursor-blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    .cursor { fill: #1a7f37; animation: cursor-blink 0.8s infinite; }
    .animated-text { fill: url(#accent-grad-light); font-size: 20px; font-weight: 700; }
  </style>

  <rect x="0" y="0" width="850" height="140" class="bg"/>
  <path d="M 0,0 L 850,0 A 12,12 0 0,1 850,32 L 0,32 Z" fill="#f3f4f6"/>
  <circle cx="20" cy="16" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="16" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="16" r="6" fill="#27c93f"/>
  <text x="425" y="21" text-anchor="middle" fill="#57606a" font-size="12" font-weight="600">terminal — bash — 85x14</text>

  <g transform="translate(25, 62)">
    <text class="user" x="0" y="0">harsh@developer</text>
    <text class="prompt" x="145" y="0">:~$</text>
    <text class="text-title" x="180" y="0">Hi, I'm Harsh 👋</text>
  </g>

  <g transform="translate(25, 102)">
    <text class="prompt" x="0" y="0">></text>
    <text class="animated-text" x="20" y="0">
      <tspan>Building software • Solving problems with Java, Python, React &amp; Flutter</tspan>
    </text>
    <rect class="cursor" x="735" y="-16" width="9" height="20"/>
  </g>
</svg>
"""

def main():
    out_dir = Path("assets")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "header-typing-dark.svg").write_text(DARK_SVG, encoding="utf-8")
    (out_dir / "header-typing-light.svg").write_text(LIGHT_SVG, encoding="utf-8")
    print("Generated header-typing-dark.svg and header-typing-light.svg")

if __name__ == "__main__":
    main()
