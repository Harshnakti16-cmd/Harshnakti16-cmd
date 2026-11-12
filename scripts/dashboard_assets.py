#!/usr/bin/env python3
"""
dashboard_assets.py - generate minimal dark developer dashboard SVG assets.

Palette:
  bg=#0D1117, card=#161B22, border=#30363D,
  green=#3FB950, blue=#58A6FF, purple=#BC8CFF,
  text=#F0F6FC, muted=#8B949E
"""

from __future__ import annotations

import html
from pathlib import Path

FONT = 'ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'
MONO = 'ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace'

BG = "#0D1117"
CARD = "#161B22"
BORDER = "#30363D"
GREEN = "#3FB950"
BLUE = "#58A6FF"
PURPLE = "#BC8CFF"
TEXT = "#F0F6FC"
MUTED = "#8B949E"

# 16x16 native vector icons for technology stack pills
TECH_ICONS: dict[str, str] = {
    "Python": (
        '<path d="M7.9 1C5 1 5.2 2.3 5.2 2.3v1.4h2.8v.4H4.1S2 3.9 2 6.8s1.8 2.8 1.8 2.8h1.1V8.3'
        's0-1.8 1.8-1.8h3s1.6 0 1.6-1.6V2.6S11.5 1 7.9 1zm-1.6.9a.55.55 0 110 1.1.55.55 0 010-1.1z" fill="#3776AB"/>'
        '<path d="M8.1 15c2.9 0 2.7-1.3 2.7-1.3v-1.4H8v-.4h3.9s2.1.2 2.1-2.7-1.8-2.8-1.8-2.8h-1.1v1.3'
        's0 1.8-1.8 1.8h-3s-1.6 0-1.6 1.6v2.3S4.5 15 8.1 15zm1.6-.9a.55.55 0 110-1.1.55.55 0 010 1.1z" fill="#FFD43B"/>'
    ),
    "FastAPI": (
        '<circle cx="8" cy="8" r="7" fill="#009688"/>'
        '<path d="M8.9 3.2L4.8 9h3.1l-.8 3.8L11.2 7H8.1z" fill="#F0F6FC"/>'
    ),
    "Flask": (
        '<path d="M6 2h4M6.8 2v3.6L3.6 12.2A1.4 1.4 0 004.9 14h6.2a1.4 1.4 0 001.3-1.8L9.2 5.6V2" '
        'fill="none" stroke="#F0F6FC" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M4.8 10.6h6.4l1.1 2a.7.7 0 01-.6 1H4.3a.7.7 0 01-.6-1z" fill="#3FB950" opacity="0.85"/>'
    ),
    "SQLAlchemy": (
        '<rect x="2" y="2.5" width="12" height="3.2" rx="1.2" fill="none" stroke="#D74A3E" stroke-width="1.3"/>'
        '<path d="M3.5 5.7v4.6c0 1.2 2 2.2 4.5 2.2s4.5-1 4.5-2.2V5.7" fill="none" stroke="#D74A3E" stroke-width="1.3"/>'
        '<circle cx="11.5" cy="11.8" r="2.2" fill="#0D1117" stroke="#F0F6FC" stroke-width="1.1"/>'
    ),
    "React": (
        '<circle cx="8" cy="8" r="1.4" fill="#61DAFB"/>'
        '<ellipse cx="8" cy="8" rx="6.6" ry="2.5" fill="none" stroke="#61DAFB" stroke-width="1.1"/>'
        '<ellipse cx="8" cy="8" rx="6.6" ry="2.5" transform="rotate(60 8 8)" fill="none" stroke="#61DAFB" stroke-width="1.1"/>'
        '<ellipse cx="8" cy="8" rx="6.6" ry="2.5" transform="rotate(120 8 8)" fill="none" stroke="#61DAFB" stroke-width="1.1"/>'
    ),
    "JavaScript": (
        '<rect x="1.5" y="1.5" width="13" height="13" rx="2.4" fill="#F7DF1E"/>'
        '<text x="12.6" y="12.3" text-anchor="end" font-size="7.2" font-weight="800" fill="#0D1117">JS</text>'
    ),
    "HTML": (
        '<rect x="1.5" y="1.5" width="13" height="13" rx="2.4" fill="#E34F26"/>'
        '<path d="M6 5.3L3.7 8 6 10.7M10 5.3L12.3 8 10 10.7" fill="none" stroke="#FFFFFF" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    "CSS": (
        '<rect x="1.5" y="1.5" width="13" height="13" rx="2.4" fill="#1572B6"/>'
        '<text x="8" y="10.7" text-anchor="middle" font-size="8.2" font-weight="800" fill="#FFFFFF">{ }</text>'
    ),
    "Flutter": (
        '<polygon points="9.2,1.5 2.5,8.2 4.6,10.3 13.4,1.5" fill="#54C5F8"/>'
        '<polygon points="9.2,7.6 5.6,11.2 9.2,14.8 13.4,14.8 9.8,11.2 13.4,7.6" fill="#01579B"/>'
        '<polygon points="5.6,11.2 7.7,9.1 9.8,11.2 7.7,13.3" fill="#29B6F6"/>'
    ),
    "Dart": (
        '<polygon points="3.8,3.8 11.4,1.8 14.2,6.2 14.2,12.4 9.5,14.2 3.8,10.5" fill="#0175C2"/>'
        '<polygon points="3.8,3.8 11.4,1.8 8.6,8.2 1.8,6.8" fill="#00D2B8"/>'
        '<polygon points="8.6,8.2 14.2,12.4 9.5,14.2 3.8,10.5" fill="#29B6F6"/>'
    ),
    "PostgreSQL": (
        '<path d="M4.2 4.8C4.2 2.8 6 1.8 8 1.8s3.8 1 3.8 3c0 2.6-.7 4.4-1.5 5.4v2.6c0 .8-.7 1.3-1.4 1.3-.7 0-1.2-.5-1.2-1.2V10.6'
        'c-.6-.4-1.2-.4-1.8 0-.9 0-1.7-2.2-1.7-5.8z" fill="#4169E1"/>'
        '<circle cx="6.7" cy="5.2" r=".7" fill="#F0F6FC"/>'
        '<circle cx="9.3" cy="5.2" r=".7" fill="#F0F6FC"/>'
        '<path d="M8 8.3c-.6 1.2-.2 2.8.8 3.6" fill="none" stroke="#F0F6FC" stroke-width="1.1" stroke-linecap="round"/>'
    ),
    "MySQL": (
        '<ellipse cx="8" cy="4.2" rx="5.2" ry="2" fill="none" stroke="#00A8C6" stroke-width="1.3"/>'
        '<path d="M2.8 4.2v3.6c0 1.1 2.3 2 5.2 2s5.2-.9 5.2-2V4.2" fill="none" stroke="#00A8C6" stroke-width="1.3"/>'
        '<path d="M2.8 7.8v3.6c0 1.1 2.3 2 5.2 2s5.2-.9 5.2-2V7.8" fill="none" stroke="#F29111" stroke-width="1.3"/>'
    ),
    "Firebase": (
        '<polygon points="3.5,12.2 5.1,2.2 8.2,7.8" fill="#FFA000"/>'
        '<polygon points="3.5,12.2 9.4,5.4 11.4,12.2 8,14.2" fill="#FFCA28"/>'
        '<polygon points="3.5,12.2 12.5,3.8 12.5,12.2 8,14.2" fill="#F57C00" opacity="0.85"/>'
    ),
    "SQLite": (
        '<ellipse cx="7" cy="4.2" rx="4.5" ry="1.8" fill="none" stroke="#58A6FF" stroke-width="1.3"/>'
        '<path d="M2.5 4.2v7.2c0 1 2 1.8 4.5 1.8s4.5-.8 4.5-1.8V4.2" fill="none" stroke="#58A6FF" stroke-width="1.3"/>'
        '<path d="M8.5 12.8L14 3.5c-1.8.4-3.3 1.7-4 3.6z" fill="#79C0FF"/>'
    ),
    "Twilio": (
        '<circle cx="8" cy="8" r="6.3" fill="none" stroke="#F22F46" stroke-width="1.6"/>'
        '<circle cx="6" cy="6" r="1.25" fill="#F22F46"/>'
        '<circle cx="10" cy="6" r="1.25" fill="#F22F46"/>'
        '<circle cx="6" cy="10" r="1.25" fill="#F22F46"/>'
        '<circle cx="10" cy="10" r="1.25" fill="#F22F46"/>'
    ),
    "ElevenLabs": (
        '<rect x="4.5" y="2.5" width="2.5" height="11" rx="0.8" fill="#F0F6FC"/>'
        '<rect x="9" y="2.5" width="2.5" height="11" rx="0.8" fill="#F0F6FC"/>'
    ),
    "Deepgram": (
        '<rect x="2.2" y="6" width="2" height="4" rx="1" fill="#13EF93"/>'
        '<rect x="5.4" y="3" width="2" height="10" rx="1" fill="#13EF93"/>'
        '<rect x="8.6" y="4.5" width="2" height="7" rx="1" fill="#58A6FF"/>'
        '<rect x="11.8" y="2" width="2" height="12" rx="1" fill="#13EF93"/>'
    ),
    "OpenAI": (
        '<circle cx="8" cy="8" r="5.8" fill="none" stroke="#10A37F" stroke-width="1.4" stroke-dasharray="3.2 1.8"/>'
        '<polygon points="8,3.5 11.9,5.75 11.9,10.25 8,12.5 4.1,10.25 4.1,5.75" fill="none" stroke="#10A37F" stroke-width="1.25"/>'
        '<circle cx="8" cy="8" r="1.3" fill="#10A37F"/>'
    ),
    "Git": (
        '<rect x="3.1" y="3.1" width="9.8" height="9.8" rx="1.8" transform="rotate(45 8 8)" fill="#F05032"/>'
        '<path d="M6.4 4.8L8.4 6.8v4.1M8.4 6.8l2 2" fill="none" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round"/>'
        '<circle cx="8.4" cy="6.8" r="1.1" fill="#FFFFFF"/>'
        '<circle cx="8.4" cy="10.9" r="1.1" fill="#FFFFFF"/>'
        '<circle cx="10.4" cy="8.8" r="1.1" fill="#FFFFFF"/>'
    ),
    "GitHub": (
        '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
        '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13'
        '-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66'
        '.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15'
        '-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27'
        '.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12'
        '.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 '
        '0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" fill="#F0F6FC"/>'
    ),
    "Postman": (
        '<circle cx="8" cy="8" r="6.8" fill="#FF6C37"/>'
        '<path d="M5 10.6L11 5.2m0 0L8.8 11.2 7.3 8.6 4.7 7.1z" fill="none" stroke="#FFFFFF" stroke-width="1.25" stroke-linejoin="round" stroke-linecap="round"/>'
    ),
}


def build_stack_card(
    title: str,
    items: list[str],
    accent: str,
    animate_highlight: bool = False,
) -> str:
    """Build a 420x132 minimal dark category card for the technology stack grid."""
    w, h = 420, 132
    pills = []
    n = len(items)

    if n == 2:
        positions = [(18, 66, 184), (218, 66, 184)]
    elif n == 3:
        positions = [(18, 66, 120), (150, 66, 120), (282, 66, 120)]
    else:
        positions = [
            (18, 53, 184),
            (218, 53, 184),
            (18, 89, 184),
            (218, 89, 184),
        ]

    for idx, name in enumerate(items):
        px, py, pw = positions[idx]
        icon_svg = TECH_ICONS[name]
        pills.append(
            f'<g transform="translate({px},{py})">'
            f'<rect width="{pw}" height="28" rx="7" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
            f'<g transform="translate(10,6)">{icon_svg}</g>'
            f'<text x="33" y="18.2" font-size="12" font-weight="600" fill="{TEXT}">{html.escape(name)}</text>'
            f"</g>"
        )

    defs = ""
    style = ""
    highlight = ""
    if animate_highlight:
        defs = (
            "<defs>"
            '<clipPath id="card-clip"><rect x="0.75" y="0.75" width="418.5" height="130.5" rx="12"/></clipPath>'
            '<linearGradient id="sweep-grad" x1="0%" y1="0%" x2="100%" y2="0%">'
            '<stop offset="0%" stop-color="#3FB950" stop-opacity="0"/>'
            '<stop offset="50%" stop-color="#3FB950" stop-opacity="0.14"/>'
            '<stop offset="75%" stop-color="#58A6FF" stop-opacity="0.10"/>'
            '<stop offset="100%" stop-color="#58A6FF" stop-opacity="0"/>'
            "</linearGradient>"
            "</defs>"
        )
        style = (
            "<style>"
            "@keyframes sweep { 0% { transform: translateX(-180px); } 50%, 100% { transform: translateX(520px); } }"
            ".sweep-bar { animation: sweep 9s ease-in-out infinite; }"
            "</style>"
        )
        highlight = (
            '<g clip-path="url(#card-clip)">'
            '<rect class="sweep-bar" x="0" y="0" width="140" height="132" fill="url(#sweep-grad)"/>'
            "</g>"
        )

    count_label = f"{n} tools" if title == "Tools" else f"{n} technologies"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{html.escape(title)} technology stack" font-family=\'{FONT}\'>'
        f"{defs}{style}"
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="12" fill="{CARD}" stroke="{BORDER}" stroke-width="1.2"/>'
        f"{highlight}"
        f'<rect x="18" y="0.75" width="56" height="2.2" rx="1.1" fill="{accent}"/>'
        f'<circle cx="23" cy="24" r="3.5" fill="{accent}"/>'
        f'<text x="34" y="28" font-size="13.5" font-weight="700" fill="{TEXT}" letter-spacing="0.3">{html.escape(title)}</text>'
        f'<text x="402" y="27.5" text-anchor="end" font-size="10.5" fill="{MUTED}">{count_label}</text>'
        f'<line x1="18" y1="41" x2="402" y2="41" stroke="{BORDER}" stroke-opacity="0.7" stroke-width="1"/>'
        f'{"".join(pills)}'
        f"</svg>\n"
    )


FOCUS_ICONS: dict[str, str] = {
    "app-dev": (
        '<rect x="2" y="3" width="16" height="14" rx="2.5" fill="none" stroke="#58A6FF" stroke-width="1.5"/>'
        '<line x1="2" y1="7.5" x2="18" y2="7.5" stroke="#58A6FF" stroke-width="1.3"/>'
        '<line x1="7.5" y1="7.5" x2="7.5" y2="17" stroke="#58A6FF" stroke-width="1.3"/>'
    ),
    "api": (
        '<path d="M6.5 4.5C5 4.5 4.5 5.2 4.5 6.3v2c0 .8-.5 1.3-1.2 1.7.7.4 1.2.9 1.2 1.7v2c0 1.1.5 1.8 2 1.8" '
        'fill="none" stroke="#3FB950" stroke-width="1.5" stroke-linecap="round"/>'
        '<path d="M13.5 4.5c1.5 0 2 .7 2 1.8v2c0 .8.5 1.3 1.2 1.7-.7.4-1.2.9-1.2 1.7v2c0 1.1-.5 1.8-2 1.8" '
        'fill="none" stroke="#3FB950" stroke-width="1.5" stroke-linecap="round"/>'
        '<circle cx="10" cy="10" r="1.6" fill="#58A6FF"/>'
    ),
    "database": (
        '<ellipse cx="10" cy="5.2" rx="6" ry="2.2" fill="none" stroke="#BC8CFF" stroke-width="1.5"/>'
        '<path d="M4 5.2v4.6c0 1.2 2.7 2.2 6 2.2s6-1 6-2.2V5.2" fill="none" stroke="#BC8CFF" stroke-width="1.5"/>'
        '<path d="M4 9.8v4.6c0 1.2 2.7 2.2 6 2.2s6-1 6-2.2V9.8" fill="none" stroke="#BC8CFF" stroke-width="1.5"/>'
    ),
    "problem-solving": (
        '<circle cx="5" cy="5.5" r="2" fill="none" stroke="#3FB950" stroke-width="1.5"/>'
        '<circle cx="15" cy="5.5" r="2" fill="none" stroke="#58A6FF" stroke-width="1.5"/>'
        '<circle cx="10" cy="14.5" r="2" fill="none" stroke="#3FB950" stroke-width="1.5"/>'
        '<path d="M6.6 6.8L8.8 12.8M13.4 6.8l-2.2 6" fill="none" stroke="#8B949E" stroke-width="1.3" stroke-linecap="round"/>'
    ),
}


def build_focus_card(
    key: str,
    title: str,
    line1: str,
    line2: str,
    accent: str,
    glow_border: bool = False,
) -> str:
    """Build a 420x118 minimal Engineering Focus card."""
    w, h = 420, 118
    style = ""
    glow_rect = ""
    if glow_border:
        style = (
            "<style>"
            "@keyframes border-glow { 0%, 100% { stroke-opacity: 0.25; } 50% { stroke-opacity: 0.72; } }"
            ".glow-stroke { animation: border-glow 7s ease-in-out infinite; }"
            "</style>"
        )
        glow_rect = (
            f'<rect class="glow-stroke" x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" '
            f'rx="12" fill="none" stroke="{accent}" stroke-width="1.4"/>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{html.escape(title)}" font-family=\'{FONT}\'>'
        f"{style}"
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="12" fill="{CARD}" stroke="{BORDER}" stroke-width="1.2"/>'
        f"{glow_rect}"
        f'<rect x="1" y="20" width="3" height="78" rx="1.5" fill="{accent}"/>'
        f'<rect x="20" y="22" width="34" height="34" rx="9" fill="{BG}" stroke="{accent}" stroke-opacity="0.45" stroke-width="1.1"/>'
        f'<g transform="translate(27,29)">{FOCUS_ICONS[key]}</g>'
        f'<text x="68" y="37" font-size="14.5" font-weight="700" fill="{TEXT}">{html.escape(title)}</text>'
        f'<text x="68" y="64" font-size="12" fill="{MUTED}">{html.escape(line1)}</text>'
        f'<text x="68" y="83" font-size="12" fill="{MUTED}">{html.escape(line2)}</text>'
        f"</svg>\n"
    )


def build_exploring_status() -> str:
    """Build an 850x54 status strip with one gentle pulse dot and slow cycling text."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 54" width="850" height="54" role="img" aria-label="Currently exploring status" font-family='{FONT}'>
  <style>
    @keyframes status-pulse {{
      0%, 100% {{ opacity: 0.45; transform: scale(1); }}
      50% {{ opacity: 0.08; transform: scale(1.5); }}
    }}
    .pulse-ring {{
      transform-origin: 26px 27px;
      animation: status-pulse 4s ease-in-out infinite;
    }}
    @keyframes phrase-cycle {{
      0% {{ opacity: 0; }}
      5%, 28% {{ opacity: 1; }}
      33.3%, 100% {{ opacity: 0; }}
    }}
    .p1 {{ opacity: 0; animation: phrase-cycle 15s ease-in-out infinite; animation-delay: 0s; }}
    .p2 {{ opacity: 0; animation: phrase-cycle 15s ease-in-out infinite; animation-delay: 5s; }}
    .p3 {{ opacity: 0; animation: phrase-cycle 15s ease-in-out infinite; animation-delay: 10s; }}
  </style>
  <rect x="0.75" y="0.75" width="848.5" height="52.5" rx="12" fill="{CARD}" stroke="{BORDER}" stroke-width="1.2"/>
  <circle class="pulse-ring" cx="26" cy="27" r="6" fill="{GREEN}"/>
  <circle cx="26" cy="27" r="4" fill="{GREEN}"/>
  <text x="42" y="31" font-size="11.5" font-weight="700" fill="{GREEN}" letter-spacing="0.8">ACTIVE FOCUS</text>
  <line x1="154" y1="15" x2="154" y2="39" stroke="{BORDER}" stroke-width="1"/>
  <text x="172" y="31.5" font-family='{MONO}' font-size="13.5" font-weight="700" fill="{BLUE}">&gt;</text>
  <text class="p1" x="190" y="31.5" font-family='{MONO}' font-size="13.5" font-weight="600" fill="{TEXT}">Building backend systems.</text>
  <text class="p2" x="190" y="31.5" font-family='{MONO}' font-size="13.5" font-weight="600" fill="{TEXT}">Exploring system design.</text>
  <text class="p3" x="190" y="31.5" font-family='{MONO}' font-size="13.5" font-weight="600" fill="{TEXT}">Practicing problem solving.</text>
</svg>
"""


def build_exploring_topics() -> str:
    """Build an 850x180 clean 2+2+1 grid of the 5 currently exploring topics."""
    topics = [
        (0, 0, 418, "Data Structures and Algorithms", GREEN),
        (432, 0, 418, "Advanced Python Backend Development", BLUE),
        (0, 62, 418, "System Design", PURPLE),
        (432, 62, 418, "Database Optimization", GREEN),
        (0, 124, 850, "Scalable Application Architecture", BLUE),
    ]
    cards = []
    for x, y, w, label, accent in topics:
        cards.append(
            f'<g transform="translate({x},{y})">'
            f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="50.5" rx="10" fill="{CARD}" stroke="{BORDER}" stroke-width="1.1"/>'
            f'<rect x="1" y="13" width="3" height="26" rx="1.5" fill="{accent}"/>'
            f'<circle cx="22" cy="26" r="3.5" fill="{accent}"/>'
            f'<text x="36" y="30.5" font-size="13.5" font-weight="600" fill="{TEXT}">{html.escape(label)}</text>'
            f"</g>"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 176" width="850" height="176" '
        f'role="img" aria-label="Currently exploring topics" font-family=\'{FONT}\'>'
        f'{"".join(cards)}'
        f"</svg>\n"
    )


def build_email_badge() -> str:
    """Build a 92x32 dark email badge matching the existing GitHub and LinkedIn badges."""
    w = 92
    envelope = (
        '<rect x="1" y="3" width="14" height="10" rx="1.8" fill="none" stroke="#BC8CFF" stroke-width="1.5"/>'
        '<path d="M1.8 4.2L8 9l6.2-4.8" fill="none" stroke="#BC8CFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 32" width="{w}" height="32" role="img" aria-label="Email" font-family='{FONT}'>
  <defs>
    <linearGradient id="badge-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161B22"/>
      <stop offset="100%" stop-color="#0D1117"/>
    </linearGradient>
  </defs>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="30.5" rx="7" ry="7" fill="url(#badge-bg)" stroke="{PURPLE}" stroke-opacity="0.55" stroke-width="1.2"/>
  <g transform="translate(12, 8)">{envelope}</g>
  <text x="36" y="20.5" font-size="12.5" font-weight="600" fill="{TEXT}" letter-spacing="0.2">Email</text>
</svg>
"""


def main() -> None:
    assets = Path("assets")
    assets.mkdir(exist_ok=True)

    stack_specs = [
        ("stack-backend.svg", "Backend", ["Python", "FastAPI", "Flask", "SQLAlchemy"], GREEN, True),
        ("stack-frontend.svg", "Frontend", ["React", "JavaScript", "HTML", "CSS"], BLUE, False),
        ("stack-mobile.svg", "Mobile", ["Flutter", "Dart"], PURPLE, False),
        ("stack-database.svg", "Database", ["PostgreSQL", "MySQL", "Firebase", "SQLite"], GREEN, False),
        ("stack-integrations.svg", "Integrations", ["Twilio", "ElevenLabs", "Deepgram", "OpenAI"], BLUE, False),
        ("stack-tools.svg", "Tools", ["Git", "GitHub", "Postman"], PURPLE, False),
    ]
    for fname, title, items, accent, anim in stack_specs:
        (assets / fname).write_text(build_stack_card(title, items, accent, anim), encoding="utf-8")

    focus_specs = [
        (
            "focus-app-dev.svg",
            "app-dev",
            "Application Development",
            "End-to-end web and mobile apps with",
            "React, Flutter, and clean UI structure.",
            BLUE,
            False,
        ),
        (
            "focus-api.svg",
            "api",
            "API Engineering",
            "RESTful services, request validation,",
            "and integrations with Python & FastAPI.",
            GREEN,
            True,
        ),
        (
            "focus-database.svg",
            "database",
            "Database Engineering",
            "Relational schemas, ORM workflows, and",
            "persistence across SQL and Firebase.",
            PURPLE,
            False,
        ),
        (
            "focus-problem-solving.svg",
            "problem-solving",
            "Problem Solving",
            "Algorithms, data structures, and",
            "structured debugging in Java & Python.",
            GREEN,
            False,
        ),
    ]
    for fname, key, title, l1, l2, accent, glow in focus_specs:
        (assets / fname).write_text(build_focus_card(key, title, l1, l2, accent, glow), encoding="utf-8")

    (assets / "exploring-status.svg").write_text(build_exploring_status(), encoding="utf-8")
    (assets / "exploring-topics.svg").write_text(build_exploring_topics(), encoding="utf-8")
    (assets / "badge-email.svg").write_text(build_email_badge(), encoding="utf-8")
    print("Generated 13 dashboard SVG assets in assets/")


if __name__ == "__main__":
    main()
