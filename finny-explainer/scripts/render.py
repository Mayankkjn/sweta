"""Finny explainer renderer: builds a 1920x1080 video from spec.py + VO lines."""
import sys, os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from spec import SECTIONS

SRC = sys.argv[1]; VO = sys.argv[2]; FONTS = sys.argv[3]; OUT = sys.argv[4]
PREVIEW = os.environ.get("PREVIEW")  # "t1,t2,..." -> write stills only
W, H, FPS = 1920, 1080, 30

# ---------------- brand ----------------
C = dict(
    ink=(14, 59, 46), green=(30, 107, 72), green2=(56, 151, 108), deep=(1, 54, 46),
    olive=(35, 48, 33), mint=(235, 245, 237), mint2=(220, 239, 226), paper=(245, 248, 245),
    gray=(90, 108, 100), gold=(214, 178, 106), amber=(222, 146, 52), coral=(224, 112, 96),
    white=(255, 255, 255),
)
def F(w, s): return ImageFont.truetype(f"{FONTS}/Poppins-{w}.ttf", s)
def SER(s, w=600): return ImageFont.truetype(f"{FONTS}/PlayfairItalic-{w}.ttf", s)

def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_back(x):
    x = min(max(x, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def clamp01(x): return min(max(x, 0.0), 1.0)

# ---------------- timeline ----------------
vo = json.load(open(f"{VO}/vo.json"))
vo_by = {(m["s"], m["l"]): m for m in vo}
LEAD, GAP, SGAP = 0.12, 0.42, 0.75
EXTRA = {"title": 0.9, "age2": 1.6, "rep3": 0.9, "end": 2.4, "rep0": 0.3}
lines = []  # dict(sec, li, start, dur, text, shots)
t = 0.0
for si, s in enumerate(SECTIONS):
    for li, (txt, shots) in enumerate(s["lines"]):
        m = vo_by[(si, li)]
        last = li == len(s["lines"]) - 1
        d = LEAD + m["dur"] + (SGAP if last else GAP)
        for sh in shots:
            if sh[0] == "custom": d += EXTRA.get(sh[1], 0)
        lines.append(dict(sec=si, li=li, start=t, dur=d, text=txt, shots=shots, audio=m["file"], adur=m["dur"]))
        t += d
TOTAL = t
print(f"total {TOTAL:.1f}s")

# shots with absolute timing
shots = []
for L in lines:
    nat = []
    for sh in L["shots"]:
        if sh[0] == "clip": nat.append((sh[2] - sh[1]) / (sh[3] if len(sh) > 3 else 1.0))
        elif sh[0] == "still": nat.append(1.6)
        else: nat.append(1.0 if sh[1] != "title" else 2.2)
    tot = sum(nat); st = L["start"]
    for sh, n in zip(L["shots"], nat):
        d = L["dur"] * n / tot
        shots.append(dict(kind=sh[0], arg=sh[1:], start=st, dur=d, nat=n, line=L))
        st += d
for sh in shots:
    if sh["kind"] == "clip":
        a, b = sh["arg"][0], sh["arg"][1]; sp = sh["arg"][2] if len(sh["arg"]) > 2 else 1.0
        # VO longer than footage -> play at speed then hold (extend); shorter -> speed up to fit
        sh["speed"] = sp * max(1.0, sh["nat"] / sh["dur"])
        print(f"  clip {a:6.1f}-{b:6.1f} nat {sh['nat']:4.1f}s slot {sh['dur']:4.1f}s speed {sh['speed']:.2f}")

# ---------------- source frames ----------------
SW = 430; SH = round(SW * 1562 / 720) // 2 * 2  # 932
BAR = round(92 / 1562 * SH)

def clean_status(img):
    a = np.asarray(img).copy()
    row = a[BAR + 3:BAR + 6].reshape(-1, 3)
    col = np.median(row, axis=0).astype(np.uint8)
    a[:BAR] = col
    im = Image.fromarray(a)
    lum = 0.299 * col[0] + 0.587 * col[1] + 0.114 * col[2]
    fg = (25, 35, 30) if lum > 140 else (240, 245, 240)
    d = ImageDraw.Draw(im)
    d.text((30, BAR // 2), "9:41", font=F(600, 15), fill=fg, anchor="lm")
    x = SW - 30
    d.rounded_rectangle((x - 24, BAR // 2 - 6, x, BAR // 2 + 6), 3, outline=fg, width=2)
    d.rectangle((x - 21, BAR // 2 - 3, x - 6, BAR // 2 + 3), fill=fg)
    for i in range(4):
        h = 4 + i * 3; d.rectangle((x - 60 + i * 6, BAR // 2 + 6 - h, x - 57 + i * 6, BAR // 2 + 6), fill=fg)
    return im

def decode(a, b):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC,
           "-vf", f"fps=30,scale={SW}:{SH}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (SW * SH * 3)
    arr = np.frombuffer(raw, np.uint8)[: n * SW * SH * 3].reshape(n, SH, SW, 3)
    return [clean_status(Image.fromarray(f)) for f in arr]

_cache = {}
def frames_for(sh):
    key = (sh["kind"],) + tuple(sh["arg"][:2])
    if key not in _cache:
        if sh["kind"] == "clip": _cache[key] = decode(sh["arg"][0], sh["arg"][1])
        else: _cache[key] = decode(sh["arg"][0], sh["arg"][0] + 0.1)[:1]
    return _cache[key]

def screen_at(sh, tl):
    fr = frames_for(sh)
    if sh["kind"] == "still": return fr[0]
    i = int(tl * sh["speed"] * 30)
    return fr[min(i, len(fr) - 1)]

# ---------------- static layers ----------------
def radial_bg(c_in, c_out, cx=0.62, cy=0.45):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - cx * W) / W) ** 2 + ((y - cy * H) / H) ** 2) / 0.75
    d = np.clip(d, 0, 1)[..., None]
    a = np.array(c_in) * (1 - d) + np.array(c_out) * d
    return Image.fromarray(a.astype(np.uint8))

def light_bg():
    im = radial_bg((250, 252, 250), (226, 240, 230)).convert("RGBA")
    blob = Image.new("RGBA", (W, H), (210, 236, 218, 0)); d = ImageDraw.Draw(blob)
    d.ellipse((1050, 80, 1650, 680), fill=(200, 234, 212, 110))
    d.ellipse((1250, 520, 1800, 1070), fill=(218, 240, 225, 130))
    d.ellipse((-200, 760, 380, 1340), fill=(205, 232, 214, 90))
    blob = blob.filter(ImageFilter.GaussianBlur(90))
    im.alpha_composite(blob)
    return im.convert("RGB")
BG = {"light": light_bg(), "dark": radial_bg((22, 82, 66), (1, 40, 34)), "olive": radial_bg((52, 74, 50), (24, 33, 23))}

def sparkle(d, x, y, r, col):
    pts = [(x, y - r), (x + r * .22, y - r * .22), (x + r, y), (x + r * .22, y + r * .22), (x, y + r), (x - r * .22, y + r * .22), (x - r, y), (x - r * .22, y - r * .22)]
    d.polygon(pts, fill=col)

for k in ("dark", "olive"):
    d = ImageDraw.Draw(BG[k])
    for (x, y, r) in [(140, 170, 9), (860, 120, 7), (1820, 260, 10), (1760, 930, 8), (980, 1010, 6), (760, 1020, 7)]:
        sparkle(d, x, y, r, C["gold"])

def phone_layer():
    pad = 60; bez = 13
    w, h = SW + 2 * bez, SH + 2 * bez
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (10, 40, 28, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad + 10, pad + 28, pad + w - 10, pad + h + 10), 62, fill=(10, 40, 28, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(26)); im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + w, pad + h), 60, fill=(18, 26, 22, 255))
    d.rounded_rectangle((pad + 2, pad + 2, pad + w - 2, pad + h - 2), 58, outline=(70, 84, 76, 255), width=2)
    return im, pad + bez
PHONE, SCR_OFF = phone_layer()
SMASK = Image.new("L", (SW, SH), 0); ImageDraw.Draw(SMASK).rounded_rectangle((0, 0, SW - 1, SH - 1), 46, fill=255)
PH_CX, PH_CY = 1350, 540
def phone_xy(cx=PH_CX, cy=PH_CY):
    return int(cx - PHONE.width / 2), int(cy - PHONE.height / 2)

def draw_phone(canvas, scr, cx=PH_CX, cy=PH_CY, alpha=1.0):
    x, y = phone_xy(cx, cy)
    layer = PHONE.copy()
    layer.paste(scr, (SCR_OFF, SCR_OFF), SMASK)
    # notch pill
    ImageDraw.Draw(layer).rounded_rectangle((layer.width / 2 - 52, SCR_OFF + 12, layer.width / 2 + 52, SCR_OFF + 40), 14, fill=(10, 12, 11, 255))
    if alpha < 1: layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(layer, (x, y))

# --- text helpers ---
def rich_line(text, size, col, acc, dark=False):
    """text with *italic serif* segments -> RGBA image"""
    parts = []; it = False
    for seg in text.split("*"):
        if seg: parts.append((seg, it))
        it = not it
    fs, fi = F(600, size), SER(int(size * 1.12), 600)
    widths = [ (fi if i else fs).getlength(s) for s, i in parts ]
    im = Image.new("RGBA", (int(sum(widths)) + 20, int(size * 1.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 0
    for (s, i), w in zip(parts, widths):
        d.text((x, size * 1.15), s, font=fi if i else fs, fill=acc if i else col, anchor="ls"); x += w
    return im

def wrap(text, font, maxw):
    words = text.split(); out = []; cur = ""
    for w_ in words:
        tst = (cur + " " + w_).strip()
        if font.getlength(tst) <= maxw: cur = tst
        else: out.append(cur); cur = w_
    if cur: out.append(cur)
    return out

def chip_img(text, dark=False):
    f = F(600, 22); w = int(f.getlength(text)) + 44
    im = Image.new("RGBA", (w, 46), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bg = (255, 255, 255, 30) if dark else (*C["mint2"], 255)
    d.rounded_rectangle((0, 0, w - 1, 45), 23, fill=bg, outline=((214, 178, 106, 200) if dark else (*C["green2"], 120)), width=1)
    d.text((22, 23), text, font=f, fill=(C["gold"] if dark else C["green"]), anchor="lm")
    return im

def wordmark(size, col):
    f = SER(size, 600); w = int(f.getlength("finny")) + 10
    im = Image.new("RGBA", (w, int(size * 1.4)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, size * 1.05), "finny", font=f, fill=col, anchor="ls")
    return im

SEC_LAYERS = {}
def section_layers(si):
    if si in SEC_LAYERS: return SEC_LAYERS[si]
    s = SECTIONS[si]; dark = s["theme"] == "dark"
    col = (255, 255, 255) if dark else C["ink"]; acc = C["gold"] if dark else C["green"]
    L = dict(chip=chip_img(s["chip"], dark) if s["chip"] else None,
             heads=[rich_line(h, 66, col, acc, dark) for h in s["head"]])
    SEC_LAYERS[si] = L; return L

STEP_IDS = ["start", "aa", "mf", "orbit", "assets", "cash", "check", "age", "report", "call"]

def draw_left(canvas, si, ts, line, tl, dark):
    """left panel: wordmark, chip, headline (animated), caption, progress"""
    L = section_layers(si); X = 130
    canvas.alpha_composite(wordmark(46, (255, 255, 255) if dark else C["green"]), (X, 70))
    y = 330
    items = ([L["chip"]] if L["chip"] else []) + L["heads"]
    for k, im in enumerate(items):
        p = ease_out((ts - 0.08 * k) / 0.55)
        if p <= 0: y += im.height + (18 if k == 0 else 0); continue
        lay = im.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * p)))
        canvas.alpha_composite(lay, (X, int(y + (1 - p) * 30)))
        y += im.height + (18 if k == 0 else 0)
    # caption (VO text)
    if line is not None:
        f = F(400, 27); p = ease_out(tl / 0.35)
        cap = Image.new("RGBA", (720, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(cap)
        cy = 0
        for ln in wrap(line["text"], f, 640):
            d.text((0, cy), ln, font=f, fill=((215, 230, 222) if dark else C["gray"])); cy += 42
        cap.putalpha(cap.getchannel("A").point(lambda v: int(v * p)))
        bar = Image.new("RGBA", (4, max(cy - 8, 30)), (*(C["gold"] if dark else C["green2"]), int(255 * p)))
        canvas.alpha_composite(bar, (X, y + 42)); canvas.alpha_composite(cap, (X + 26, y + 36))
    # progress
    sid = SECTIONS[si]["id"]
    if sid in STEP_IDS:
        cur = STEP_IDS.index(sid); d = ImageDraw.Draw(canvas)
        for i in range(len(STEP_IDS)):
            x0 = X + i * 50
            if i < cur: c = (*(C["green2"] if not dark else (150, 190, 160)), 255)
            elif i == cur: c = (*(C["green"] if not dark else C["gold"]), 255)
            else: c = (200, 220, 208, 255) if not dark else (78, 98, 76, 255)
            d.rounded_rectangle((x0, 975, x0 + 42, 981), 3, fill=c)
        d.text((X, 948), f"STEP {cur + 1} OF {len(STEP_IDS)}", font=F(600, 16), fill=(C["gold"] if dark else C["green"]))

# ---------------- custom scenes ----------------
def shadowed_card(w, h, r=30, fill=(255, 255, 255, 255), outline=None, sh_alpha=70):
    pad = 40
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (8, 40, 26, 0))
    s = Image.new("RGBA", im.size, (8, 40, 26, 0))
    ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 10), r, fill=(8, 40, 26, sh_alpha))
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad, pad + w, pad + h), r, fill=fill, outline=outline, width=3 if outline else 0)
    return im, pad

def age_card(label, dotc, age, corpus):
    w, h = 300, 400
    im, p = shadowed_card(w, h, 36, sh_alpha=140); d = ImageDraw.Draw(im); cx = p + w / 2
    d.text((cx, p + 52), "FIRE Age", font=F(500, 28), fill=(70, 80, 75), anchor="mm")
    d.text((cx, p + 130), str(age), font=F(700, 108), fill=C["ink"], anchor="mm")
    d.text((cx, p + 196), "years", font=F(500, 28), fill=C["ink"], anchor="mm")
    d.line((p + 70, p + 240, p + w - 70, p + 240), fill=(225, 230, 226), width=2)
    d.text((cx, p + 282), "Corpus", font=F(500, 26), fill=(70, 80, 75), anchor="mm")
    d.text((cx, p + 336), corpus, font=F(700, 42), fill=C["ink"], anchor="mm")
    lab = Image.new("RGBA", (im.width, 60), (0, 0, 0, 0)); ld = ImageDraw.Draw(lab)
    f = F(600, 24); tw = f.getlength(label) + 26; x0 = im.width / 2 - tw / 2
    ld.ellipse((x0, 22, x0 + 16, 38), fill=dotc); ld.text((x0 + 26, 30), label, font=f, fill=(255, 255, 255), anchor="lm")
    out = Image.new("RGBA", (im.width, im.height + 50), (0, 0, 0, 0)); out.alpha_composite(im); out.alpha_composite(lab, (0, im.height - 20))
    return out
AGE_CARDS = [age_card("YOUR PACE", C["coral"], 52, "₹ 18.1 Cr"), age_card("WITH FINNY", (110, 200, 130), 43, "₹ 5.8 Cr")]

def paste_scaled(canvas, im, cx, cy, s, alpha=1.0):
    if s <= 0.01 or alpha <= 0.01: return
    w, h = max(1, int(im.width * s)), max(1, int(im.height * s))
    lay = im if (w, h) == im.size else im.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")
    if alpha < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(lay, (int(cx - w / 2), int(cy - h / 2)))

AGE_STILL = None
def scene_age(canvas, which, tl, line):
    global AGE_STILL
    if AGE_STILL is None: AGE_STILL = decode(449.4, 449.5)[0]
    # phone holds the real FIRE-age screen, cards pop out of it
    phx = 1350
    draw_phone(canvas, AGE_STILL, phx, 540)
    x0, y0 = phone_xy(phx, 540); sc = SW / 720
    src = [(x0 + SCR_OFF + 207 * sc, y0 + SCR_OFF + 836 * sc), (x0 + SCR_OFF + 512 * sc, y0 + SCR_OFF + 836 * sc)]
    dst = [(1010, 520), (1690, 520)]
    s0 = 250 * sc / 300 * (380 / 450)
    pop1 = line["adur"] * 0.52 if which == "age1" else -10
    t1 = tl - pop1 if which == "age1" else 10
    t2 = tl - 0.15 if which == "age2" else -1
    for k, tt in ((0, t1), (1, t2)):
        if tt < 0: continue
        p = ease_back(tt / 0.7); q = ease_out(tt / 0.7)
        cx = src[k][0] + (dst[k][0] - src[k][0]) * q; cy = src[k][1] + (dst[k][1] - src[k][1]) * q
        paste_scaled(canvas, AGE_CARDS[k], cx, cy, s0 + (1.0 - s0) * p, clamp01(tt / 0.2))
    if which == "age2":
        tb = tl - line["adur"] * 0.62
        if tb > 0:
            p = ease_back(tb / 0.6)
            f = F(700, 34); txt = "9 years sooner"; w = int(f.getlength(txt)) + 90
            b = Image.new("RGBA", (w, 74), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
            d.rounded_rectangle((0, 0, w - 1, 73), 37, fill=(*C["gold"], 255))
            d.text((w / 2, 37), txt, font=f, fill=(40, 34, 18), anchor="mm")
            paste_scaled(canvas, b, 1350, 930, max(0.01, p), clamp01(tb / 0.2))

def ring(d, cx, cy, r, frac, col, bg=(226, 236, 229), wdt=16):
    d.arc((cx - r, cy - r, cx + r, cy + r), 0, 360, fill=bg, width=wdt)
    if frac > 0: d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * frac, fill=col, width=wdt)

def bar(d, x, y, w, frac, col, h=12):
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=(228, 236, 230))
    if frac > 0: d.rounded_rectangle((x, y, x + max(h, w * frac), y + h), h // 2, fill=col)

def pill(d, x, y, text, col, bgc):
    dot = text.startswith("●"); text = text.lstrip("● ")
    f = F(600, 19); w = f.getlength(text) + 30 + (18 if dot else 0)
    d.rounded_rectangle((x, y, x + w, y + 34), 17, fill=bgc)
    if dot: d.ellipse((x + 14, y + 12, x + 24, y + 22), fill=col)
    d.text((x + 15 + (18 if dot else 0), y + 17), text, font=f, fill=col, anchor="lm")

def score_card(prog):
    w, h = 900, 270
    im, p = shadowed_card(w, h, 30); d = ImageDraw.Draw(im)
    ring(d, p + 150, p + h / 2, 92, 0.8 * prog, C["green2"], wdt=18)
    d.text((p + 150, p + h / 2 - 8), "8", font=F(700, 76), fill=C["ink"], anchor="mm")
    d.text((p + 150, p + h / 2 + 44), "/ 10", font=F(500, 22), fill=C["gray"], anchor="mm")
    d.text((p + 290, p + 64), "Your FIRE ", font=F(600, 40), fill=C["ink"], anchor="ls")
    d.text((p + 290 + F(600, 40).getlength("Your FIRE "), p + 64), "Score", font=SER(46), fill=C["green"], anchor="ls")
    pill(d, p + 290, p + 92, "●  On Track", C["green"], C["mint2"])
    f = F(400, 25); yy = p + 160
    for ln in ["Strong FIRE trajectory — you're well", "positioned to reach financial independence."]:
        d.text((p + 290, yy), ln, font=f, fill=C["gray"]); yy += 38
    return im

def pillar_card(kind, prog, active):
    w, h = 286, 400
    im, p = shadowed_card(w, h, 26, outline=((*C["green2"], 255) if active else None)); d = ImageDraw.Draw(im); X = p + 26
    if kind == 0: title, sc, tag, tagc, tagbg = "Foundations", 6, "Needs attention", (176, 106, 22), (252, 236, 212)
    elif kind == 1: title, sc, tag, tagc, tagbg = "Investment", 9, "Strong", C["green"], C["mint2"]
    else: title, sc, tag, tagc, tagbg = "Risk &", 9, "Well diversified", C["green"], C["mint2"]
    sub = {0: None, 1: "Momentum", 2: "Resilience"}[kind]
    d.text((X, p + 52), title, font=F(600, 30), fill=C["ink"], anchor="ls")
    if sub: d.text((X, p + 90), sub, font=SER(32), fill=C["green"], anchor="ls")
    d.text((p + w - 26, p + 52), f"{sc}", font=F(700, 40), fill=C["ink"], anchor="rs")
    d.text((p + w - 26, p + 76), "/10", font=F(500, 18), fill=C["gray"], anchor="rs")
    pill(d, X, p + 112, tag, tagc, tagbg)
    y = p + 186; fl = F(500, 21); fv = F(700, 34)
    if kind == 0:
        d.text((X, y), "Savings rate", font=fl, fill=C["gray"]); d.text((X, y + 30), "8%", font=fv, fill=C["ink"])
        d.text((X + 72, y + 46), "of income", font=F(400, 19), fill=C["gray"])
        bar(d, X, y + 86, w - 52, 0.08 / 0.3 * prog, C["amber"])
        d.text((X, y + 118), "Corpus progress", font=fl, fill=C["gray"])
        d.text((X, y + 148), "₹2.25 Cr", font=F(700, 28), fill=C["ink"]); d.text((X + 132, y + 158), "of ₹3.61 Cr", font=F(400, 19), fill=C["gray"])
    elif kind == 1:
        d.text((X, y), "Assets beating inflation", font=fl, fill=C["gray"]); d.text((X, y + 30), f"{int(97 * prog)}%", font=F(700, 56), fill=C["ink"])
        bar(d, X, y + 108, w - 52, 0.97 * prog, C["green2"])
        d.text((X, y + 136), "Stocks · Equity MFs · NPS", font=F(400, 19), fill=C["gray"])
        d.text((X, y + 162), "SGBs · Gold", font=F(400, 19), fill=C["gray"])
    else:
        d.text((X, y), "Low-growth exposure", font=fl, fill=C["gray"]); d.text((X, y + 30), "3%", font=fv, fill=C["ink"])
        bar(d, X, y + 80, w - 52, 0.03 * prog + 0.001, C["green2"])
        d.text((X, y + 108), "Liquid assets", font=fl, fill=C["gray"]); d.text((X, y + 138), f"{int(94 * prog)}%", font=fv, fill=C["ink"])
        bar(d, X, y + 188, w - 52, 0.94 * prog, C["green2"])
    return im

def scene_report(canvas, which, tl, line):
    k = int(which[-1])
    rep_lines = [L for L in lines if SECTIONS[L["sec"]]["id"] == "report"]
    t0 = rep_lines[0]["start"]; now = line["start"] + tl; ts = now - t0
    p = ease_out(ts / 0.6)
    sc = score_card(clamp01(ts / 1.2))
    paste_scaled(canvas, sc, 1340, 290 + (1 - p) * 40, 1.0, p)
    for j in range(3):
        L = rep_lines[j + 1]
        tt = now - L["start"]
        if tt < 0: continue
        q = ease_back(tt / 0.55)
        im = pillar_card(j, clamp01(tt / 1.0), active=(k == j + 1) or (k == 3 and j == 2))
        paste_scaled(canvas, im, 1340 + (j - 1) * 312, 720, 0.85 + 0.15 * q, clamp01(tt / 0.25))

def center_text(canvas, y, text, font, col, alpha=1.0):
    lay = Image.new("RGBA", (W, int(font.size * 1.6)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((W / 2, font.size * 0.8), text, font=font, fill=col, anchor="mm")
    if alpha < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(lay, (0, int(y - font.size * 0.8)))

def scene_title(canvas, tl):
    p = ease_out(tl / 0.8)
    wm = wordmark(190, (255, 255, 255))
    paste_scaled(canvas, wm, W / 2, 470 + (1 - p) * 30, 1.0, p)
    q = ease_out((tl - 0.45) / 0.7)
    center_text(canvas, 640, "Your path to financial independence", F(500, 36), (205, 228, 214), q)
    center_text(canvas, 700, "FIRE  ·  Financial Independence, Retire Early", F(500, 22), C["gold"], q)

def node(canvas, cx, cy, num, t1, t2, prog):
    if prog <= 0: return
    im, p = shadowed_card(440, 300, 28, fill=(255, 255, 255, 18), outline=(214, 178, 106, 160), sh_alpha=0)
    d = ImageDraw.Draw(im)
    d.ellipse((p + 30, p + 34, p + 96, p + 100), fill=C["gold"]); d.text((p + 63, p + 67), str(num), font=F(700, 32), fill=(40, 34, 18), anchor="mm")
    d.text((p + 30, p + 166), t1, font=F(600, 38), fill=(255, 255, 255), anchor="ls")
    d.text((p + 30, p + 224), t2, font=SER(38), fill=C["gold"], anchor="ls")
    paste_scaled(canvas, im, cx, cy + (1 - ease_out(prog)) * 40, 1.0, clamp01(prog * 1.5))

def scene_outro(canvas, which, tl, line):
    if which == "out1":
        p1 = ease_out(tl / 0.6); p2 = ease_out((tl - 0.9) / 0.6)
        center_text(canvas, 300, "From a free review…", F(500, 34), (205, 228, 214), p1)
        for k, (txt, x) in enumerate((("Free portfolio review", 640), ("Paid advisory client", 1280))):
            pp = p1 if k == 0 else p2
            if pp <= 0: continue
            f = F(600, 40); w = int(f.getlength(txt)) + 90
            b = Image.new("RGBA", (w, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
            d.rounded_rectangle((0, 0, w - 1, 99), 50, fill=((255, 255, 255, 30) if k == 0 else (*C["gold"], 255)),
                                outline=(214, 178, 106, 200), width=2)
            d.text((w / 2, 50), txt, font=f, fill=((255, 255, 255) if k == 0 else (40, 34, 18)), anchor="mm")
            paste_scaled(canvas, b, x, 520, 0.9 + 0.1 * ease_back(pp), pp)
        if p2 > 0:
            d = ImageDraw.Draw(canvas); x0, x1 = 905, 905 + (1010 - 905) * p2
            d.line((x0, 520, x1, 520), fill=C["gold"], width=4)
            if p2 > 0.9: d.polygon([(1010, 508), (1030, 520), (1010, 532)], fill=C["gold"])
    elif which == "out2":
        center_text(canvas, 250, "How Finny gets you there", F(500, 34), (205, 228, 214), ease_out(tl / 0.5))
        A = line["adur"]
        for k, (t1, t2, at) in enumerate((("Financial models", "create the plan", 0.0), ("Expert advisors", "walk you through it", 0.36 * A), ("AI agents", "execute it", 0.72 * A))):
            node(canvas, 470 + k * 490, 560, k + 1, t1, t2, (tl - at) / 0.6)
    else:
        p = ease_out(tl / 0.8)
        paste_scaled(canvas, wordmark(170, (255, 255, 255)), W / 2, 400 + (1 - p) * 30, 1.0, p)
        q = ease_out((tl - 0.5) / 0.8)
        hl = rich_line("Your one-stop shop for *financial independence*", 52, (255, 255, 255), C["gold"])
        paste_scaled(canvas, hl, W / 2 + 10, 585, 1.0, q)
        r = ease_out((tl - 1.4) / 0.8)
        center_text(canvas, 720, "SEBI Registered  ·  100% safe  ·  0% commissions", F(500, 24), (190, 214, 200), r)
        center_text(canvas, 800, "Know your FIRE age in 3 minutes", F(600, 28), C["gold"], r)

# ---------------- frame render ----------------
def theme_of(sh):
    sid = SECTIONS[sh["line"]["sec"]]["id"]
    if sh["kind"] == "custom" and sh["arg"][0] in ("title", "out1", "out2", "end"): return "dark"
    if sid == "age": return "olive"
    return SECTIONS[sh["line"]["sec"]]["theme"]

sec_start = {}
for L in lines: sec_start.setdefault(L["sec"], L["start"])

def render(tt):
    i = max(j for j, s in enumerate(shots) if s["start"] <= tt + 1e-9)
    sh = shots[i]; tl = tt - sh["start"]; line = sh["line"]; ltl = tt - line["start"]
    th = theme_of(sh); dark = th != "light"
    canvas = BG[th].copy().convert("RGBA")
    kind = sh["kind"]; name = sh["arg"][0] if kind == "custom" else None
    si = line["sec"]
    if name == "title": scene_title(canvas, tl)
    elif name in ("out1", "out2", "end"): scene_outro(canvas, name, tl, line)
    else:
        draw_left(canvas, si, tt - sec_start[si], line, ltl, dark)
        if name in ("age1", "age2"): scene_age(canvas, name, ltl, line)
        elif name and name.startswith("rep"): scene_report(canvas, name, ltl, line)
        else:
            # phone entrance on first phone shot of intro
            first_phone = next(s for s in shots if s["kind"] != "custom")
            yoff = (1 - ease_out((tt - first_phone["start"]) / 0.7)) * 120 if sh is first_phone or tt - first_phone["start"] < 0.7 else 0
            scr = screen_at(sh, tl)
            # quick screen crossfade from previous phone shot
            if i > 0 and shots[i - 1]["kind"] != "custom" and tl < 0.2:
                prev = screen_at(shots[i - 1], shots[i - 1]["dur"])
                scr = Image.blend(prev, scr, tl / 0.2)
            draw_phone(canvas, scr, PH_CX, PH_CY + yoff)
    return canvas.convert("RGB"), i

def main():
    if PREVIEW == "mid":
        ims = [render(s["start"] + 0.75 * s["dur"])[0].resize((480, 270), Image.LANCZOS) for s in shots]
        for k in range(0, len(ims), 16):
            sheet = Image.new("RGB", (1920, 1080), (0, 0, 0))
            for j, im in enumerate(ims[k:k + 16]): sheet.paste(im, ((j % 4) * 480, (j // 4) * 270))
            sheet.save(f"{OUT}_sheet{k // 16}.png")
        return
    if PREVIEW:
        for x in PREVIEW.split(","):
            im, _ = render(float(x)); im.save(f"{OUT}_{float(x):06.2f}.png")
        return
    # audio track
    alist = OUT + ".audio.txt"
    filt = []; ins = []
    for k, L in enumerate(lines):
        ins += ["-i", L["audio"]]
        filt.append(f"[{k}:a]aresample=48000,adelay={int((L['start'] + LEAD) * 1000)}|{int((L['start'] + LEAD) * 1000)}[a{k}]")
    mix = "".join(f"[a{k}]" for k in range(len(lines)))
    filt.append(f"{mix}amix=inputs={len(lines)}:normalize=0,apad,atrim=0:{TOTAL:.3f},loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "48000", "-ac", "2", OUT + ".vo.wav"], check=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", OUT + ".vo.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT], stdin=subprocess.PIPE)
    n = int(round(TOTAL * FPS)); prev_full = None; prev_i = -1; fade_from = None; fade_t0 = 0
    for f in range(n):
        tt = f / FPS
        im, i = render(tt)
        if i != prev_i and prev_full is not None:
            a, b = shots[prev_i], shots[i]
            if theme_of(a) != theme_of(b) or a["kind"] == "custom" or b["kind"] == "custom" or a["line"]["sec"] != b["line"]["sec"]:
                if not (a["kind"] == "custom" and b["kind"] == "custom" and a["line"]["sec"] == b["line"]["sec"]):
                    fade_from = prev_full; fade_t0 = tt
        if fade_from is not None:
            x = (tt - fade_t0) / 0.35
            if x >= 1: fade_from = None
            else: im = Image.blend(fade_from, im, ease_out(x))
        if fade_from is None: prev_full = im
        prev_i = i
        enc.stdin.write(im.tobytes())
        if f % 300 == 0: print(f"frame {f}/{n}", flush=True)
    enc.stdin.close(); enc.wait()

main()
