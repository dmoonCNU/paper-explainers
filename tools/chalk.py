# -*- coding: utf-8 -*-
"""Chalkboard-style explainer video renderer (Pillow + ffmpeg)."""
import math, os, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(ROOT, 'levy', 'audio'); FIG = os.path.join(ROOT, 'levy', 'figs')
W, H, FPS = 1920, 1080, 25
SR = 22050; SPF = SR // FPS          # 882 audio samples per frame
PAD = 1.4                            # seconds of silence after each narration
FONT_MAIN = r'C:\Windows\Fonts\Inkfree.ttf'
FONT_FALL = r'C:\Windows\Fonts\segoepr.ttf'

WHITE = (242, 240, 228); YEL = (250, 218, 110); PINK = (250, 150, 165)
BLUE = (140, 205, 250); GRN = (160, 232, 170); ORG = (250, 175, 110)

rnd = random.Random(42)
_fc = {}
def font(path, size):
    k = (path, int(size))
    if k not in _fc: _fc[k] = ImageFont.truetype(path, int(size))
    return _fc[k]
_missing = bytes(font(FONT_MAIN, 40).getmask('\uFFFE'))
_has = {}
def has_glyph(ch):
    if ch not in _has:
        _has[ch] = ord(ch) < 127 or (not 0x370 <= ord(ch) <= 0x3FF) and bytes(font(FONT_MAIN, 40).getmask(ch)) != _missing
    return _has[ch]

# ------------------------------------------------------------------ board
def make_board():
    rs = np.random.RandomState(3)
    low = rs.rand(9, 16).astype(np.float32)
    cloud = np.asarray(Image.fromarray((low * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255
    fine = rs.rand(H, W).astype(np.float32)
    base = np.array([30, 62, 50], dtype=np.float32)
    img = base[None, None, :] * (0.86 + 0.28 * cloud[..., None]) + (fine[..., None] - 0.5) * 7
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    # faint eraser smudges
    sm = Image.new('L', (W, H), 0); d = ImageDraw.Draw(sm)
    for _ in range(26):
        x, y = rs.randint(60, W - 60), rs.randint(60, H - 60)
        dx, dy = rs.randint(-420, 420), rs.randint(-60, 60)
        d.line([x, y, x + dx, y + dy], fill=int(rs.randint(14, 34)), width=int(rs.randint(40, 110)))
    sm = sm.filter(ImageFilter.GaussianBlur(38))
    im = Image.composite(Image.new('RGB', (W, H), (205, 215, 205)), im, sm)
    # wooden frame
    d = ImageDraw.Draw(im); f = 22
    for i in range(f):
        c = (112 - i, 74 - i // 2, 40)
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=c)
    d.rectangle([f, f, W - 1 - f, H - 1 - f], outline=(20, 36, 30), width=3)
    return im

def make_grain():
    rs = np.random.RandomState(9)
    g = 150 + rs.rand(H, W) * 105
    speck = rs.rand(H, W) < 0.07
    g[speck] *= 0.45
    im = Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
    return im

# ------------------------------------------------------------------ text layout
def parse(text):
    """-> list of (char, level); ^{..} raises level, _{..} lowers it."""
    out = []; stack = [0]; i = 0
    while i < len(text):
        c = text[i]
        if c in '^_' and i + 1 < len(text) and text[i + 1] == '{':
            stack.append(stack[-1] + (1 if c == '^' else -1) if (stack[-1] >= 0 or c == '_') else 1); i += 2; continue
        if c == '}' and len(stack) > 1:
            stack.pop(); i += 1; continue
        out.append((c, stack[-1])); i += 1
    return out

def lvl_style(size, lvl):
    if lvl == 0: return size, 0
    if lvl == 1: return size * 0.62, -size * 0.36
    if lvl >= 2: return size * 0.48, -size * 0.66
    return size * 0.62, size * 0.22

class Line:
    """One rendered line of chalk text: mask + cumulative x advances."""
    def __init__(self, text, size):
        runs = parse(text); x = 0.0; items = []
        for ch, lvl in runs:
            s, dy = lvl_style(size, lvl)
            f = font(FONT_MAIN if has_glyph(ch) else FONT_FALL, s * (1.0 if has_glyph(ch) else 0.86))
            adv = f.getlength(ch)
            items.append((ch, f, x, dy)); x += adv
        self.w = int(x) + 8; self.h = int(size * 1.9); self.base = int(size * 1.25)
        m = Image.new('L', (self.w + 8, self.h), 0); d = ImageDraw.Draw(m)
        for ch, f, cx, dy in items:
            d.text((cx + 4, self.base + dy), ch, font=f, fill=255, anchor='ls')
        self.mask = m.filter(ImageFilter.MaxFilter(3))
        self.cmask = self.mask.filter(ImageFilter.MaxFilter(5))
        self.adv = [it[2] for it in items] + [x]
        self.n = len(items)

# ------------------------------------------------------------------ elements
class El:
    kind = ''
    def __init__(self, t, dur): self.t = t; self.dur = max(dur, 0.04); self.done = False; self.tip = None
    def prog(self, now): return min(1.0, max(0.0, (now - self.t) / self.dur))

class Text(El):
    def __init__(self, t, text, x, y, size=54, color=WHITE, mw=None, cps=24, center=False):
        lines = text.split('\n'); sz = size
        while True:
            self.lines = [Line(l, sz) for l in lines]
            if mw is None or max(l.w for l in self.lines) <= mw or sz < 26: break
            sz *= 0.95
        self.size = sz; self.color = color
        nchar = sum(l.n for l in self.lines)
        super().__init__(t, nchar / cps)
        self.pos = []
        for i, l in enumerate(self.lines):
            lx = x - l.w / 2 if center else x
            self.pos.append((int(lx), int(y + i * sz * 1.28)))
        self.nchar = max(nchar, 1); self.drawn = [0] * len(self.lines)
        self.width = max(l.w for l in self.lines); self.height = int(len(lines) * sz * 1.28)
    def draw(self, st, now):
        p = self.prog(now) * self.nchar; acc = 0
        for i, l in enumerate(self.lines):
            k = min(max(p - acc, 0), l.n); acc += l.n
            ki = int(k); xr = l.adv[ki] + (l.adv[min(ki + 1, l.n)] - l.adv[ki]) * (k - ki) if l.n else 0
            xr = int(xr) + (12 if k >= l.n else 4)
            x0 = self.drawn[i]
            if xr > x0:
                px, py = self.pos[i]
                box = (x0, 0, min(xr, l.mask.width), l.h)
                st.col.paste(self.color, (px + x0, py), l.cmask.crop(box))
                reg = (px + x0, py, px + box[2], py + l.h)
                st.alpha.paste(ImageChops.lighter(st.alpha.crop(reg), l.mask.crop(box)), reg[:2])
                self.drawn[i] = box[2]
            if 0 < k < l.n:
                self.tip = (self.pos[i][0] + xr, self.pos[i][1] + l.base - self.size * 0.3 + 9 * math.sin(now * 31))
        if self.prog(now) >= 1: self.done = True; self.tip = None

def wobble(pts, amp=1.6, step=14):
    """Resample a polyline and add a little hand tremor."""
    out = []
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / step))
        nx, ny = (-(y2 - y1) / L, (x2 - x1) / L) if L > 0 else (0, 0)
        for j in range(n):
            f = j / n; o = rnd.uniform(-amp, amp) if 0 < j else 0
            out.append((x1 + (x2 - x1) * f + nx * o, y1 + (y2 - y1) * f + ny * o))
    out.append(pts[-1]); return out

class Path(El):
    def __init__(self, t, pts, color=WHITE, w=6, dur=0.6, dash=False, amp=1.6, raw=False):
        super().__init__(t, dur)
        self.pts = pts if raw else wobble(pts, amp); self.color = color; self.w = w; self.dash = dash; self.i = 0
    def draw(self, st, now):
        n = len(self.pts) - 1; k = int(self.prog(now) * n)
        while self.i < k:
            a, b = self.pts[self.i], self.pts[self.i + 1]
            if not (self.dash and (self.i // 2) % 2):
                for im, col, ww in ((st.dcol, self.color, self.w + 6), (st.dalpha, 255, self.w)):
                    im.line([a, b], fill=col, width=ww); r = ww / 2
                    im.ellipse([b[0] - r, b[1] - r, b[0] + r, b[1] + r], fill=col)
            self.i += 1
        self.tip = self.pts[self.i] if self.i < n else None
        if self.prog(now) >= 1: self.done = True; self.tip = None

class Dots(El):
    def __init__(self, t, pts, color, r=8, dur=0.5):
        super().__init__(t, dur); self.pts = pts; self.color = color; self.r = r; self.i = 0
    def draw(self, st, now):
        k = int(self.prog(now) * len(self.pts))
        while self.i < k:
            x, y = self.pts[self.i]; r = self.r
            st.dcol.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=self.color)
            st.dalpha.ellipse([x - r, y - r, x + r, y + r], fill=255); self.i += 1
        if self.prog(now) >= 1: self.done = True

class Paper(El):
    """A printed figure taped to the board."""
    def __init__(self, t, name, x, y, w, h, rot=0.0):
        super().__init__(t, 0.6)
        im = Image.open(os.path.join(FIG, name + '.png')).convert('RGB')
        s = min((w - 36) / im.width, (h - 36) / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        pw, ph = im.width + 36, im.height + 36
        sheet = Image.new('RGBA', (pw + 40, ph + 60), (0, 0, 0, 0))
        sh = Image.new('L', sheet.size, 0); ImageDraw.Draw(sh).rectangle([26, 46, 26 + pw, 46 + ph], fill=130)
        sheet.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(9)))
        sheet.paste((250, 249, 244), (20, 36, 20 + pw, 36 + ph)); sheet.paste(im, (38, 54))
        tp = Image.new('RGBA', sheet.size, (0, 0, 0, 0)); d = ImageDraw.Draw(tp)
        for cx in (20 + pw * 0.2, 20 + pw * 0.8):
            d.polygon([(cx - 48, 20), (cx + 48, 26), (cx + 46, 54), (cx - 50, 48)], fill=(238, 226, 170, 205))
        sheet = Image.alpha_composite(sheet, tp).rotate(rot, resample=Image.BICUBIC, expand=True)
        self.sheet = sheet; self.xy = (int(x + (w - sheet.width) / 2), int(y + (h - sheet.height) / 2))
    def draw(self, st, now):
        p = self.prog(now)
        if p >= 1:
            st.base.paste(self.sheet, self.xy, self.sheet); self.done = True; st.fading = None
        elif p > 0:
            st.fading = (self, p)

# ------------------------------------------------------------------ helpers to build scenes
def line(t, x1, y1, x2, y2, color=WHITE, w=6, dur=0.5, dash=False):
    return Path(t, [(x1, y1), (x2, y2)], color, w, dur, dash)
def arrow(t, x1, y1, x2, y2, color=WHITE, w=6, dur=0.5, head=22):
    a = math.atan2(y2 - y1, x2 - x1)
    h1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
    h2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
    return [Path(t, [(x1, y1), (x2, y2)], color, w, dur), Path(t + dur, [h1, (x2, y2), h2], color, w, 0.15, amp=0)]
def ellipse(t, cx, cy, rx, ry, color=WHITE, w=6, dur=0.7, a0=-1.9, turns=1.04, dash=False):
    n = max(24, int((rx + ry) * 0.5)); j = rnd.uniform(0.985, 1.015)
    pts = [(cx + rx * j * math.cos(a0 + turns * 2 * math.pi * i / n), cy + ry * math.sin(a0 + turns * 2 * math.pi * i / n)) for i in range(n + 1)]
    return Path(t, pts, color, w, dur, dash, raw=True)
def rect(t, x, y, w_, h_, color=WHITE, w=5, dur=0.8):
    return Path(t, [(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_), (x, y - 3)], color, w, dur, amp=2.2)
def curve(t, fn, x0, x1, n, color, w=7, dur=1.2):
    return Path(t, [fn(x0 + (x1 - x0) * i / n) for i in range(n + 1)], color, w, dur, raw=True)
def check(t, x, y, color=GRN, s=1.0):
    return Path(t, [(x, y), (x + 16 * s, y + 20 * s), (x + 48 * s, y - 26 * s)], color, 7, 0.3, amp=0.5)
def title(t, text, color=YEL):
    T = Text(t, text, 70, 30, 78, color, mw=1780, cps=30)
    return [T, line(t + T.dur, 70, 150, 70 + T.width + 10, 153, color, 5, 0.4)]
def scribble(t, cx, cy, r, color, dur=0.8, w=6):
    """Fill a disc with a chalk scribble."""
    pts = []; n = int(r / 5)
    for i in range(-n, n + 1):
        y = cy + i * 5; hw = math.sqrt(max(r * r - (i * 5) ** 2, 0))
        pts += [(cx - hw, y), (cx + hw, y)] if i % 2 == 0 else [(cx + hw, y), (cx - hw, y)]
    return Path(t, pts, color, w, dur, raw=True)

def flat(xs):
    out = []
    for x in xs:
        out += flat(x) if isinstance(x, list) else [x]
    return out

# ------------------------------------------------------------------ scenes
def scenes(D):
    S = []
    # ---------------- 1 title
    d = D[0]; e = []
    e += [Text(0.4, 'Taking a picture of the', 960, 170, 84, WHITE, center=True, cps=22)]
    e += [Text(2.6, 'Quark-Gluon Plasma', 960, 300, 150, YEL, center=True, cps=14)]
    e += [line(4.3, 420, 520, 1500, 526, YEL, 6, 0.6)]
    e += [Text(0.38 * d, 'Bose-Einstein correlations  &  Lévy sources', 960, 590, 66, WHITE, center=True, cps=26)]
    e += [Text(0.55 * d, 'PbPb collisions at 5.02 TeV   |   CMS experiment, LHC', 960, 720, 54, BLUE, center=True, cps=28)]
    e += [Text(0.80 * d, 'based on  Phys. Rev. C 109, 024914 (2024)', 960, 900, 40, WHITE, center=True, cps=32)]
    S.append(e)

    # ---------------- 2 collision
    d = D[1]; e = title(0.3, '1.  A droplet of quark-gluon plasma')
    e += [ellipse(2.0, 190, 400, 42, 110, BLUE), Text(2.6, 'Pb', 160, 520, 50, BLUE)]
    e += arrow(3.0, 250, 400, 350, 400)
    e += [ellipse(3.6, 560, 400, 42, 110, BLUE), Text(4.2, 'Pb', 530, 520, 50, BLUE)]
    e += arrow(4.4, 500, 400, 400, 400)
    e += arrow(0.15 * d, 650, 400, 770, 400, YEL)
    t = 0.17 * d
    e += [ellipse(t, 950, 400, 130, 130, ORG, 7, 0.8), scribble(t + 0.8, 950, 400, 78, YEL, 1.0), Text(t + 1.6, 'quark-gluon plasma', 780, 540, 46, ORG)]
    e += [Text(0.30 * d, 'T > 10^{12} K', 830, 615, 54, PINK)]
    t = 0.47 * d
    e += arrow(t, 1120, 400, 1240, 400, YEL)
    rr = random.Random(5); pts = []
    for i in range(22):
        a = i * 2 * math.pi / 22 + rr.uniform(-0.1, 0.1); r = rr.uniform(95, 190)
        p = (1500 + r * math.cos(a), 400 + r * 0.85 * math.sin(a)); pts.append(p)
        e += [Path(t + 0.7 + i * 0.07, [(1500 + 26 * math.cos(a), 400 + 26 * math.sin(a)), p], WHITE, 3, 0.12)]
    e += [Dots(t + 0.9, pts[0::3], GRN, 9, 1.5), Dots(t + 0.95, pts[1::3], YEL, 9, 1.5), Dots(t + 1.0, pts[2::3], PINK, 9, 1.5)]
    e += [Text(0.55 * d, 'thousands of particles\n(mostly pions)', 1320, 590, 46, WHITE)]
    e += [Text(0.66 * d, 'size  ≈  10 fm', 110, 720, 62, GRN), Text(0.66 * d + 1.2, '(1 fm = 10^{-15} m)', 560, 730, 46, WHITE)]
    e += [Text(0.74 * d, 'lifetime  ≈  10^{-23} s', 110, 815, 62, GRN)]
    T = Text(0.88 * d, 'How do we measure its size and shape?', 960, 920, 70, YEL, center=True, cps=22)
    e += [T, rect(0.88 * d + T.dur, 960 - T.width / 2 - 30, 925, T.width + 60, 120, YEL, 5, 0.8)]
    S.append(e)

    # ---------------- 3 HBT
    d = D[2]; e = title(0.3, '2.  Bose-Einstein correlations')
    ox, oy, pw, ph = 150, 900, 720, 600; base = oy - 220; amp = 330
    e += [Text(0.02 * d, 'pions are bosons', 1010, 190, 56, WHITE)]
    e += [Text(0.07 * d, 'identical bosons like the same state', 1010, 270, 50, WHITE, mw=850)]
    e += [Text(0.15 * d, '-> pairs with nearly equal momentum', 1010, 350, 50, GRN, mw=850),
          Text(0.19 * d, '    show up more often', 1010, 420, 50, GRN, mw=850)]
    t = 0.25 * d
    e += [Text(t, 'C(q) =', 1010, 560, 60, YEL), Text(t + 0.8, 'pairs, same collision', 1240, 520, 46, WHITE),
          line(t + 2.2, 1230, 605, 1790, 608, WHITE, 5, 0.4), Text(t + 2.7, 'pairs, different collisions', 1240, 615, 46, WHITE)]
    t = 0.37 * d
    e += arrow(t, ox, oy, ox + pw + 30, oy) + arrow(t + 0.6, ox, oy, ox, oy - ph - 20)
    e += [Text(t + 1.2, 'q', ox + pw + 10, oy - 5, 54, WHITE), Text(t + 1.4, 'C(q)', ox + 20, oy - ph - 70, 54, WHITE),
          line(t + 1.8, ox, base, ox + pw, base, WHITE, 3, 0.5, dash=True), Text(t + 2.3, '1', ox - 50, base - 60, 48, WHITE),
          line(t + 2.5, ox - 12, base - amp, ox + 12, base - amp, WHITE, 5, 0.1), Text(t + 2.6, '2', ox - 50, base - amp - 60, 48, WHITE)]
    f1 = lambda q: (ox + q * pw, base - amp * math.exp(-(q * 9) ** 1.7))
    f2 = lambda q: (ox + q * pw, base - amp * math.exp(-(q * 3.0) ** 1.7))
    e += [curve(0.44 * d, f1, 0, 1, 90, GRN, 8, 1.6), Text(0.44 * d + 1.6, 'bump at small q', 330, 380, 46, WHITE)]
    t = 0.53 * d
    T = Text(t, 'bump width  ~  1 / (source size)', 1010, 740, 56, YEL, mw=840)
    e += [T, rect(t + T.dur, 990, 745, T.width + 40, 110, YEL, 5, 0.7)]
    e += [Text(0.61 * d, 'narrow bump = LARGE source', 230, 700, 46, GRN)]
    e += [curve(0.66 * d, f2, 0, 1, 90, PINK, 8, 1.6), Text(0.66 * d + 1.5, 'wide bump = SMALL source', 230, 770, 46, PINK)]
    e += [Text(0.76 * d, 'same trick measured the size of stars', 1010, 890, 44, BLUE, mw=850),
          Text(0.82 * d, '(Hanbury Brown & Twiss)', 1010, 945, 44, BLUE, mw=850),
          Text(0.92 * d, 'here:  "femtoscopy"', 150, 950, 60, YEL)]
    S.append(e)

    # ---------------- 4 shape
    d = D[3]; e = title(0.3, '3.  Not only how big...  what shape?')
    ox, oy, pw, ph = 150, 930, 760, 640
    e += arrow(1.5, ox, oy, ox + pw + 30, oy) + arrow(2.1, ox, oy, ox, oy - ph - 20)
    e += [Text(2.8, 'distance r', ox + pw - 190, oy + 5, 46, WHITE), Text(3.4, 'source density', ox + 20, oy - ph - 60, 46, WHITE)]
    g = lambda r: (ox + r / 6 * pw, oy - 560 * math.exp(-r * r / 2.0))
    c = lambda r: (ox + r / 6 * pw, oy - 560 / (1 + r * r / 0.55))
    e += [curve(0.13 * d, g, 0, 6, 100, WHITE, 8, 1.8), Text(0.13 * d + 1.8, 'Gaussian (bell curve)', 440, 420, 48, WHITE)]
    e += [Text(0.25 * d, 'Lévy stable distributions', 1010, 190, 60, YEL), Text(0.31 * d, 'shape parameter  α', 1010, 275, 56, WHITE)]
    e += [Text(0.37 * d, 'α = 2 :  Gaussian', 1010, 370, 56, WHITE), Text(0.37 * d + 0.4, 'α = 2', 480, 480, 52, WHITE)]
    e += [Text(0.44 * d, 'α = 1 :  Cauchy', 1010, 450, 56, PINK), curve(0.46 * d, c, 0, 6, 100, PINK, 8, 1.8),
          Text(0.46 * d + 1.8, 'α = 1', 400, 680, 52, PINK), Text(0.50 * d, 'long tail!', 640, 760, 52, PINK)]
    e += arrow(0.50 * d + 1.0, 730, 830, 760, 895, PINK, 5, 0.3)
    def walk(cx, cy, seed, jump):
        r = random.Random(seed); x, y = cx, cy; pts = [(x, y)]
        for i in range(1, 90):
            a = r.uniform(0, 6.283); st = 11
            if jump and i % 15 == 8: st = r.uniform(110, 160)
            x = max(cx - 190, min(cx + 190, x + st * math.cos(a))); y = max(cy - 110, min(cy + 110, y + st * math.sin(a)))
            pts.append((x, y))
        return pts
    t = 0.60 * d
    e += [Text(t, 'gas thins out -> longer free paths', 1010, 560, 46, BLUE, mw=850)]
    e += [Path(0.66 * d, walk(1200, 760, 3, False), WHITE, 4, 2.5, raw=True), Text(0.66 * d + 1.0, 'small steps', 1090, 880, 42, WHITE)]
    e += [Path(0.78 * d, walk(1640, 760, 11, True), PINK, 4, 3.0, raw=True), Text(0.78 * d + 1.5, 'a few long steps', 1490, 880, 42, PINK)]
    T = Text(0.91 * d, '"anomalous diffusion"', 1190, 960, 56, YEL)
    e += [T, line(0.91 * d + T.dur, 1190, 1045, 1190 + T.width, 1048, YEL, 5, 0.4)]
    S.append(e)

    # ---------------- 5 formula
    d = D[4]; e = title(0.3, '4.  One formula, three numbers')
    T = Text(0.04 * d, 'C(q)  =  1  +  λ · e^{-(qR)^{α}}', 960, 200, 130, WHITE, center=True, cps=9)
    e += [T, rect(0.04 * d + T.dur + 0.2, 960 - T.width / 2 - 40, 215, T.width + 80, 210, YEL, 6, 1.0)]
    cols = [(GRN, 'R', 'size', 0.24), (YEL, 'α', 'shape', 0.42), (PINK, 'λ', 'strength', 0.62)]
    for i, (colr, sym, nm, f) in enumerate(cols):
        x = 130 + i * 600; t = f * d
        e += [Text(t, sym, x, 470, 120, colr, cps=4), Text(t + 0.4, '=  ' + nm, x + 120, 510, 66, colr)]
    x = 130; t = 0.28 * d
    e += [Text(t, 'Lévy scale:\nhow big the source is', x, 680, 44, WHITE)]
    e += [line(t + 2.0, x + 40, 900, x + 400, 900, GRN, 6, 0.5), line(t + 2.5, x + 40, 875, x + 40, 925, GRN, 6, 0.1), line(t + 2.6, x + 400, 875, x + 400, 925, GRN, 6, 0.1),
          Text(t + 2.8, 'a few fm', x + 130, 905, 44, GRN)]
    x = 730; t = 0.47 * d
    e += [Text(t, '2 : Gaussian\nsmaller : longer tail', x, 680, 44, WHITE)]
    e += [curve(t + 2.5, lambda r: (x + 220 + r * 55, 990 - 150 * math.exp(-r * r / 1.2)), -4, 4, 60, WHITE, 6, 0.9),
          curve(t + 3.6, lambda r: (x + 220 + r * 55, 990 - 150 / (1 + r * r / 0.35)), -4, 4, 60, YEL, 6, 0.9)]
    x = 1330; t = 0.68 * d
    e += [Text(t, 'how many pions come\nfrom the hot core,\nnot from a wide halo', x, 660, 42, WHITE)]
    t = 0.80 * d
    e += [scribble(t, x + 220, 930, 34, PINK, 0.6), Text(t + 0.6, 'core', x + 30, 885, 42, PINK),
          ellipse(t + 1.2, x + 220, 930, 105, 105, WHITE, 4, 1.0, dash=True), Text(t + 2.2, 'halo', x + 345, 885, 42, WHITE)]
    S.append(e)

    # ---------------- 6 measurement
    d = D[5]; e = title(0.3, '5.  The measurement  (CMS, 2018)')
    e += [Text(0.02 * d, '4.27 billion PbPb collisions', 90, 190, 60, GRN, mw=900)]
    e += [Text(0.11 * d, 'energy:  5.02 TeV per nucleon pair', 90, 280, 52, WHITE, mw=900)]
    e += [Text(0.20 * d, '1)  pair up same-charge particles,', 90, 400, 50, WHITE, mw=900), Text(0.24 * d, '     same collision', 90, 465, 50, WHITE)]
    e += [Text(0.30 * d, '2)  divide by pairs from', 90, 555, 50, WHITE, mw=900), Text(0.33 * d, '     different collisions', 90, 620, 50, WHITE),
          Text(0.37 * d, '     (no quantum effect)', 90, 685, 44, BLUE)]
    e += [Text(0.47 * d, '3)  Coulomb repulsion + Lévy fit', 90, 775, 50, WHITE, mw=900)]
    e += [Paper(0.63 * d, 'fig2', 1010, 185, 850, 625, -1.2)]
    e += [Text(0.66 * d, 'points = data,  curve = fit', 1120, 815, 46, YEL)]
    T = Text(0.82 * d, '6 centrality classes  x  24 momentum ranges', 90, 900, 54, YEL, mw=1750)
    e += [T, line(0.82 * d + T.dur, 90, 990, 90 + T.width, 993, YEL, 5, 0.4)]
    e += credit()
    S.append(e)

    # ---------------- 7 R
    d = D[6]; e = title(0.3, 'Result 1:  size   R = 1.6 - 5.8 fm')
    e += [Paper(0.12 * d, 'fig4', 60, 185, 900, 570, 1.0)]
    e += [Text(0.17 * d, 'R shrinks as transverse mass grows', 90, 770, 46, GRN, mw=860)]
    e += [Text(0.38 * d, 'black: head-on (central) -> largest', 90, 845, 44, WHITE, mw=860)]
    e += [Text(0.48 * d, 'magenta: glancing -> smallest', 90, 905, 44, PINK, mw=860)]
    e += [Text(0.59 * d, 'more nucleons = bigger fireball', 90, 975, 50, YEL, mw=860)]
    e += [Paper(0.72 * d, 'fig7', 980, 185, 900, 570, -1.0)]
    e += [Text(0.77 * d, 'R  ~  (N_{part})^{1/3}', 1090, 780, 66, YEL)]
    e += [Text(0.88 * d, 'like radius vs. volume', 1090, 890, 48, WHITE)]
    e += credit()
    S.append(e)

    # ---------------- 8 hydro
    d = D[7]; e = title(0.3, 'The fireball expands like a fluid')
    e += [Paper(0.08 * d, 'fig5', 50, 185, 1060, 645, -0.8)]
    T = Text(0.10 * d, '1/R^{2}  =  A · m_{T}  +  B', 1170, 200, 72, YEL, mw=700)
    e += [T, rect(0.10 * d + T.dur, 1150, 215, T.width + 40, 130, YEL, 5, 0.7)]
    e += [Text(0.20 * d, 'hydrodynamics:', 1170, 390, 50, WHITE), Text(0.24 * d, 'a straight line', 1170, 455, 50, WHITE), check(0.33 * d, 1560, 500)]
    e += [Text(0.50 * d, 'slope A  ->  expansion rate', 1170, 560, 46, GRN, mw=700)]
    e += [Text(0.57 * d, '"Hubble constant"', 1170, 625, 52, GRN)]
    e += [Text(0.70 * d, 'H = 0.11 - 0.18 c/fm', 1170, 715, 60, YEL, mw=700)]
    e += [Text(0.84 * d, 'puzzle:   B < 0  ?', 1170, 850, 64, PINK)]
    e += [Text(0.90 * d, 'lines cross the axis below zero', 150, 860, 46, PINK)]
    e += credit()
    S.append(e)

    # ---------------- 9 alpha
    d = D[8]; e = title(0.3, 'Result 2:  shape   α = 1.6 - 2.0')
    e += [Paper(0.36 * d, 'fig9', 60, 190, 780, 810, 1.0)]
    sx, sw, sy = 960, 820, 330
    ax = lambda a: sx + (a - 1.0) * sw
    e += [line(0.03 * d, sx, sy, sx + sw, sy, WHITE, 6, 0.8), line(0.03 * d + 0.8, ax(1), sy - 28, ax(1), sy + 28, PINK, 7, 0.15), line(0.03 * d + 1.0, ax(2), sy - 28, ax(2), sy + 28, WHITE, 7, 0.15),
          Text(0.03 * d + 1.2, '1', ax(1) - 12, sy + 20, 50, PINK), Text(0.03 * d + 1.4, '2', ax(2) - 14, sy + 20, 50, WHITE)]
    e += [Path(0.07 * d, [(ax(1.6), sy - 6), (ax(2.0), sy - 6), (ax(2.0), sy + 6), (ax(1.6), sy + 6), (ax(1.6), sy), (ax(2.0), sy)], YEL, 9, 1.0), Text(0.07 * d + 1.0, 'CMS  PbPb', ax(1.62), sy - 120, 54, YEL)]
    e += [Text(0.15 * d, 'Cauchy', ax(1) - 60, sy + 90, 46, PINK), Text(0.20 * d, 'Gaussian', ax(2) - 110, sy + 90, 46, WHITE)]
    e += [Text(0.26 * d, 'neither!  ->  full Lévy needed', 960, 520, 54, YEL, mw=880)]
    e += [Text(0.40 * d, 'α hardly depends on pair momentum', 960, 630, 44, WHITE, mw=880)]
    e += [Text(0.48 * d, 'more central  ->  closer to 2', 960, 700, 50, GRN, mw=880)]
    e += [scribble(0.62 * d, ax(1.2), sy, 17, BLUE, 0.4), Text(0.62 * d + 0.4, 'RHIC AuAu ≈ 1.2', ax(1.2) - 150, sy - 135, 46, BLUE)]
    e += [Text(0.72 * d, '~50% larger than at RHIC', 960, 800, 50, BLUE, mw=880)]
    e += [Text(0.84 * d, 'denser matter -> less anomalous', 960, 880, 46, WHITE, mw=880), Text(0.90 * d, 'diffusion ?', 960, 940, 46, WHITE)]
    e += credit()
    S.append(e)

    # ---------------- 10 lambda
    d = D[9]; e = title(0.3, 'Result 3:  strength  λ')
    e += [Paper(0.05 * d, 'fig10', 50, 190, 760, 825, -0.8)]
    e += [Text(0.08 * d, 'no particle ID:', 850, 185, 50, WHITE), Text(0.14 * d, 'non-pion pairs weaken the bump', 850, 250, 46, WHITE, mw=1000)]
    T = Text(0.30 * d, 'λ*  =  λ / (pion fraction)^{2}', 850, 350, 60, YEL, mw=1000)
    e += [T, rect(0.30 * d + T.dur, 830, 362, T.width + 40, 115, YEL, 5, 0.7)]
    e += [Text(0.42 * d, 'λ*  flat in transverse mass,', 850, 520, 48, GRN), Text(0.49 * d, 'but still  < 1', 850, 585, 56, PINK)]
    cx, cy = 1620, 800
    t = 0.56 * d
    e += [scribble(t, cx, cy, 52, YEL, 0.8), Text(t + 0.8, 'core', cx - 45, cy - 150, 46, YEL), ellipse(t + 1.4, cx, cy, 190, 190, WHITE, 4, 1.2, dash=True), Text(t + 2.6, 'halo', cx + 120, cy + 150, 46, WHITE)]
    rr = random.Random(8); pts = [(cx + rr.uniform(95, 165) * math.cos(i * 0.7 + 0.3), cy + rr.uniform(95, 165) * math.sin(i * 0.7 + 0.3)) for i in range(9)]
    pts = [p for p in pts if not (cx - 80 < p[0] < cx + 100 and cy - 175 < p[1] < cy - 60)]
    e += [Dots(t + 3.0, pts, GRN, 8, 1.2)]
    e += [Text(0.62 * d, 'some pions come from', 850, 700, 46, WHITE), Text(0.68 * d, 'the halo: decays far', 850, 760, 46, WHITE), Text(0.74 * d, 'from the core', 850, 820, 46, WHITE)]
    e += [Text(0.90 * d, 'λ* smaller when central', 850, 930, 46, BLUE)]
    e += credit()
    S.append(e)

    # ---------------- 11 summary
    d = D[10]; e = title(0.3, 'Summary')
    rows = [(0.06, GRN, 'Quantum correlations = a ruler for the source'),
            (0.22, YEL, 'Size:  R = 1.6 - 5.8 fm,  grows with N_{part}'),
            (0.38, WHITE, 'Scales like an expanding fluid'),
            (0.48, PINK, 'Shape:  α = 1.6 - 2.0,  close to (not exactly) Gaussian'),
            (0.67, BLUE, 'Strength:  λ* < 1,  a core plus a halo')]
    for i, (f, colr, tx) in enumerate(rows):
        y = 190 + i * 118
        T = Text(f * d, tx, 200, y, 58, colr, mw=1620, cps=26)
        e += [T, check(f * d + T.dur + 0.1, 100, y + 80)]
    T = Text(0.78 * d, 'A new, precise picture of hot nuclear matter', 960, 810, 64, YEL, center=True, mw=1700)
    e += [T, rect(0.78 * d + T.dur, 960 - T.width / 2 - 30, 818, T.width + 60, 118, YEL, 5, 0.8)]
    e += [Text(0.95 * d, 'Thanks for watching!', 960, 950, 56, WHITE, center=True)]
    S.append(e)
    return [flat(s) for s in S]

def credit():
    return [Text(0.2, 'figures: CMS, Phys. Rev. C 109, 024914 (2024), CC BY 4.0', 1180, 1018, 26, (200, 205, 195), cps=200)]

# ------------------------------------------------------------------ render
class State: pass

def chalk_stick(im, tip, color):
    d = ImageDraw.Draw(im); x, y = tip
    d.line([x + 5, y + 3, x + 50, y - 66], fill=(18, 30, 26), width=20)
    d.line([x, y, x + 44, y - 68], fill=(250, 250, 244), width=18)
    d.line([x, y, x + 7, y - 11], fill=color, width=18)

def render_scene(els, nframes, board, grain, sink=None, snaps=None):
    st = State(); st.base = board.copy(); st.col = Image.new('RGB', (W, H), WHITE); st.alpha = Image.new('L', (W, H), 0)
    st.dcol = ImageDraw.Draw(st.col); st.dalpha = ImageDraw.Draw(st.alpha); st.fading = None
    els = sorted(els, key=lambda e: e.t); last = None; out = {}
    fade_n = int(0.6 * FPS)
    for f in range(nframes):
        now = f / FPS; tip = None; changed = False
        for e in els:
            if e.done or now < e.t: continue
            e.draw(st, now); changed = True
            if e.tip: tip = (e.tip, getattr(e, 'color', WHITE))
        left = nframes - f
        if changed or last is None or left <= fade_n or (snaps and f in snaps):
            base = st.base
            if st.fading:
                p, a = st.fading
                tmp = st.base.copy(); tmp.paste(p.sheet, p.xy, p.sheet); base = Image.blend(st.base, tmp, a)
            m = ImageChops.multiply(st.alpha.filter(ImageFilter.GaussianBlur(0.9)), grain)
            fr = Image.composite(st.col, base, m)
            if tip: chalk_stick(fr, *tip)
            if left <= fade_n: fr = Image.blend(board, fr, max(0.0, (left - 1) / fade_n))
            last = fr.tobytes()
            if snaps and f in snaps: out[f] = fr.copy()
        if sink: sink.write(last)
    return out

def main():
    durs = []
    for i in range(1, 12):
        with wave.open(os.path.join(AUD, 's%02d.wav' % i)) as w: durs.append(w.getnframes() / w.getframerate())
    nfr = [int(round((d + PAD) * FPS)) for d in durs]
    board = make_board(); grain = make_grain()
    sc = scenes(durs)
    for i, (els, n) in enumerate(zip(sc, nfr)):
        late = [e for e in els if e.t + e.dur > durs[i] + PAD - 0.7]
        if late: print('scene', i + 1, 'has', len(late), 'elements finishing too late', [round(e.t + e.dur - durs[i], 1) for e in late])
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        outd = os.path.join(ROOT, 'levy', 'preview'); os.makedirs(outd, exist_ok=True)
        which = [int(a) for a in sys.argv[2:]] or range(1, 12)
        for i in which:
            n = nfr[i - 1]; snaps = {int(n * 0.45), n - int(0.6 * FPS) - 2}
            got = render_scene(sc[i - 1], n, board, grain, None, snaps)
            for k, f in enumerate(sorted(got)): got[f].resize((1280, 720), Image.LANCZOS).save(os.path.join(outd, 's%02d_%d.png' % (i, k)))
            print('preview scene', i, flush=True)
        return
    out = sys.argv[1]
    wavp = os.path.join(ROOT, 'levy', 'narration_all.wav')
    with wave.open(wavp, 'wb') as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
        for i, n in enumerate(nfr):
            with wave.open(os.path.join(AUD, 's%02d.wav' % (i + 1))) as w: data = w.readframes(w.getnframes())
            need = n * SPF * 2
            lead = int(0.25 * SR) * 2
            data = (b'\0' * lead + data)[:need]
            o.writeframes(data + b'\0' * (need - len(data)))
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
           '-i', wavp, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-shortest', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, (els, n) in enumerate(zip(sc, nfr)):
        render_scene(els, n, board, grain, p.stdin)
        print('scene %d/11 done (%d frames)' % (i + 1, n), flush=True)
    p.stdin.close(); p.wait()
    print('ffmpeg exit', p.returncode)

if __name__ == '__main__':
    main()
