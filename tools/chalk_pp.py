# -*- coding: utf-8 -*-
"""Chalkboard video: CMS Bose-Einstein correlations in pp at 13 TeV (JHEP 03 (2020) 014)."""
import math, os, random, subprocess, sys, wave
from PIL import Image
import chalk as E
from chalk import Text, Path, Dots, Paper, line, arrow, ellipse, rect, curve, check, title, scribble, flat
from chalk import WHITE, YEL, PINK, BLUE, GRN, ORG, W, H, FPS, SR, SPF, PAD

ROOT = os.path.dirname(os.path.abspath(__file__))
E.FIG = os.path.join(ROOT, 'pp', 'figs'); AUD = os.path.join(ROOT, 'pp', 'audio'); NS = 10


def credit():
    return [Text(0.2, 'figures: CMS, JHEP 03 (2020) 014, CC BY 4.0', 1330, 1018, 26, (200, 205, 195), cps=200)]


def burst(t, cx, cy, n, rmin, rmax, seed, dur=1.2):
    rr = random.Random(seed); out = []; pts = []
    for i in range(n):
        a = i * 2 * math.pi / n + rr.uniform(-0.12, 0.12); r = rr.uniform(rmin, rmax)
        p = (cx + r * math.cos(a), cy + r * 0.9 * math.sin(a)); pts.append(p)
        out.append(Path(t + i * dur / n, [(cx + 12 * math.cos(a), cy + 12 * math.sin(a)), p], WHITE, 3, 0.1))
    out += [Dots(t + 0.2, pts[0::3], GRN, 7, dur), Dots(t + 0.25, pts[1::3], YEL, 7, dur), Dots(t + 0.3, pts[2::3], PINK, 7, dur)]
    return out


def scenes(D):
    S = []
    # ---------------- 1 title
    d = D[0]; e = []
    e += [Text(0.4, 'How big is a', 960, 150, 90, WHITE, center=True, cps=18)]
    e += [Text(2.0, 'proton-proton collision?', 960, 280, 140, YEL, center=True, cps=14)]
    e += [line(4.4, 330, 495, 1590, 501, YEL, 6, 0.6)]
    e += [Text(0.30 * d, '...and does it behave like a tiny hot fluid?', 960, 560, 62, PINK, center=True, cps=24)]
    e += [Text(0.55 * d, 'Bose-Einstein correlations of charged hadrons', 960, 700, 58, WHITE, center=True, cps=28)]
    e += [Text(0.70 * d, 'pp collisions at 13 TeV   |   CMS experiment, LHC', 960, 800, 54, BLUE, center=True, cps=28)]
    e += [Text(0.88 * d, 'based on  JHEP 03 (2020) 014', 960, 930, 40, WHITE, center=True, cps=32)]
    S.append(e)

    # ---------------- 2 setting
    d = D[1]; e = title(0.3, '1.  Small collisions, big surprise')
    y = 320
    e += [ellipse(0.04 * d, 170, y, 80, 80, BLUE), Text(0.04 * d + 0.6, 'Pb', 140, y - 45, 50, BLUE)]
    e += arrow(0.06 * d, 265, y, 340, y) + arrow(0.07 * d, 475, y, 400, y)
    e += [ellipse(0.08 * d, 570, y, 80, 80, BLUE), Text(0.08 * d + 0.6, 'Pb', 540, y - 45, 50, BLUE)]
    e += arrow(0.11 * d, 680, y, 790, y, YEL)
    e += [ellipse(0.12 * d, 930, y, 110, 110, ORG, 7, 0.8), scribble(0.12 * d + 0.8, 930, y, 66, YEL, 0.9)]
    e += [Text(0.15 * d, 'quark-gluon plasma', 1090, y - 105, 54, ORG), Text(0.20 * d, 'flows like a fluid', 1090, y - 25, 54, GRN)]
    y = 640
    e += [ellipse(0.26 * d, 170, y, 26, 26, BLUE), Text(0.26 * d + 0.4, 'p', 155, y + 30, 50, BLUE)]
    e += arrow(0.28 * d, 215, y, 320, y) + arrow(0.29 * d, 525, y, 420, y)
    e += [ellipse(0.30 * d, 570, y, 26, 26, BLUE), Text(0.30 * d + 0.4, 'p', 555, y + 30, 50, BLUE)]
    e += [Text(0.33 * d, 'much smaller!', 250, y + 55, 44, WHITE)]
    e += arrow(0.40 * d, 680, y, 790, y, YEL)
    e += burst(0.42 * d, 910, y, 6, 50, 95, 2, 0.6) + [Text(0.44 * d, 'usually:\na few particles', 800, y + 100, 44, WHITE)]
    e += burst(0.50 * d, 1330, y, 34, 60, 150, 4, 1.6) + [Text(0.53 * d, 'rarely:\n> 100 particles', 1220, y + 150, 44, YEL)]
    e += [Text(0.63 * d, 'hints of\nfluid-like\nbehaviour!', 1570, y - 110, 50, PINK)]
    T = Text(0.76 * d, 'A tiny fireball?   ->   measure the size of the source', 960, 925, 62, YEL, center=True, mw=1700)
    e += [T, rect(0.76 * d + T.dur, 960 - T.width / 2 - 30, 932, T.width + 60, 115, YEL, 5, 0.8)]
    S.append(e)

    # ---------------- 3 method
    d = D[2]; e = title(0.3, '2.  A quantum ruler')
    ox, oy, pw, ph = 150, 900, 720, 600; base = oy - 220; amp = 330
    e += [Text(0.05 * d, 'pions are bosons', 1010, 185, 56, WHITE)]
    e += [Text(0.10 * d, 'identical bosons come out with', 1010, 260, 48, WHITE, mw=850), Text(0.14 * d, 'nearly the same momentum', 1010, 322, 48, WHITE, mw=850)]
    t = 0.19 * d
    e += arrow(t, ox, oy, ox + pw + 30, oy) + arrow(t + 0.6, ox, oy, ox, oy - ph - 20)
    e += [Text(t + 1.2, 'q', ox + pw + 10, oy - 5, 54, WHITE), Text(t + 1.4, 'pairs', ox + 20, oy - ph - 70, 50, WHITE),
          line(t + 1.8, ox, base, ox + pw, base, WHITE, 3, 0.5, dash=True), Text(t + 2.3, '1', ox - 50, base - 60, 48, WHITE)]
    f1 = lambda q: (ox + q * pw, base - amp * math.exp(-(q * 12)))
    f2 = lambda q: (ox + q * pw, base - amp * math.exp(-(q * 4.0)))
    e += [curve(0.29 * d, f2, 0, 1, 90, PINK, 8, 1.6), Text(0.31 * d, 'excess at small q', 420, 400, 46, WHITE)]
    T = Text(0.38 * d, 'peak width  ~  1 / (source size)', 1010, 430, 56, YEL, mw=840)
    e += [T, rect(0.38 * d + T.dur, 990, 435, T.width + 40, 110, YEL, 5, 0.7)]
    e += [Text(0.46 * d, 'wide peak = SMALL source', 230, 700, 46, PINK)]
    e += [curve(0.51 * d, f1, 0, 1, 90, GRN, 8, 1.6), Text(0.52 * d, 'narrow peak = LARGE source', 230, 770, 46, GRN)]
    e += [Text(0.59 * d, 'C(q)  =  C [ 1 + λ e^{-qR} ]', 1010, 590, 68, WHITE, mw=850, cps=12)]
    e += [Text(0.68 * d, 'R = radius of the source', 1010, 720, 52, GRN), Text(0.74 * d, '     ("length of homogeneity")', 1010, 785, 42, GRN)]
    e += [Text(0.81 * d, 'λ = strength of the correlation', 1010, 860, 50, PINK, mw=850)]
    e += [Text(0.90 * d, 'exponential fits better than Gaussian', 1010, 950, 42, BLUE, mw=850)]
    S.append(e)

    # ---------------- 4 data
    d = D[3]; e = title(0.3, '3.  The data  (CMS, 2015)')
    e += [Text(0.02 * d, 'pp collisions at 13 TeV', 110, 190, 64, GRN)]
    e += [Text(0.10 * d, 'special runs: only ~0.1 collisions per beam crossing', 110, 300, 50, WHITE, mw=1700)]
    e += [Text(0.24 * d, '->  one clean pp collision per event', 110, 375, 54, YEL)]
    e += [Text(0.36 * d, 'high-multiplicity trigger keeps the rare busy events', 110, 490, 50, WHITE, mw=1700)]
    ax0, ax1, ay = 200, 1700, 760
    e += arrow(0.50 * d, ax0, ay, ax1 + 40, ay)
    e += [line(0.50 * d + 0.7, ax0, ay - 20, ax0, ay + 20, WHITE, 5, 0.1), line(0.50 * d + 0.8, ax1, ay - 20, ax1, ay + 20, WHITE, 5, 0.1),
          Text(0.50 * d + 0.9, 'few', ax0 - 40, ay + 15, 46, WHITE), Text(0.55 * d, '~250 charged particles', ax1 - 420, ay + 15, 46, YEL)]
    e += burst(0.52 * d, ax0 + 30, ay - 95, 5, 30, 60, 3, 0.4) + burst(0.56 * d, ax1 - 80, ay - 115, 40, 40, 105, 6, 1.5)
    e += [Text(0.60 * d, 'multiplicity N', 820, ay - 90, 50, WHITE)]
    e += [Text(0.72 * d, 'study the source vs.  multiplicity N  and  pair momentum k_{T}', 110, 920, 52, BLUE, mw=1700)]
    S.append(e)

    # ---------------- 5 background
    d = D[4]; e = title(0.3, '4.  The catch: fake correlations')
    e += [Text(0.10 * d, 'close pairs also come from...', 70, 180, 50, WHITE)]
    t = 0.14 * d
    for i, a in enumerate((-0.25, -0.1, 0.05, 0.2)):
        e += [Path(t + i * 0.15, [(110, 330), (110 + 190 * math.cos(a), 330 + 190 * math.sin(a))], ORG, 4, 0.2)]
    e += [Text(t + 0.6, 'jets', 150, 380, 48, ORG)]
    t = 0.18 * d
    e += [Path(t, [(450, 330), (540, 330)], BLUE, 5, 0.2, dash=True), Path(t + 0.2, [(540, 330), (640, 285)], BLUE, 4, 0.2), Path(t + 0.4, [(540, 330), (640, 375)], BLUE, 4, 0.2),
          Text(t + 0.6, 'decays', 470, 380, 48, BLUE)]
    e += [Text(0.25 * d, '3 ways to remove them:', 70, 480, 54, YEL)]
    e += [Text(0.30 * d, '1)  data / simulation without BEC', 70, 570, 46, WHITE, mw=850), Text(0.34 * d, '     (double ratio)', 70, 625, 40, GRN)]
    e += [Text(0.40 * d, '2)  opposite-charge pairs from data', 70, 700, 46, WHITE, mw=850), Text(0.46 * d, '     (cluster subtraction)', 70, 755, 40, GRN)]
    e += [Text(0.54 * d, '3)  a hybrid of both', 70, 830, 46, WHITE, mw=850)]
    e += [Paper(0.60 * d, 'fig3a', 920, 175, 480, 470, 1.2), Paper(0.60 * d + 0.3, 'fig3b', 1410, 175, 480, 470, -1.2)]
    e += [Text(0.66 * d, 'black: same charge (BEC peak)', 960, 655, 44, WHITE, mw=900)]
    e += [Text(0.74 * d, 'blue: opposite charge (no BEC)', 960, 715, 44, BLUE, mw=900)]
    e += [Text(0.83 * d, 'low multiplicity', 990, 800, 44, YEL), Text(0.88 * d, 'high multiplicity:', 1440, 800, 44, YEL)]
    e += [Text(0.93 * d, 'narrower peak = larger source', 1280, 870, 46, GRN)]
    e += credit()
    S.append(e)

    # ---------------- 6 result 1
    d = D[5]; e = title(0.3, 'Result 1:  the source grows with multiplicity')
    e += [Paper(0.04 * d, 'fig4top', 40, 180, 1390, 600, -0.6)]
    e += [Text(0.08 * d, 'R :', 1470, 200, 60, YEL), Text(0.12 * d, '0.8  ->  3 fm', 1470, 280, 58, YEL, mw=420)]
    e += [Text(0.30 * d, 'proton radius', 1470, 400, 44, BLUE), Text(0.36 * d, '< 1 fm', 1470, 455, 50, BLUE)]
    e += [Text(0.47 * d, '3 methods', 1470, 570, 48, GRN), Text(0.50 * d, 'agree', 1470, 630, 48, GRN), check(0.53 * d, 1640, 690)]
    e += [Text(0.58 * d, 'left:  steep rise, slope change near N ~ 20-30, then levelling off', 70, 800, 46, WHITE, mw=1780)]
    e += [Text(0.80 * d, 'right:  strength λ drops fast, then stays roughly constant', 70, 880, 46, PINK, mw=1780)]
    e += credit()
    S.append(e)

    # ---------------- 7 energy
    d = D[6]; e = title(0.3, 'Does the collision energy matter?')
    e += [Paper(0.10 * d, 'fig5', 40, 180, 1390, 620, 0.6)]
    e += [Text(0.18 * d, 'red:', 1470, 210, 52, PINK), Text(0.22 * d, '13 TeV', 1470, 270, 60, PINK)]
    e += [Text(0.36 * d, 'black:', 1470, 390, 52, WHITE), Text(0.40 * d, '7 TeV', 1470, 450, 60, WHITE), Text(0.46 * d, '(CMS, ATLAS)', 1470, 525, 42, WHITE)]
    e += [Text(0.56 * d, 'they agree!', 1470, 640, 56, GRN), check(0.60 * d, 1560, 760)]
    T = Text(0.70 * d, 'same multiplicity  ->  same size, whatever the energy', 960, 870, 60, YEL, center=True, mw=1700)
    e += [T, rect(0.70 * d + T.dur, 960 - T.width / 2 - 30, 877, T.width + 60, 112, YEL, 5, 0.8)]
    e += credit()
    S.append(e)

    # ---------------- 8 cube root + CGC
    d = D[7]; e = title(0.3, 'Result 2:  R grows like N^{1/3}')
    e += [Paper(0.03 * d, 'fig6', 40, 180, 1390, 620, -0.6)]
    e += [Text(0.08 * d, 'N ~ volume', 1470, 200, 52, WHITE), Text(0.12 * d, '   ~ R^{3}', 1470, 265, 56, WHITE)]
    T = Text(0.17 * d, 'R ~ N^{1/3}', 1480, 370, 64, YEL)
    e += [T, rect(0.17 * d + T.dur, 1460, 380, T.width + 40, 120, YEL, 5, 0.6)]
    e += [Text(0.26 * d, 'fluid models', 1470, 540, 46, GRN), Text(0.29 * d, 'predict this', 1470, 595, 46, GRN), check(0.31 * d, 1740, 640)]
    e += [Text(0.44 * d, 'right:  colour glass condensate (blue curve)', 70, 810, 46, BLUE, mw=1330)]
    e += [Text(0.56 * d, 'radius far too small  (initial size only, no expansion)', 70, 875, 44, WHITE, mw=1330)]
    e += [Text(0.78 * d, 'but the same shape:  rise, then plateau', 70, 940, 46, YEL, mw=1330)]
    e += [Text(0.88 * d, 'saturation', 1470, 740, 46, PINK), Text(0.91 * d, 'above ~100', 1470, 795, 46, PINK), Text(0.94 * d, 'particles ?', 1470, 850, 46, PINK)]
    e += credit()
    S.append(e)

    # ---------------- 9 expansion
    d = D[8]; e = title(0.3, 'Result 3:  the source is expanding')
    e += [Paper(0.17 * d, 'fig4botL', 30, 180, 590, 540, 1.0)]
    e += [Text(0.20 * d, 'R shrinks as pair', 70, 730, 44, GRN), Text(0.24 * d, 'momentum k_{T} grows', 70, 785, 44, GRN)]
    e += [Paper(0.36 * d, 'fig7', 630, 180, 1260, 540, -0.6)]
    e += [Text(0.30 * d, '1/R^{2}  =  a + b · m_{T}', 700, 735, 56, YEL)]
    e += [Text(0.42 * d, 'straight lines, as in heavy-ion collisions', 700, 815, 44, WHITE, mw=1150), check(0.47 * d, 1560, 860)]
    e += [Text(0.55 * d, 'slope -> "Hubble" expansion rate', 700, 880, 44, GRN, mw=800)]
    e += [Text(0.64 * d, 'H ~ 0.17 - 0.30 /fm', 1370, 880, 48, YEL, mw=500)]
    e += [Text(0.72 * d, '(gold-gold: 0.1 - 0.2 /fm)', 1370, 945, 38, BLUE, mw=500)]
    e += [Text(0.82 * d, 'blue (many particles): slower expansion', 70, 945, 42, BLUE, mw=1200)]
    e += credit()
    S.append(e)

    # ---------------- 10 summary
    d = D[9]; e = title(0.3, 'Summary')
    rows = [(0.05, GRN, 'Bose-Einstein correlations measure the pp source size'),
            (0.16, YEL, 'R:  0.8 -> 3 fm,  grows like N^{1/3}'),
            (0.33, PINK, 'possible saturation at the highest multiplicities'),
            (0.42, WHITE, 'same size at 7 and 13 TeV'),
            (0.50, BLUE, 'R shrinks with pair momentum:  an expanding source')]
    for i, (f, colr, tx) in enumerate(rows):
        y = 180 + i * 108
        T = Text(f * d, tx, 200, y, 56, colr, mw=1620, cps=26)
        e += [T, check(f * d + T.dur + 0.1, 100, y + 78)]
    T = Text(0.63 * d, 'Busy pp collisions look like mini heavy-ion collisions', 960, 760, 62, YEL, center=True, mw=1700)
    e += [T, rect(0.63 * d + T.dur, 960 - T.width / 2 - 30, 767, T.width + 60, 115, YEL, 5, 0.8)]
    e += [Text(0.84 * d, 'Why?  Still an open question.', 560, 920, 54, PINK, center=True)]
    e += [Text(0.94 * d, 'Thanks for watching!', 1400, 920, 54, WHITE, center=True)]
    S.append(e)
    return [flat(s) for s in S]


def main():
    durs = []
    for i in range(1, NS + 1):
        with wave.open(os.path.join(AUD, 's%02d.wav' % i)) as w: durs.append(w.getnframes() / w.getframerate())
    nfr = [int(round((d + PAD) * FPS)) for d in durs]
    board = E.make_board(); grain = E.make_grain(); sc = scenes(durs)
    for i, els in enumerate(sc):
        late = [e for e in els if e.t + e.dur > durs[i] + PAD - 0.7]
        if late: print('scene', i + 1, 'late elements:', [round(e.t + e.dur - durs[i], 1) for e in late])
    starts = [sum(nfr[:i]) / FPS for i in range(NS)]
    print('chapter starts (s):', [round(s) for s in starts], 'total', round(sum(nfr) / FPS))
    if sys.argv[1] == 'preview':
        outd = os.path.join(ROOT, 'pp', 'preview'); os.makedirs(outd, exist_ok=True)
        for i in ([int(a) for a in sys.argv[2:]] or range(1, NS + 1)):
            n = nfr[i - 1]; f = n - int(0.6 * FPS) - 2
            got = E.render_scene(sc[i - 1], n, board, grain, None, {f})
            got[f].resize((1280, 720), Image.LANCZOS).save(os.path.join(outd, 's%02d.png' % i)); print('preview', i, flush=True)
        return
    out = sys.argv[1]; wavp = os.path.join(ROOT, 'pp', 'narration_all.wav')
    with wave.open(wavp, 'wb') as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
        for i, n in enumerate(nfr):
            with wave.open(os.path.join(AUD, 's%02d.wav' % (i + 1))) as w: data = w.readframes(w.getnframes())
            need = n * SPF * 2; data = (b'\0' * (int(0.25 * SR) * 2) + data)[:need]
            o.writeframes(data + b'\0' * (need - len(data)))
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
           '-i', wavp, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-shortest', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, (els, n) in enumerate(zip(sc, nfr)):
        E.render_scene(els, n, board, grain, p.stdin); print('scene %d/%d done' % (i + 1, NS), flush=True)
    p.stdin.close(); p.wait(); print('ffmpeg exit', p.returncode)


if __name__ == '__main__':
    main()
