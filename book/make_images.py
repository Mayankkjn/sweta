"""Draws the colourful illustrations for the Class 2 Hindi book as SVG and renders them to PNG."""
import os
import math
import cairosvg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

W, H = 600, 330


# ---------------------------------------------------------------- helpers
def svg(body, defs="", w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>')


def grad(gid, c1, c2, vertical=True):
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    return f'<linearGradient id="{gid}" {xy}><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'


def frame(body, defs="", bg="#fff"):
    # rounded border so each picture looks like a book illustration
    return svg(f'<clipPath id="clip"><rect x="4" y="4" width="{W-8}" height="{H-8}" rx="22"/></clipPath>'
               f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{bg}"/>{body}</g>'
               f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="22" fill="none" stroke="#ff8a00" stroke-width="6"/>',
               defs)


def sun(x, y, r=28, face=True):
    rays = "".join(
        f'<line x1="{x + math.cos(a) * (r + 6):.1f}" y1="{y + math.sin(a) * (r + 6):.1f}" '
        f'x2="{x + math.cos(a) * (r + 18):.1f}" y2="{y + math.sin(a) * (r + 18):.1f}" stroke="#ffb300" stroke-width="5" stroke-linecap="round"/>'
        for a in [i * math.pi / 6 for i in range(12)])
    f = ""
    if face:
        f = (f'<circle cx="{x - r * .3}" cy="{y - r * .15}" r="3" fill="#6d3b00"/>'
             f'<circle cx="{x + r * .3}" cy="{y - r * .15}" r="3" fill="#6d3b00"/>'
             f'<path d="M{x - r * .35},{y + r * .2} Q{x},{y + r * .55} {x + r * .35},{y + r * .2}" stroke="#6d3b00" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<circle cx="{x - r * .55}" cy="{y + r * .2}" r="4" fill="#ff7043" opacity=".6"/>'
             f'<circle cx="{x + r * .55}" cy="{y + r * .2}" r="4" fill="#ff7043" opacity=".6"/>')
    return f'{rays}<circle cx="{x}" cy="{y}" r="{r}" fill="#ffd600" stroke="#ffb300" stroke-width="3"/>{f}'


def cloud(x, y, s=1.0, c="#ffffff", stroke="#cfd8dc"):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{c}" stroke="{stroke}" stroke-width="2">'
            f'<ellipse cx="0" cy="0" rx="40" ry="20"/><circle cx="-20" cy="-10" r="20"/>'
            f'<circle cx="12" cy="-18" r="24"/><circle cx="32" cy="-4" r="16"/>'
            f'<ellipse cx="0" cy="2" rx="38" ry="16" stroke="none"/></g>')


def tree(x, y, s=1.0, leaf="#43a047", leaf2="#66bb6a", fruit=None):
    fr = ""
    if fruit:
        for fx, fy in [(-18, -78), (14, -92), (22, -66), (-6, -100), (-26, -96), (4, -70)]:
            fr += f'<circle cx="{fx}" cy="{fy}" r="5" fill="{fruit}" stroke="#00000033"/>'
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-8,0 L-6,-50 L6,-50 L8,0 Z" fill="#8d5524"/>'
            f'<circle cx="0" cy="-80" r="34" fill="{leaf}"/><circle cx="-24" cy="-64" r="22" fill="{leaf}"/>'
            f'<circle cx="24" cy="-64" r="22" fill="{leaf}"/><circle cx="-8" cy="-92" r="18" fill="{leaf2}"/>'
            f'<circle cx="14" cy="-84" r="12" fill="{leaf2}"/>{fr}</g>')


def flower(x, y, c="#e91e63", s=1.0):
    petals = "".join(f'<circle cx="{math.cos(a) * 6:.1f}" cy="{-22 + math.sin(a) * 6:.1f}" r="5" fill="{c}"/>'
                     for a in [i * math.pi * 2 / 5 for i in range(5)])
    return (f'<g transform="translate({x},{y}) scale({s})"><line x1="0" y1="0" x2="0" y2="-20" stroke="#2e7d32" stroke-width="3"/>'
            f'<ellipse cx="5" cy="-8" rx="6" ry="3" fill="#43a047"/>{petals}<circle cx="0" cy="-22" r="4" fill="#ffeb3b"/></g>')


def kid(x, y, s=1.0, girl=False, skin="#f1c27d", hair="#3e2723", top="#e53935", bottom="#1e88e5",
        arms="down", flip=False, mouth="smile"):
    """A cartoon child standing with feet at (x, y)."""
    sx = -s if flip else s
    if arms == "up":
        a = ('<path d="M-14,-66 L-30,-92" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<path d="M14,-66 L30,-92" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<circle cx="-31" cy="-95" r="5" fill="{k}"/><circle cx="31" cy="-95" r="5" fill="{k}"/>')
    elif arms == "wave":
        a = ('<path d="M-14,-66 L-24,-40" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<path d="M14,-66 L30,-92" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<circle cx="-25" cy="-37" r="5" fill="{k}"/><circle cx="31" cy="-95" r="5" fill="{k}"/>')
    elif arms == "front":
        a = ('<path d="M-14,-66 L-4,-50 L18,-52" stroke="{c}" stroke-width="7" stroke-linecap="round" fill="none"/>'
             '<path d="M14,-66 L30,-52" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<circle cx="22" cy="-52" r="5" fill="{k}"/><circle cx="33" cy="-51" r="5" fill="{k}"/>')
    else:
        a = ('<path d="M-14,-66 L-22,-40" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<path d="M14,-66 L22,-40" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'
             '<circle cx="-23" cy="-37" r="5" fill="{k}"/><circle cx="23" cy="-37" r="5" fill="{k}"/>')
    a = a.replace("{c}", top).replace("{k}", skin)
    legs = (f'<rect x="-10" y="-34" width="7" height="32" rx="3" fill="{skin}"/>'
            f'<rect x="3" y="-34" width="7" height="32" rx="3" fill="{skin}"/>'
            f'<ellipse cx="-8" cy="-1" rx="8" ry="4" fill="#5d4037"/><ellipse cx="8" cy="-1" rx="8" ry="4" fill="#5d4037"/>')
    if girl:
        body = f'<path d="M-13,-70 L13,-70 L22,-28 L-22,-28 Z" fill="{top}"/><path d="M-20,-34 L20,-34 L22,-28 L-22,-28 Z" fill="{bottom}"/>'
        hr = (f'<circle cx="-17" cy="-86" r="7" fill="{hair}"/><circle cx="17" cy="-86" r="7" fill="{hair}"/>'
              f'<path d="M-17,-88 A17,17 0 0 1 17,-88 Q8,-98 0,-92 Q-8,-98 -17,-88 Z" fill="{hair}"/>'
              f'<circle cx="-20" cy="-80" r="3" fill="#ff4081"/><circle cx="20" cy="-80" r="3" fill="#ff4081"/>')
    else:
        body = (f'<rect x="-14" y="-70" width="28" height="36" rx="6" fill="{top}"/>'
                f'<rect x="-14" y="-38" width="28" height="12" rx="3" fill="{bottom}"/>')
        hr = f'<path d="M-17,-88 A17,17 0 0 1 17,-88 Q10,-96 2,-92 Q-6,-99 -17,-88 Z" fill="{hair}"/>'
        legs = legs.replace('y="-34"', 'y="-28"').replace('height="32"', 'height="26"')
    if mouth == "open":
        m = '<ellipse cx="0" cy="-78" rx="4" ry="5" fill="#b71c1c"/>'
    elif mouth == "sad":
        m = '<path d="M-5,-76 Q0,-81 5,-76" stroke="#5d4037" stroke-width="2" fill="none" stroke-linecap="round"/>'
    else:
        m = '<path d="M-6,-80 Q0,-73 6,-80" stroke="#5d4037" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    face = (f'<rect x="-4" y="-74" width="8" height="6" fill="{skin}"/>'
            f'<circle cx="0" cy="-86" r="17" fill="{skin}"/>{hr}'
            f'<circle cx="-6" cy="-87" r="2.4" fill="#212121"/><circle cx="6" cy="-87" r="2.4" fill="#212121"/>'
            f'<circle cx="-11" cy="-80" r="3" fill="#ff8a80" opacity=".7"/><circle cx="11" cy="-80" r="3" fill="#ff8a80" opacity=".7"/>{m}')
    return f'<g transform="translate({x},{y}) scale({sx},{s})">{legs}{a}{body}{face}</g>'


def grass_strip(y, c1="#7cb342", c2="#558b2f"):
    blades = "".join(f'<path d="M{i},{y} l4,-10 l4,10" fill="{c2}"/>' for i in range(0, W, 14))
    return f'<rect x="0" y="{y}" width="{W}" height="{H - y}" fill="{c1}"/>{blades}'


def bird(x, y, s=1.0, c="#37474f"):
    return f'<path transform="translate({x},{y}) scale({s})" d="M-10,0 Q-5,-7 0,0 Q5,-7 10,0" stroke="{c}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'


def arrow(x1, y1, x2, y2, c="#ff6f00"):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - 12 * math.cos(ang - .5)
    hy1 = y2 - 12 * math.sin(ang - .5)
    hx2 = x2 - 12 * math.cos(ang + .5)
    hy2 = y2 - 12 * math.sin(ang + .5)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M{x2},{y2} L{hx1:.1f},{hy1:.1f} L{hx2:.1f},{hy2:.1f} Z" fill="{c}"/>')


def badge(x, y, n, c="#d81b60"):
    return (f'<circle cx="{x}" cy="{y}" r="13" fill="{c}" stroke="#fff" stroke-width="3"/>'
            f'<text x="{x}" y="{y + 6}" font-family="DejaVu Sans" font-weight="bold" font-size="16" fill="#fff" text-anchor="middle">{n}</text>')


def drop_char(x, y, s=1.0, c="#29b6f6", mood="smile"):
    m = ('<path d="M-6,8 Q0,14 6,8" stroke="#01579b" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
         if mood == "smile" else '<ellipse cx="0" cy="10" rx="4" ry="5" fill="#01579b"/>')
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M0,-30 C10,-14 20,-2 20,10 A20,20 0 0 1 -20,10 C-20,-2 -10,-14 0,-30 Z" fill="{c}" stroke="#0277bd" stroke-width="2"/>'
            f'<ellipse cx="-8" cy="-4" rx="4" ry="7" fill="#fff" opacity=".6"/>'
            f'<circle cx="-6" cy="2" r="2.6" fill="#01579b"/><circle cx="6" cy="2" r="2.6" fill="#01579b"/>'
            f'<circle cx="-11" cy="9" r="3" fill="#f48fb1" opacity=".8"/><circle cx="11" cy="9" r="3" fill="#f48fb1" opacity=".8"/>{m}</g>')


def save(name, content):
    path = os.path.join(OUT, name + ".png")
    cairosvg.svg2png(bytestring=content.encode("utf-8"), write_to=path, output_width=1200)
    print("wrote", path)


# ---------------------------------------------------------------- pictures
def cover():
    d = grad("sky", "#81d4fa", "#e1f5fe")
    rainbow = "".join(f'<path d="M60,330 A240,220 0 0 1 540,330" stroke="{c}" stroke-width="12" fill="none"/>'
                      .replace("240,220", f"{240 - i * 12},{220 - i * 12}").replace("M60", f"M{60 + i * 12}").replace("540", f"{540 - i * 12}")
                      for i, c in enumerate(["#e53935", "#fb8c00", "#fdd835", "#43a047", "#1e88e5", "#3949ab", "#8e24aa"]))
    book = ('<g transform="translate(300,272)">'
            '<path d="M-150,0 Q-75,-30 0,-8 L0,40 Q-75,18 -150,48 Z" fill="#fff3e0" stroke="#e65100" stroke-width="4"/>'
            '<path d="M150,0 Q75,-30 0,-8 L0,40 Q75,18 150,48 Z" fill="#fffde7" stroke="#e65100" stroke-width="4"/>'
            + "".join(f'<line x1="{-130 + i * 2}" y1="{10 + i * 7}" x2="{-20}" y2="{4 + i * 7}" stroke="#ffab91" stroke-width="3"/>' for i in range(4))
            + "".join(f'<line x1="20" y1="{4 + i * 7}" x2="{130 - i * 2}" y2="{10 + i * 7}" stroke="#a5d6a7" stroke-width="3"/>' for i in range(4))
            + '</g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{rainbow}{sun(520, 60, 30)}'
            f'{cloud(110, 70, 1.1)}{cloud(380, 50, .8)}'
            f'{grass_strip(285)}'
            f'{tree(60, 300, .9, fruit="#ff7043")}{tree(545, 300, .8, fruit="#ffca28")}'
            f'{flower(120, 312, "#e91e63")}{flower(480, 315, "#7e57c2")}{flower(150, 318, "#ff9800")}'
            f'{book}'
            f'{kid(200, 258, 1.0, girl=True, top="#ec407a", bottom="#ffca28", arms="up")}'
            f'{kid(400, 258, 1.0, girl=False, top="#29b6f6", bottom="#3949ab", arms="wave", skin="#e0ac69", flip=True)}'
            f'{bird(240, 70)}{bird(270, 85, .8)}{bird(330, 100, .7)}')
    save("cover", frame(body, d))


def paper_tree():
    """Riya with the talking page Pannu, dreaming of the tree in the forest."""
    d = grad("sky", "#b3e5fc", "#fffde7")
    pannu = ('<g transform="translate(330,170) rotate(-8)">'
             '<rect x="-38" y="-50" width="76" height="100" rx="6" fill="#ffffff" stroke="#5c6bc0" stroke-width="3"/>'
             + "".join(f'<line x1="-30" y1="{-30 + i * 14}" x2="30" y2="{-30 + i * 14}" stroke="#90caf9" stroke-width="2"/>' for i in range(6))
             + '<line x1="-22" y1="-50" x2="-22" y2="50" stroke="#ef9a9a" stroke-width="2"/>'
             '<circle cx="-10" cy="-8" r="6" fill="#fff" stroke="#212121" stroke-width="2"/><circle cx="-9" cy="-7" r="3" fill="#212121"/>'
             '<circle cx="12" cy="-8" r="6" fill="#fff" stroke="#212121" stroke-width="2"/><circle cx="13" cy="-7" r="3" fill="#212121"/>'
             '<path d="M-10,12 Q1,26 14,12" stroke="#d32f2f" stroke-width="3" fill="#ffcdd2"/>'
             '<path d="M-38,0 L-58,-14" stroke="#5c6bc0" stroke-width="4" stroke-linecap="round"/>'
             '<path d="M38,0 L58,-18" stroke="#5c6bc0" stroke-width="4" stroke-linecap="round"/></g>')
    bubble = ('<ellipse cx="470" cy="110" rx="110" ry="88" fill="#e8f5e9" stroke="#66bb6a" stroke-width="4"/>'
              '<circle cx="380" cy="190" r="10" fill="#e8f5e9" stroke="#66bb6a" stroke-width="3"/>'
              '<circle cx="364" cy="210" r="6" fill="#e8f5e9" stroke="#66bb6a" stroke-width="3"/>'
              '<clipPath id="bub"><ellipse cx="470" cy="110" rx="106" ry="84"/></clipPath>'
              '<g clip-path="url(#bub)"><rect x="360" y="140" width="230" height="80" fill="#9ccc65"/>'
              f'{tree(470, 160, 1.15, fruit=None)}{tree(405, 165, .6, leaf="#2e7d32")}{tree(540, 168, .65, leaf="#388e3c")}'
              f'{bird(445, 50, .8, "#6d4c41")}{bird(500, 45, .7, "#6d4c41")}'
              '<g transform="translate(492,128)"><ellipse cx="0" cy="0" rx="8" ry="6" fill="#a1887f"/><circle cx="7" cy="-5" r="4" fill="#a1887f"/>'
              '<path d="M-8,0 Q-18,-12 -10,-18" stroke="#a1887f" stroke-width="6" fill="none" stroke-linecap="round"/></g></g>')
    boats = "".join(f'<path transform="translate({x},{y})" d="M-16,0 L16,0 L10,8 L-10,8 Z M-6,0 L0,-14 L6,0 Z" fill="#fff" stroke="#7986cb" stroke-width="2"/>'
                    for x, y in [(90, 300), (150, 312), (250, 305)])
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
            f'<rect x="0" y="250" width="{W}" height="80" fill="#ffe0b2"/>'
            f'<rect x="20" y="40" width="130" height="90" rx="6" fill="#fff8e1" stroke="#8d6e63" stroke-width="5"/>'
            f'<line x1="85" y1="40" x2="85" y2="130" stroke="#8d6e63" stroke-width="4"/><line x1="20" y1="85" x2="150" y2="85" stroke="#8d6e63" stroke-width="4"/>'
            f'{sun(110, 70, 14, face=False)}'
            f'{kid(200, 285, 1.35, girl=True, top="#ab47bc", bottom="#ffee58", arms="up", mouth="open")}'
            f'{boats}{pannu}{bubble}')
    save("ch1_pannu", frame(body, d))


def paper_process():
    d = grad("bg", "#fff8e1", "#ffe0b2")
    logs = ('<g transform="translate(70,200)">'
            + "".join(f'<rect x="{-40 + (i % 3) * 26}" y="{-20 - (i // 3) * 22}" width="26" height="22" rx="4" fill="#a1887f" stroke="#5d4037" stroke-width="2"/>'
                      f'<circle cx="{-27 + (i % 3) * 26}" cy="{-9 - (i // 3) * 22}" r="7" fill="#d7ccc8" stroke="#8d6e63" stroke-width="2"/>'
                      for i in range(5)) + '</g>')
    chipper = ('<g transform="translate(185,170)"><rect x="-38" y="-30" width="76" height="60" rx="8" fill="#ef5350" stroke="#b71c1c" stroke-width="3"/>'
               '<path d="M-24,-30 L-14,-52 L14,-52 L24,-30 Z" fill="#ffa726" stroke="#e65100" stroke-width="3"/>'
               '<circle cx="-12" cy="0" r="10" fill="#fff" stroke="#b71c1c" stroke-width="3"/><circle cx="14" cy="0" r="10" fill="#fff" stroke="#b71c1c" stroke-width="3"/>'
               + "".join(f'<rect x="{-30 + i * 11}" y="{40 + (i % 2) * 6}" width="8" height="6" fill="#bcaaa4"/>' for i in range(6)) + '</g>')
    vat = ('<g transform="translate(300,180)"><path d="M-48,-30 L48,-30 L40,40 L-40,40 Z" fill="#42a5f5" stroke="#0d47a1" stroke-width="3"/>'
           '<ellipse cx="0" cy="-30" rx="48" ry="10" fill="#e0e0e0" stroke="#0d47a1" stroke-width="3"/>'
           + "".join(f'<circle cx="{-30 + i * 15}" cy="{-34 - (i % 2) * 8}" r="{4 + i % 3}" fill="#fafafa" stroke="#90a4ae"/>' for i in range(5))
           + '<path d="M-20,-40 q-6,-10 0,-18 q6,-8 0,-16" stroke="#b0bec5" stroke-width="3" fill="none"/>'
           '<path d="M10,-44 q-6,-10 0,-18 q6,-8 0,-16" stroke="#b0bec5" stroke-width="3" fill="none"/>'
           '<path d="M-30,48 L-20,40 M30,48 L20,40" stroke="#0d47a1" stroke-width="3"/>'
           '<path d="M-36,52 Q0,64 36,52" stroke="#ff7043" stroke-width="8" fill="none"/></g>')
    rollers = ('<g transform="translate(425,180)"><rect x="-60" y="-4" width="120" height="8" fill="#fff" stroke="#bdbdbd" stroke-width="2"/>'
               + "".join(f'<circle cx="{-42 + i * 42}" cy="-20" r="16" fill="#7e57c2" stroke="#4527a0" stroke-width="3"/><circle cx="{-42 + i * 42}" cy="-20" r="5" fill="#d1c4e9"/>'
                         f'<circle cx="{-42 + i * 42}" cy="20" r="16" fill="#26a69a" stroke="#00695c" stroke-width="3"/><circle cx="{-42 + i * 42}" cy="20" r="5" fill="#b2dfdb"/>'
                         for i in range(3)) + '</g>')
    roll = ('<g transform="translate(540,180)"><rect x="-30" y="-40" width="60" height="70" fill="#fafafa" stroke="#9e9e9e" stroke-width="3"/>'
            '<ellipse cx="0" cy="-40" rx="30" ry="10" fill="#fff" stroke="#9e9e9e" stroke-width="3"/><ellipse cx="0" cy="-40" rx="8" ry="3" fill="#8d6e63"/>'
            '<g transform="translate(6,52) rotate(-6)"><rect x="-26" y="-14" width="52" height="34" rx="3" fill="#ffca28" stroke="#f57f17" stroke-width="3"/>'
            '<rect x="-14" y="-6" width="28" height="10" fill="#fff"/></g></g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<rect x="0" y="250" width="{W}" height="80" fill="#bcaaa4"/><rect x="0" y="250" width="{W}" height="6" fill="#8d6e63"/>'
            f'{logs}{chipper}{vat}{rollers}{roll}'
            f'{arrow(110, 175, 140, 175)}{arrow(228, 175, 248, 175)}{arrow(352, 175, 362, 175)}{arrow(488, 175, 505, 175)}'
            f'{badge(70, 105, 1)}{badge(185, 90, 2)}{badge(300, 98, 3)}{badge(425, 130, 4)}{badge(540, 105, 5)}'
            f'{cloud(120, 50, .6)}{cloud(450, 45, .7)}'
            f'{kid(520, 315, .55, girl=True, top="#ab47bc", bottom="#ffee58", arms="wave")}')
    save("ch1_process", frame(body, d))


def rain_poem():
    d = grad("sky", "#78909c", "#cfd8dc")
    drops = "".join(f'<line x1="{x}" y1="{y}" x2="{x - 5}" y2="{y + 14}" stroke="#4fc3f7" stroke-width="3" stroke-linecap="round"/>'
                    for x in range(30, 600, 34) for y in range(100 if x % 3 else 120, 250, 46))
    umbrella = ('<g transform="translate(245,180)"><path d="M-55,0 A55,45 0 0 1 55,0 Q41,-10 27,0 Q14,-10 0,0 Q-14,-10 -27,0 Q-41,-10 -55,0 Z" fill="#ff1744" stroke="#b71c1c" stroke-width="3"/>'
                '<path d="M-27,0 A27,45 0 0 1 0,-45 A27,45 0 0 1 27,0" fill="#ffea00" opacity=".9"/>'
                '<line x1="0" y1="-45" x2="0" y2="50" stroke="#4e342e" stroke-width="4"/></g>')
    frog = ('<g transform="translate(520,292)"><ellipse cx="0" cy="0" rx="26" ry="16" fill="#66bb6a" stroke="#2e7d32" stroke-width="3"/>'
            '<circle cx="-12" cy="-16" r="9" fill="#66bb6a" stroke="#2e7d32" stroke-width="3"/><circle cx="12" cy="-16" r="9" fill="#66bb6a" stroke="#2e7d32" stroke-width="3"/>'
            '<circle cx="-12" cy="-17" r="4" fill="#212121"/><circle cx="12" cy="-17" r="4" fill="#212121"/>'
            '<path d="M-12,0 Q0,10 12,0" stroke="#1b5e20" stroke-width="3" fill="none"/></g>')
    boat = '<path transform="translate(400,292)" d="M-28,0 L28,0 L18,14 L-18,14 Z M-10,0 L0,-26 L10,0 Z" fill="#fff" stroke="#e65100" stroke-width="3"/>'
    peacock = ('<g transform="translate(90,250)">'
               + "".join(f'<ellipse cx="{math.cos(a) * 34:.1f}" cy="{math.sin(a) * 34 - 20:.1f}" rx="12" ry="20" transform="rotate({math.degrees(a) + 90:.0f} {math.cos(a) * 34:.1f} {math.sin(a) * 34 - 20:.1f})" fill="#00897b" stroke="#004d40" stroke-width="2"/>'
                         f'<circle cx="{math.cos(a) * 40:.1f}" cy="{math.sin(a) * 40 - 20:.1f}" r="5" fill="#1a237e"/>'
                         for a in [math.pi + i * math.pi / 8 for i in range(9)])
               + '<ellipse cx="0" cy="0" rx="12" ry="22" fill="#1565c0"/><circle cx="0" cy="-28" r="9" fill="#1565c0"/>'
               '<path d="M8,-28 L18,-25 L8,-23 Z" fill="#ffb300"/><circle cx="3" cy="-30" r="2" fill="#fff"/>'
               '<path d="M-2,-37 L-4,-48 M2,-37 L4,-48" stroke="#1565c0" stroke-width="2"/></g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
            f'{cloud(100, 60, 1.4, "#546e7a", "#37474f")}{cloud(300, 50, 1.6, "#607d8b", "#37474f")}{cloud(500, 65, 1.3, "#546e7a", "#37474f")}'
            f'<path d="M330,70 L310,110 L325,110 L305,150" stroke="#ffee58" stroke-width="6" fill="none" stroke-linejoin="round"/>'
            f'{drops}{grass_strip(270)}'
            f'<ellipse cx="440" cy="300" rx="130" ry="20" fill="#4fc3f7" opacity=".8"/>'
            f'{peacock}{umbrella}'
            f'{kid(225, 280, 1.0, girl=True, top="#7e57c2", bottom="#ffca28", arms="up", mouth="open")}'
            f'{kid(275, 280, 1.0, top="#ff7043", bottom="#1565c0", arms="up", skin="#c68642", flip=True, mouth="open")}'
            f'{boat}{frog}')
    save("poem1_rain", frame(body, d))


def tea_garden():
    d = grad("sky", "#80deea", "#e0f7fa")
    hills = ('<path d="M0,140 Q120,70 260,120 T600,95 L600,330 L0,330 Z" fill="#a5d6a7"/>'
             '<path d="M0,180 Q150,120 300,170 T600,150 L600,330 L0,330 Z" fill="#81c784"/>')
    rows = ""
    for r in range(5):
        y = 190 + r * 28
        rows += "".join(f'<ellipse cx="{x + (r % 2) * 20}" cy="{y}" rx="24" ry="13" fill="{"#2e7d32" if (x // 44 + r) % 2 else "#388e3c"}"/>'
                        for x in range(-10, 640, 44))
    woman = ('<g transform="translate(390,262)">'
             '<path d="M-14,-62 L14,-62 L22,0 L-22,0 Z" fill="#ffeb3b"/><path d="M-22,-8 L22,-8 L22,0 L-22,0 Z" fill="#e53935"/>'
             '<path d="M-14,-62 L22,-20 L18,-14 L-14,-54 Z" fill="#e53935"/>'
             '<path d="M10,-76 L34,-76 L28,-30 L16,-30 Z" fill="#d7a86e" stroke="#8d6e63" stroke-width="3"/>'
             + "".join(f'<line x1="{12 + i * 4}" y1="-74" x2="{18 + i * 2}" y2="-32" stroke="#a1887f" stroke-width="1.5"/>' for i in range(5))
             + '<ellipse cx="22" cy="-78" rx="12" ry="5" fill="#43a047"/>'
             '<circle cx="0" cy="-76" r="14" fill="#c68642"/><path d="M-14,-78 A14,14 0 0 1 14,-78 L14,-70 L-14,-70 Z" fill="#212121"/>'
             '<circle cx="-5" cy="-75" r="2" fill="#212121"/><circle cx="5" cy="-75" r="2" fill="#212121"/>'
             '<path d="M-5,-69 Q0,-65 5,-69" stroke="#4e342e" stroke-width="2" fill="none"/><circle cx="0" cy="-82" r="2" fill="#e53935"/>'
             '<path d="M-14,-56 L-30,-36" stroke="#c68642" stroke-width="6" stroke-linecap="round"/><ellipse cx="-32" cy="-34" rx="6" ry="4" fill="#66bb6a"/></g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{sun(90, 60, 24)}'
            f'{cloud(260, 50, .8)}{cloud(480, 70, .9)}{hills}'
            f'<path d="M0,240 Q300,180 600,230" stroke="none" fill="none"/>'
            f'{rows}{tree(560, 200, .7, leaf="#1b5e20")}{tree(30, 190, .6, leaf="#1b5e20")}'
            f'{woman}'
            f'{kid(230, 300, 1.05, top="#29b6f6", bottom="#5d4037", arms="wave", skin="#e0ac69")}'
            f'{kid(165, 300, 1.25, top="#43a047", bottom="#795548", skin="#d1a26b", hair="#212121")}'
            f'{bird(330, 60)}{bird(360, 75, .8)}')
    save("ch2_tea", frame(body, d))


def kaziranga():
    d = grad("sky", "#ffe082", "#fff8e1")
    rhino = ('<g transform="translate(250,240)">'
             '<ellipse cx="0" cy="0" rx="80" ry="45" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<path d="M-30,-40 Q-20,-10 -30,40" stroke="#78909c" stroke-width="4" fill="none"/>'
             '<path d="M20,-42 Q30,-10 20,42" stroke="#78909c" stroke-width="4" fill="none"/>'
             '<rect x="-60" y="25" width="22" height="45" rx="6" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<rect x="-25" y="30" width="22" height="40" rx="6" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<rect x="30" y="30" width="22" height="40" rx="6" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<rect x="55" y="25" width="20" height="45" rx="6" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<path d="M70,-20 Q130,-30 140,10 Q140,30 110,30 Q80,30 70,20 Z" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<path d="M126,-4 L140,-46 L144,-2 Z" fill="#eceff1" stroke="#455a64" stroke-width="3"/>'
             '<path d="M108,-14 L112,-30 L118,-12 Z" fill="#eceff1" stroke="#455a64" stroke-width="2"/>'
             '<path d="M84,-24 L78,-44 L94,-30 Z" fill="#90a4ae" stroke="#455a64" stroke-width="3"/>'
             '<circle cx="104" cy="-4" r="4" fill="#212121"/><circle cx="105" cy="-5" r="1.4" fill="#fff"/>'
             '<path d="M118,18 Q126,22 134,18" stroke="#455a64" stroke-width="3" fill="none"/>'
             '<path d="M-80,-4 Q-96,6 -90,20" stroke="#455a64" stroke-width="4" fill="none"/></g>')
    grass = "".join(f'<path d="M{x},330 Q{x + 4},{270 - (x * 7) % 30} {x + 10},{258 - (x * 13) % 40}" stroke="{c}" stroke-width="4" fill="none"/>'
                    for x, c in zip(range(0, 600, 9), ["#9e9d24", "#afb42b", "#827717", "#c0ca33"] * 70))
    boat = ('<g transform="translate(470,170)"><path d="M-50,0 L50,0 Q40,16 0,16 Q-40,16 -50,0 Z" fill="#8d6e63" stroke="#4e342e" stroke-width="3"/>'
            '<path d="M-20,0 A20,16 0 0 1 20,0 Z" fill="#ffb74d" stroke="#e65100" stroke-width="2"/>'
            '<line x1="38" y1="-30" x2="20" y2="20" stroke="#4e342e" stroke-width="3"/></g>')
    egret = ('<g transform="translate(330,192)"><ellipse cx="0" cy="0" rx="9" ry="6" fill="#fff"/><circle cx="8" cy="-6" r="4" fill="#fff"/>'
             '<path d="M11,-6 L18,-5" stroke="#fbc02d" stroke-width="2"/></g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{sun(500, 60, 26)}'
            '<path d="M0,120 L80,70 L150,110 L240,60 L330,115 L420,80 L520,120 L600,95 L600,170 L0,170 Z" fill="#7986cb" opacity=".6"/>'
            '<path d="M0,150 Q150,130 300,150 T600,145 L600,200 L0,200 Z" fill="#4fc3f7"/>'
            '<path d="M40,165 q20,-6 40,0 M200,180 q20,-6 40,0 M380,160 q20,-6 40,0" stroke="#e1f5fe" stroke-width="3" fill="none"/>'
            f'{boat}<rect x="0" y="195" width="{W}" height="135" fill="#c5e1a5"/>'
            f'{tree(40, 210, .7, leaf="#33691e")}{tree(570, 205, .6, leaf="#33691e")}'
            f'{egret}{rhino}{grass}{bird(150, 60)}{bird(180, 75, .8)}{bird(400, 40, .7)}')
    save("ch2_rhino", frame(body, d))


def litter_monster():
    d = grad("sky", "#bcaaa4", "#d7ccc8")
    trash = ""
    for x, y, kind in [(60, 300, 0), (140, 290, 1), (470, 305, 2), (540, 288, 0), (260, 312, 1), (380, 300, 2)]:
        if kind == 0:
            trash += f'<rect x="{x}" y="{y}" width="12" height="28" rx="4" fill="#4dd0e1" transform="rotate(70 {x} {y})" stroke="#00838f" stroke-width="2"/>'
        elif kind == 1:
            trash += f'<path d="M{x},{y} l20,-6 l8,10 l-18,8 Z" fill="#ffca28" stroke="#f57f17" stroke-width="2"/>'
        else:
            trash += f'<circle cx="{x}" cy="{y}" r="9" fill="#eeeeee" stroke="#9e9e9e" stroke-width="2"/>'
    monster = ('<g transform="translate(300,215)">'
               '<path d="M-90,80 Q-110,10 -70,-30 Q-60,-90 0,-85 Q70,-95 75,-30 Q115,10 95,80 Z" fill="#8d6e63" stroke="#4e342e" stroke-width="4"/>'
               '<path d="M-60,-20 l18,-8 l6,14 l-18,6 Z" fill="#ffca28"/><rect x="40" y="10" width="12" height="30" rx="4" fill="#4dd0e1" transform="rotate(30 40 10)"/>'
               '<circle cx="-40" cy="50" r="10" fill="#eeeeee"/><path d="M50,55 l20,-4 l2,14 l-20,4 Z" fill="#ef5350"/>'
               '<circle cx="-28" cy="-40" r="18" fill="#fff" stroke="#4e342e" stroke-width="3"/><circle cx="-24" cy="-38" r="8" fill="#d50000"/>'
               '<circle cx="28" cy="-40" r="18" fill="#fff" stroke="#4e342e" stroke-width="3"/><circle cx="24" cy="-38" r="8" fill="#d50000"/>'
               '<path d="M-48,-64 L-12,-54 M48,-64 L12,-54" stroke="#3e2723" stroke-width="6" stroke-linecap="round"/>'
               '<path d="M-40,0 Q0,30 40,0 L30,14 L20,4 L10,16 L0,6 L-10,16 L-20,4 L-30,14 Z" fill="#3e2723"/>'
               '<path d="M-90,20 L-130,-10" stroke="#8d6e63" stroke-width="16" stroke-linecap="round"/>'
               '<path d="M90,20 L130,-14" stroke="#8d6e63" stroke-width="16" stroke-linecap="round"/></g>')
    flies = "".join(f'<g transform="translate({x},{y})"><ellipse cx="0" cy="0" rx="4" ry="3" fill="#212121"/>'
                    f'<ellipse cx="-3" cy="-4" rx="3" ry="2" fill="#cfd8dc"/><ellipse cx="3" cy="-4" rx="3" ry="2" fill="#cfd8dc"/></g>'
                    for x, y in [(210, 90), (380, 80), (420, 130), (180, 150), (350, 50)])
    smell = "".join(f'<path d="M{x},120 q-8,-12 0,-24 q8,-12 0,-24" stroke="#9ccc65" stroke-width="4" fill="none" opacity=".8"/>'
                    for x in [200, 230, 380, 410])
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{grass_strip(280, "#a1887f", "#8d6e63")}'
            f'{tree(50, 285, .7, leaf="#827717", leaf2="#9e9d24")}'
            f'{monster}{smell}{flies}{trash}'
            f'{kid(510, 300, 1.3, top="#ff7043", bottom="#1565c0", skin="#e0ac69", mouth="open", arms="up", flip=True)}')
    save("ch3_monster", frame(body, d))


def clean_park():
    d = grad("sky", "#81d4fa", "#e1f5fe")

    def bin_(x, c, dark):
        return (f'<g transform="translate({x},300)"><path d="M-22,-50 L22,-50 L18,0 L-18,0 Z" fill="{c}" stroke="{dark}" stroke-width="3"/>'
                f'<rect x="-26" y="-58" width="52" height="10" rx="4" fill="{dark}"/>'
                f'<path d="M-8,-30 l8,-10 l8,10 M-8,-18 l16,0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    broom = '<g transform="translate(140,250) rotate(25)"><line x1="0" y1="-50" x2="0" y2="20" stroke="#8d6e63" stroke-width="4"/><path d="M-12,20 L12,20 L16,46 L-16,46 Z" fill="#ffd54f" stroke="#f9a825" stroke-width="2"/></g>'
    glasses = ('<g transform="translate(300,60)"><circle cx="-26" cy="0" r="20" fill="none" stroke="#424242" stroke-width="5"/>'
               '<circle cx="26" cy="0" r="20" fill="none" stroke="#424242" stroke-width="5"/>'
               '<path d="M-6,0 Q0,-6 6,0" stroke="#424242" stroke-width="5" fill="none"/>'
               '<path d="M-46,0 L-62,-6 M46,0 L62,-6" stroke="#424242" stroke-width="5"/></g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{sun(530, 55, 26)}{cloud(120, 50, .9)}'
            f'{glasses}{grass_strip(260)}'
            f'{tree(40, 280, .8, fruit="#ef5350")}{tree(580, 275, .75, fruit="#ffca28")}'
            + "".join(flower(x, 320, c) for x, c in [(70, "#e91e63"), (100, "#ff9800"), (520, "#7e57c2"), (555, "#e91e63"), (330, "#ffeb3b")])
            + f'{bin_(250, "#43a047", "#1b5e20")}{bin_(310, "#1e88e5", "#0d47a1")}'
            f'{broom}{kid(120, 300, 1.05, top="#ff7043", bottom="#1565c0", skin="#e0ac69", arms="front")}'
            f'{kid(200, 300, 1.0, girl=True, top="#ec407a", bottom="#ffee58", arms="wave")}'
            f'{kid(390, 300, 1.0, top="#26a69a", bottom="#5d4037", skin="#c68642", arms="up", mouth="open")}'
            f'{kid(460, 300, 1.05, girl=True, top="#ffa726", bottom="#7e57c2", skin="#d1a26b", arms="wave", flip=True)}'
            f'{bird(200, 110)}{bird(420, 120, .8)}')
    save("ch3_clean", frame(body, d))


def tree_poem():
    d = grad("sky", "#b2ebf2", "#f1f8e9")
    nest = ('<g transform="translate(330,120)"><ellipse cx="0" cy="0" rx="26" ry="12" fill="#8d6e63" stroke="#4e342e" stroke-width="2"/>'
            '<circle cx="-8" cy="-10" r="8" fill="#ffca28"/><circle cx="10" cy="-10" r="8" fill="#ffca28"/>'
            '<path d="M-2,-10 L4,-8 L-2,-6 Z M16,-10 L22,-8 L16,-6 Z" fill="#ff6f00"/>'
            '<circle cx="-10" cy="-12" r="1.5"/><circle cx="8" cy="-12" r="1.5"/></g>')
    swing = ('<line x1="200" y1="160" x2="200" y2="245" stroke="#6d4c41" stroke-width="3"/>'
             '<line x1="240" y1="160" x2="240" y2="245" stroke="#6d4c41" stroke-width="3"/>'
             '<rect x="192" y="244" width="56" height="8" rx="3" fill="#ff7043"/>')
    can = ('<g transform="translate(470,250)"><path d="M-14,-14 L14,-14 L14,14 L-14,14 Z" fill="#29b6f6" stroke="#01579b" stroke-width="2"/>'
           '<path d="M-14,-6 L-36,-20" stroke="#01579b" stroke-width="5"/>'
           '<path d="M-38,-18 q-6,8 -4,16 M-42,-16 q-8,10 -8,18" stroke="#4fc3f7" stroke-width="2" fill="none"/></g>')
    sapling = ('<g transform="translate(415,292)"><path d="M-14,0 L14,0 L10,16 L-10,16 Z" fill="#a1887f"/>'
               '<line x1="0" y1="0" x2="0" y2="-28" stroke="#2e7d32" stroke-width="3"/>'
               '<ellipse cx="-8" cy="-22" rx="9" ry="5" fill="#66bb6a"/><ellipse cx="8" cy="-28" rx="9" ry="5" fill="#66bb6a"/></g>')
    squirrel = ('<g transform="translate(300,210) rotate(-70)"><ellipse cx="0" cy="0" rx="12" ry="8" fill="#a1887f"/><circle cx="12" cy="-4" r="6" fill="#a1887f"/>'
                '<path d="M-12,0 Q-26,-16 -14,-24" stroke="#a1887f" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="14" cy="-6" r="1.5"/></g>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{sun(540, 55, 24)}{cloud(90, 50, .8)}'
            f'{grass_strip(280)}'
            f'{tree(300, 300, 2.6, fruit="#ff7043")}{nest}{squirrel}{swing}'
            f'{kid(220, 290, .9, girl=True, top="#ec407a", bottom="#ffee58", arms="up", mouth="open")}'
            f'{sapling}{kid(490, 300, 1.05, top="#5c6bc0", bottom="#795548", skin="#c68642", arms="front", flip=True)}{can}'
            + "".join(flower(x, 322, c, .9) for x, c in [(40, "#e91e63"), (70, "#ffeb3b"), (100, "#7e57c2"), (560, "#ff9800")])
            + f'{bird(120, 110, 1, "#5d4037")}{bird(150, 95, .8, "#5d4037")}{bird(460, 100, .9, "#5d4037")}')
    save("poem2_tree", frame(body, d))


def robot(x, y, s=1.0, eyes="#00e5ff"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<rect x="-14" y="-6" width="10" height="26" rx="4" fill="#90a4ae"/><rect x="4" y="-6" width="10" height="26" rx="4" fill="#90a4ae"/>'
            '<ellipse cx="-9" cy="22" rx="10" ry="5" fill="#455a64"/><ellipse cx="9" cy="22" rx="10" ry="5" fill="#455a64"/>'
            '<rect x="-30" y="-62" width="60" height="58" rx="12" fill="#ff7043" stroke="#bf360c" stroke-width="3"/>'
            '<rect x="-18" y="-50" width="36" height="24" rx="5" fill="#fff3e0"/>'
            '<circle cx="-8" cy="-38" r="5" fill="#e53935"/><circle cx="8" cy="-38" r="5" fill="#43a047"/>'
            '<rect x="-14" y="-20" width="28" height="6" rx="3" fill="#ffca28"/>'
            '<path d="M-30,-50 L-46,-28" stroke="#90a4ae" stroke-width="8" stroke-linecap="round"/><circle cx="-48" cy="-25" r="7" fill="#78909c"/>'
            '<path d="M30,-50 L48,-72" stroke="#90a4ae" stroke-width="8" stroke-linecap="round"/><circle cx="50" cy="-75" r="7" fill="#78909c"/>'
            '<rect x="-6" y="-70" width="12" height="10" fill="#90a4ae"/>'
            '<rect x="-32" y="-112" width="64" height="44" rx="14" fill="#29b6f6" stroke="#01579b" stroke-width="3"/>'
            f'<rect x="-24" y="-104" width="48" height="26" rx="8" fill="#263238"/>'
            f'<circle cx="-10" cy="-92" r="6" fill="{eyes}"/><circle cx="10" cy="-92" r="6" fill="{eyes}"/>'
            f'<path d="M-8,-83 Q0,-78 8,-83" stroke="{eyes}" stroke-width="2.5" fill="none"/>'
            '<line x1="0" y1="-112" x2="0" y2="-128" stroke="#546e7a" stroke-width="3"/><circle cx="0" cy="-131" r="6" fill="#ffeb3b" stroke="#f9a825" stroke-width="2"/>'
            '<rect x="-38" y="-100" width="6" height="18" rx="3" fill="#01579b"/><rect x="32" y="-100" width="6" height="18" rx="3" fill="#01579b"/></g>')


def robot_room():
    d = grad("wall", "#fff9c4", "#ffecb3")
    window = ('<rect x="410" y="40" width="150" height="110" rx="8" fill="#81d4fa" stroke="#8d6e63" stroke-width="6"/>'
              '<line x1="485" y1="40" x2="485" y2="150" stroke="#8d6e63" stroke-width="5"/>'
              f'{cloud(450, 80, .5)}')
    clock = ('<g transform="translate(90,80)"><circle r="34" fill="#fff" stroke="#e91e63" stroke-width="6"/>'
             + "".join(f'<circle cx="{math.cos(a) * 26:.1f}" cy="{math.sin(a) * 26:.1f}" r="2.5" fill="#880e4f"/>' for a in [i * math.pi / 6 for i in range(12)])
             + '<line x1="0" y1="0" x2="0" y2="-20" stroke="#212121" stroke-width="4" stroke-linecap="round"/>'
             '<line x1="0" y1="0" x2="14" y2="6" stroke="#212121" stroke-width="3" stroke-linecap="round"/></g>')
    shelf = ('<rect x="40" y="170" width="120" height="8" fill="#8d6e63"/>'
             + "".join(f'<rect x="{48 + i * 18}" y="{136 + (i % 2) * 4}" width="14" height="{34 - (i % 2) * 4}" fill="{c}"/>'
                       for i, c in enumerate(["#e53935", "#1e88e5", "#43a047", "#fdd835", "#8e24aa", "#fb8c00"])))
    stars = "".join(f'<path transform="translate({x},{y}) scale(.6)" d="M0,-12 L3,-4 L12,-4 L5,2 L8,11 L0,6 L-8,11 L-5,2 L-12,-4 L-3,-4 Z" fill="#ffd600"/>'
                    for x, y in [(330, 120), (360, 95), (300, 90)])
    body = (f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
            f'<rect x="0" y="250" width="{W}" height="80" fill="#a1887f"/>'
            + "".join(f'<line x1="{x}" y1="250" x2="{x - 30}" y2="330" stroke="#8d6e63" stroke-width="2"/>' for x in range(40, 640, 70))
            + f'{window}{clock}{shelf}{stars}'
            f'{robot(330, 270, 1.15)}'
            f'{kid(200, 285, 1.35, top="#fdd835", bottom="#1565c0", skin="#e0ac69", arms="up", mouth="open")}'
            f'<rect x="470" y="235" width="80" height="12" rx="4" fill="#ef5350"/><rect x="478" y="223" width="64" height="12" rx="4" fill="#42a5f5"/>')
    save("ch4_robot", frame(body, d))


def video_call():
    d = grad("bg", "#e1bee7", "#f3e5f5")
    granny = ('<g transform="translate(300,170)">'
              '<path d="M-60,80 Q-60,20 0,20 Q60,20 60,80 Z" fill="#00897b"/>'
              '<circle cx="0" cy="-10" r="34" fill="#e0ac69"/>'
              '<path d="M-34,-14 A34,34 0 0 1 34,-14 Q20,-34 0,-30 Q-20,-34 -34,-14 Z" fill="#eeeeee"/>'
              '<circle cx="0" cy="-46" r="12" fill="#eeeeee"/>'
              '<circle cx="-13" cy="-8" r="10" fill="none" stroke="#5d4037" stroke-width="3"/><circle cx="13" cy="-8" r="10" fill="none" stroke="#5d4037" stroke-width="3"/>'
              '<line x1="-3" y1="-8" x2="3" y2="-8" stroke="#5d4037" stroke-width="3"/>'
              '<circle cx="-13" cy="-8" r="3" fill="#212121"/><circle cx="13" cy="-8" r="3" fill="#212121"/>'
              '<path d="M-12,10 Q0,22 12,10" stroke="#6d4c41" stroke-width="3" fill="none"/>'
              '<circle cx="0" cy="2" r="2" fill="#d32f2f"/>'
              '<path d="M40,30 L66,-6" stroke="#e0ac69" stroke-width="10" stroke-linecap="round"/><circle cx="68" cy="-10" r="8" fill="#e0ac69"/></g>')
    tablet = ('<rect x="170" y="40" width="260" height="210" rx="20" fill="#263238"/>'
              '<rect x="184" y="54" width="232" height="182" rx="8" fill="#b3e5fc"/>'
              '<clipPath id="scr"><rect x="184" y="54" width="232" height="182" rx="8"/></clipPath>'
              f'<g clip-path="url(#scr)"><rect x="184" y="170" width="232" height="70" fill="#a5d6a7"/>{tree(390, 190, .5)}{granny}</g>'
              '<rect x="360" y="64" width="46" height="56" rx="6" fill="#fff" stroke="#90a4ae" stroke-width="2"/>'
              f'<g transform="translate(383,118) scale(.42)">{kid(0, 0, 1, top="#fdd835", bottom="#1565c0", skin="#e0ac69")}</g>'
              '<circle cx="300" cy="224" r="10" fill="#e53935"/><path d="M294,224 L306,224" stroke="#fff" stroke-width="3"/>')
    hearts = "".join(f'<path transform="translate({x},{y}) scale({s})" d="M0,6 C-12,-4 -8,-14 0,-8 C8,-14 12,-4 0,6 Z" fill="#ec407a"/>'
                     for x, y, s in [(460, 70, 1.6), (490, 110, 1.1), (130, 90, 1.3)])
    body = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>{hearts}{tablet}'
            f'{kid(100, 320, 1.25, top="#fdd835", bottom="#1565c0", skin="#e0ac69", arms="wave")}'
            f'{robot(520, 318, .8)}')
    save("ch4_videocall", frame(body, d))


def water_cycle():
    d = grad("sky", "#81d4fa", "#e1f5fe")
    sea = ('<path d="M0,250 Q300,240 360,270 L600,330 L0,330 Z" fill="#0288d1"/>'
           '<path d="M20,270 q15,-8 30,0 q15,8 30,0 M120,290 q15,-8 30,0 q15,8 30,0 M60,312 q15,-8 30,0 q15,8 30,0" stroke="#b3e5fc" stroke-width="3" fill="none"/>')
    mountains = ('<path d="M330,250 L430,90 L500,180 L540,130 L620,250 Z" fill="#8d6e63"/>'
                 '<path d="M412,118 L430,90 L450,118 L440,112 L430,122 L420,112 Z" fill="#fff"/>'
                 '<path d="M530,146 L540,130 L552,146 L546,142 L540,150 Z" fill="#fff"/>')
    land = '<path d="M330,250 L620,250 L600,330 L360,330 Q380,290 330,250 Z" fill="#9ccc65"/>'
    river = '<path d="M470,180 Q450,230 480,260 Q500,300 380,320 Q300,330 250,312" stroke="#4fc3f7" stroke-width="12" fill="none" stroke-linecap="round"/>'
    vapour = "".join(f'<path d="M{x},230 q-8,-14 0,-28 q8,-14 0,-28 q-8,-14 0,-28" stroke="#ffffff" stroke-width="4" fill="none" opacity=".9" stroke-dasharray="6 6"/>'
                     for x in [110, 150, 190])
    rain = "".join(f'<line x1="{x}" y1="{y}" x2="{x - 4}" y2="{y + 12}" stroke="#0277bd" stroke-width="3" stroke-linecap="round"/>'
                   for x in range(400, 500, 16) for y in (90, 115))
    body = (f'<rect width="{W}" height="{H}" fill="url(#sky)"/>{sun(70, 60, 28)}'
            f'{sea}{land}{mountains}{river}{vapour}'
            f'{cloud(260, 70, 1.3)}{cloud(450, 70, 1.4, "#90a4ae", "#607d8b")}{rain}'
            f'{arrow(230, 110, 360, 70, "#ff6f00")}'
            f'{drop_char(150, 150, .9)}{drop_char(250, 70, .6)}{drop_char(470, 140, .6, mood="open")}{drop_char(300, 300, .7)}'
            f'{badge(150, 240, 1)}{badge(250, 100, 2, "#7b1fa2")}{badge(520, 110, 3, "#00897b")}{badge(250, 280, 4, "#ef6c00")}')
    save("ch5_cycle", frame(body, d))


def drop_leaf():
    d = grad("bg", "#c8e6c9", "#f1f8e9")
    leaf = ('<g transform="translate(250,190) rotate(-15)">'
            '<path d="M-150,0 Q-40,-90 150,0 Q-40,90 -150,0 Z" fill="#43a047" stroke="#1b5e20" stroke-width="4"/>'
            '<path d="M-150,0 L150,0" stroke="#1b5e20" stroke-width="3"/>'
            + "".join(f'<path d="M{x},0 Q{x + 25},{-26 if i % 2 else 26} {x + 50},{-40 if i % 2 else 40}" stroke="#2e7d32" stroke-width="2" fill="none"/>'
                      for i, x in enumerate(range(-110, 90, 30)))
            + '</g>')
    garden = "".join(flower(x, 320, c, 1.3) for x, c in [(420, "#e91e63"), (460, "#ff9800"), (500, "#7e57c2"), (540, "#e91e63"), (575, "#ffeb3b")])
    body = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'{cloud(470, 50, 1.2, "#b0bec5", "#78909c")}'
            + "".join(f'<line x1="{x}" y1="80" x2="{x - 4}" y2="94" stroke="#0288d1" stroke-width="3" stroke-linecap="round"/>' for x in range(430, 520, 18))
            + f'{leaf}{drop_char(250, 150, 1.6)}{drop_char(150, 200, .6)}{drop_char(345, 168, .5)}'
            f'{grass_strip(300)}{garden}'
            f'{kid(470, 300, 1.2, girl=True, top="#ffa726", bottom="#00897b", skin="#c68642", arms="wave", mouth="open", flip=True)}')
    save("ch5_leaf", frame(body, d))


if __name__ == "__main__":
    cover()
    paper_tree()
    paper_process()
    rain_poem()
    tea_garden()
    kaziranga()
    litter_monster()
    clean_park()
    tree_poem()
    robot_room()
    video_call()
    water_cycle()
    drop_leaf()
