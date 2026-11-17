# -*- coding: utf-8 -*-
"""Chalkboard video: CMS Bose-Einstein correlations in pp, pPb and PbPb (Phys. Rev. C 97, 064912)."""
import math, os, random, subprocess, sys, wave
from PIL import Image
import chalk as E
from chalk import Text, Path, Dots, Paper, line, arrow, ellipse, rect, curve, check, title, scribble, flat
from chalk import WHITE, YEL, PINK, BLUE, GRN, ORG, W, H, FPS, SR, SPF, PAD

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'ppb')
E.FIG = os.path.join(WORK, 'figs'); AUD = os.path.join(WORK, 'audio'); NS = 10


def credit():
    return [Text(0.2, 'figures: CMS, Phys. Rev. C 97, 064912 (2018), CC BY 4.0', 1180, 1018, 26, (200, 205, 195), cps=200)]


def scenes(D):
    S = []
    # ---------------- 1 title
    d = D[0]; e = []
    e += [Text(0.4, 'pp,   pPb,   PbPb', 960, 140, 100, WHITE, center=True, cps=14)]
    e += [Text(0.22 * d, 'three collisions, one ruler', 960, 280, 130, YEL, center=True, cps=14, mw=1750)]
    e += [line(0.22 * d + 2.2, 250, 480, 1670, 486, YEL, 6, 0.6)]
    e += [Text(0.50 * d, 'does the particle source look different?', 960, 545, 62, PINK, center=True, cps=24)]
    e += [Text(0.70 * d, 'Bose-Einstein correlations of pions and kaons', 960, 690, 58, WHITE, center=True, cps=28)]
    e += [Text(0.80 * d, 'CMS experiment, LHC   |   0.9 - 7 TeV', 960, 790, 54, BLUE, center=True, cps=28)]
    e += [Text(0.92 * d, 'based on  Phys. Rev. C 97, 064912 (2018)', 960, 930, 40, WHITE, center=True, cps=32)]
    S.append(e)

    # ---------------- 2 three systems
    d = D[1]; e = title(0.3, '1.  Three collision systems')
    y = 250; t = 0.05 * d
    e += [ellipse(t, 170, y, 26, 26, BLUE), Text(t + 0.4, 'p', 155, y + 28, 46, BLUE)]
    e += arrow(t + 0.6, 215, y, 320, y) + arrow(t + 0.9, 525, y, 420, y)
    e += [ellipse(t + 1.2, 570, y, 26, 26, BLUE), Text(t + 1.6, 'p', 555, y + 28, 46, BLUE)]
    e += [Text(0.07 * d, 'pp', 700, y - 45, 64, GRN), Text(0.10 * d, '0.9,  2.76,  7 TeV', 900, y - 40, 56, WHITE, cps=10)]
    y = 440; t = 0.22 * d
    e += [ellipse(t, 170, y, 26, 26, BLUE), Text(t + 0.4, 'p', 155, y + 28, 46, BLUE)]
    e += arrow(t + 0.6, 215, y, 320, y) + arrow(t + 0.9, 475, y, 400, y)
    e += [ellipse(t + 1.2, 570, y, 78, 78, BLUE), Text(t + 1.8, 'Pb', 538, y - 45, 52, BLUE)]
    e += [Text(0.25 * d, 'pPb', 700, y - 45, 64, GRN), Text(0.28 * d, '5.02 TeV', 900, y - 40, 56, WHITE, cps=12)]
    y = 730; t = 0.33 * d
    e += [ellipse(t, 190, y - 58, 78, 78, BLUE), Text(t + 0.6, 'Pb', 158, y - 103, 52, BLUE)]
    e += arrow(t + 0.9, 285, y - 58, 360, y - 58) + arrow(t + 1.2, 455, y + 58, 380, y + 58)
    e += [ellipse(t + 1.5, 550, y + 58, 78, 78, BLUE), Text(t + 2.1, 'Pb', 518, y + 13, 52, BLUE)]
    e += [Text(0.35 * d, 'PbPb', 700, y - 75, 64, GRN), Text(0.38 * d, '2.76 TeV', 900, y - 70, 56, WHITE, cps=12)]
    e += [Text(0.43 * d, 'peripheral only:  nuclei barely overlap', 700, y + 10, 44, PINK, mw=800)]
    e += [Text(0.58 * d, 'about as many\nparticles as the\nbusiest pPb', 1500, 400, 46, ORG)]
    e += arrow(0.58 * d + 2.2, 1560, 590, 1480, 690, ORG, 5)
    T = Text(0.76 * d, 'Same number of particles   ->   same source size?', 960, 925, 62, YEL, center=True, mw=1700)
    e += [T, rect(0.76 * d + T.dur, 960 - T.width / 2 - 30, 932, T.width + 60, 115, YEL, 5, 0.8)]
    S.append(e)

    # ---------------- 3 method
    d = D[2]; e = title(0.3, '2.  The quantum ruler')
    ox, oy, pw, ph = 150, 900, 720, 600; base = oy - 220; amp = 330
    e += [Text(0.09 * d, '1 fm  =  10^{-15} m', 1010, 180, 56, BLUE)]
    e += [Text(0.26 * d, 'pions, kaons  =  bosons', 1010, 262, 52, WHITE)]
    e += [Text(0.31 * d, 'identical bosons: nearly the same momentum', 1010, 335, 44, WHITE, mw=850)]
    t = 0.40 * d
    e += arrow(t, ox, oy, ox + pw + 30, oy) + arrow(t + 0.6, ox, oy, ox, oy - ph - 20)
    e += [Text(t + 1.2, 'q', ox + pw + 10, oy - 5, 54, WHITE), Text(t + 1.4, 'pairs', ox + 20, oy - ph - 70, 50, WHITE),
          line(t + 1.8, ox, base, ox + pw, base, WHITE, 3, 0.5, dash=True), Text(t + 2.3, '1', ox - 50, base - 60, 48, WHITE)]
    f1 = lambda q: (ox + q * pw, base - amp * math.exp(-(q * 12)))
    f2 = lambda q: (ox + q * pw, base - amp * math.exp(-(q * 4.0)))
    e += [curve(0.50 * d, f2, 0, 1, 90, PINK, 8, 1.6), Text(0.52 * d, 'peak at small q', 430, 400, 46, WHITE)]
    T = Text(0.58 * d, 'peak width  ~  1 / (source size)', 1010, 430, 56, YEL, mw=840)
    e += [T, rect(0.58 * d + T.dur, 990, 435, T.width + 40, 110, YEL, 5, 0.7)]
    e += [curve(0.67 * d, f1, 0, 1, 90, GRN, 8, 1.4), Text(0.68 * d, 'narrow peak = LARGE source', 230, 735, 46, GRN)]
    e += [Text(0.76 * d, 'C(q)  =  C [ 1 + λ e^{-qR} ]', 1010, 590, 68, WHITE, mw=850, cps=14)]
    e += [Text(0.86 * d, 'R = radius of the source', 1010, 730, 52, GRN)]
    e += [Text(0.93 * d, 'λ = strength of the correlation', 1010, 830, 50, PINK, mw=850)]
    S.append(e)

    # ---------------- 4 particle identification
    d = D[3]; e = title(0.3, '3.  Which particle is which?')
    e += [Text(0.02 * d, 'BEC needs\nidentical particles', 70, 185, 46, WHITE)]
    e += [Text(0.17 * d, 'silicon tracker', 70, 335, 52, GRN)]
    e += [Text(0.25 * d, 'a particle loses a\nlittle energy in it', 70, 415, 44, WHITE)]
    e += [Text(0.36 * d, 'heavier = slower\n= more energy loss', 70, 560, 46, YEL)]
    e += [Paper(0.46 * d, 'fig1', 560, 185, 1320, 572, -0.5)]
    e += [Text(0.55 * d, 'bands:   pions,   kaons,   protons', 600, 775, 50, PINK)]
    e += [Text(0.63 * d, 'left:  all positive particles', 600, 850, 44, WHITE)]
    e += [Text(0.71 * d, 'right:  identified,  purity > 99.5%', 600, 912, 44, GRN)]
    T = Text(0.90 * d, 'clean pions\nand kaons', 70, 760, 54, YEL)
    e += [T, check(0.90 * d + T.dur, 360, 880)]
    e += credit()
    S.append(e)

    # ---------------- 5 corrections
    d = D[4]; e = title(0.3, '4.  Cleaning up the peak')
    e += [Text(0.07 * d, '1)  electric charge  (Coulomb)', 70, 180, 54, YEL)]
    t = 0.11 * d
    e += [ellipse(t, 210, 325, 30, 30, PINK, 5, 0.4), Text(t + 0.3, '+', 196, 288, 50, PINK), ellipse(t + 0.5, 320, 325, 30, 30, PINK, 5, 0.4), Text(t + 0.8, '+', 306, 288, 50, PINK)]
    e += arrow(t + 1.1, 172, 325, 100, 325, PINK, 5, 0.3) + arrow(t + 1.4, 358, 325, 430, 325, PINK, 5, 0.3)
    e += [Text(0.13 * d, 'same charge repels:  fewer pairs at small q', 480, 275, 42, WHITE, mw=660)]
    T = Text(0.20 * d, 'calculated and corrected', 480, 340, 44, GRN)
    e += [T, check(0.20 * d + T.dur, 490 + T.width, 385)]
    e += [Text(0.26 * d, '2)  "clusters"', 70, 440, 54, YEL)]
    t = 0.30 * d
    for i, a in enumerate((-0.25, -0.1, 0.05, 0.2)):
        e += [Path(t + i * 0.15, [(110, 590), (110 + 190 * math.cos(a), 590 + 190 * math.sin(a))], ORG, 4, 0.2)]
    e += [Text(t + 0.6, 'small jets', 130, 632, 44, ORG)]
    t = 0.34 * d
    e += [Path(t, [(470, 590), (560, 590)], BLUE, 5, 0.2, dash=True), Path(t + 0.2, [(560, 590), (660, 545)], BLUE, 4, 0.2), Path(t + 0.4, [(560, 590), (660, 635)], BLUE, 4, 0.2),
          Text(t + 0.6, 'decays', 490, 632, 44, BLUE)]
    e += [Text(0.37 * d, 'also close\nin momentum', 760, 545, 42, WHITE)]
    e += [Text(0.43 * d, 'opposite-charge pairs:  no BEC, but clusters', 70, 725, 46, BLUE, mw=1050)]
    e += [Paper(0.56 * d, 'fig3b', 1180, 180, 700, 617, 0.8)]
    e += [Text(0.58 * d, 'broad bump = clusters', 1270, 805, 44, BLUE)]
    e += [Text(0.63 * d, 'scale it, remove it from same-charge pairs', 70, 800, 46, WHITE, mw=1050)]
    e += [Text(0.73 * d, 'pp cross-check:  data / simulation without BEC', 70, 885, 44, WHITE, mw=1050)]
    T = Text(0.95 * d, 'the two methods agree', 70, 955, 46, GRN)
    e += [T, check(0.95 * d + T.dur, 90 + T.width, 1000)]
    e += credit()
    S.append(e)

    # ---------------- 6 result 1
    d = D[5]; e = title(0.3, 'Result 1:  more particles, bigger source')
    e += [Paper(0.06 * d, 'fig20top', 40, 185, 1130, 489, -0.5)]
    e += [Text(0.10 * d, 'pion pairs in pPb', 420, 690, 42, WHITE)]
    e += [Text(0.22 * d, 'few particles', 110, 750, 46, YEL), Text(0.28 * d, 'many particles', 690, 750, 46, YEL)]
    e += [Text(0.34 * d, 'narrower peak', 690, 808, 46, GRN)]
    e += [Text(0.43 * d, 'R :   2.1 fm   ->   3.95 fm', 110, 880, 58, GRN, cps=12)]
    e += [Paper(0.52 * d, 'fig22R', 1240, 185, 610, 566, 0.6)]
    e += [Text(0.60 * d, 'radius vs. multiplicity N_{trk}', 1250, 775, 42, WHITE, mw=620)]
    e += [Text(0.74 * d, 'grows in every system', 1250, 835, 46, PINK, mw=620)]
    e += [Text(0.81 * d, 'about 1 -> 5 fm', 1250, 898, 50, YEL)]
    e += [Text(0.90 * d, 'pp:  R ~ N^{1/3}', 690, 955, 54, YEL)]
    e += credit()
    S.append(e)

    # ---------------- 7 system comparison
    d = D[6]; e = title(0.3, 'Does it matter what collides?')
    e += [Paper(0.03 * d, 'fig22R', 60, 180, 800, 742, -0.6)]
    e += [Text(0.17 * d, 'pp at 3 energies  (red, green, blue)', 930, 195, 48, WHITE, mw=940)]
    e += [Text(0.25 * d, 'on top of each other', 930, 260, 48, GRN), check(0.25 * d + 1.2, 1500, 305)]
    e += [Text(0.35 * d, 'pPb  (magenta):  the same trend', 930, 370, 48, PINK, mw=940)]
    e += [Text(0.46 * d, 'peripheral PbPb  (orange):  close,', 930, 470, 48, ORG, mw=940)]
    e += [Text(0.52 * d, 'somewhat larger at high multiplicity', 930, 532, 42, ORG, mw=940)]
    T1 = Text(0.62 * d, 'size is set by HOW MANY particles,', 950, 650, 52, YEL, mw=900)
    T2 = Text(0.72 * d, 'not by WHAT collided, or at what energy', 950, 722, 52, YEL, mw=900)
    e += [T1, T2, rect(0.72 * d + T2.dur, 930, 655, max(T1.width, T2.width) + 40, 165, YEL, 5, 0.9)]
    e += [Text(0.88 * d, 'some differences at the highest multiplicities', 930, 880, 42, BLUE, mw=940)]
    e += credit()
    S.append(e)

    # ---------------- 8 shape
    d = D[7]; e = title(0.3, 'Result 2:  the shape of the source')
    cx, cy = 300, 430
    e += [line(0.05 * d, 60, cy, 600, cy, WHITE, 3, 0.6, dash=True), Text(0.05 * d + 0.6, 'beam', 70, cy + 8, 38, WHITE)]
    e += arrow(0.12 * d, cx, cy, cx + 250, cy, GRN, 7) + [Text(0.12 * d + 0.5, 'long', cx + 150, cy - 100, 50, GRN)]
    e += arrow(0.17 * d, cx, cy, cx, cy - 200, PINK, 7) + [Text(0.17 * d + 0.5, 'out', cx + 20, cy - 235, 50, PINK), Text(0.20 * d, '(pair direction)', cx + 110, cy - 220, 36, PINK)]
    e += arrow(0.27 * d, cx, cy, cx - 130, cy + 120, BLUE, 7) + [Text(0.27 * d + 0.5, 'side', cx - 110, cy + 125, 50, BLUE)]
    e += [Paper(0.33 * d, 'fig27top', 740, 180, 1120, 500, 0.5)]
    e += [Text(0.35 * d, 'R_{L}  (long)', 930, 695, 44, GRN), Text(0.37 * d, 'R_{O}  (out)', 1500, 695, 44, PINK)]
    e += [Text(0.40 * d, 'pp, pPb:   R_{L} > R_{S} > R_{O}', 70, 765, 50, YEL, mw=680)]
    e += [Text(0.45 * d, '->  stretched along the beam', 790, 768, 46, GRN), ellipse(0.47 * d, 1560, 808, 95, 36, GRN, 6, 0.6)]
    e += [Text(0.50 * d, 'peripheral PbPb:   R_{L} ~ R_{O} ~ R_{S}', 70, 850, 50, ORG, mw=680)]
    e += [Text(0.58 * d, '->  nearly symmetric', 790, 853, 46, ORG), ellipse(0.60 * d, 1560, 893, 40, 40, ORG, 6, 0.6)]
    e += [Text(0.66 * d, 'biggest difference:  R_{O}', 70, 940, 48, PINK)]
    e += [Text(0.86 * d, '->  different lifetimes ?', 790, 940, 50, YEL)]
    e += credit()
    S.append(e)

    # ---------------- 9 kT and kaons
    d = D[8]; e = title(0.3, 'Two more observations')
    e += [Text(0.05 * d, '1)  R shrinks as pair\n     momentum k_{T} grows', 690, 185, 44, GRN)]
    e += [Paper(0.15 * d, 'fig24pPb', 40, 185, 620, 538, -0.8)]
    e += [Text(0.19 * d, 'pPb pions:  one line per multiplicity class', 50, 735, 38, WHITE, mw=610)]
    e += [Text(0.30 * d, '->  expanding source', 690, 325, 48, YEL)]
    T = Text(0.47 * d, 'R  =  f(N) · g(k_{T})', 720, 440, 56, YEL, mw=500)
    e += [T, rect(0.47 * d + T.dur, 700, 448, T.width + 40, 112, YEL, 5, 0.7)]
    e += [Text(0.53 * d, 'the two dependences\n"factorize"', 700, 580, 42, WHITE)]
    e += [Paper(0.66 * d, 'fig23R', 1260, 185, 620, 575, 0.8)]
    e += [Text(0.67 * d, '2)  kaons', 700, 725, 54, PINK)]
    e += [Text(0.73 * d, '~100x fewer kaon pairs  ->  larger uncertainties', 700, 810, 44, WHITE, mw=1150)]
    e += [Text(0.90 * d, 'kaon radii grow too, but less than pion radii', 700, 885, 46, PINK, mw=1150)]
    e += credit()
    S.append(e)

    # ---------------- 10 summary
    d = D[9]; e = title(0.3, 'Summary')
    rows = [(0.04, GRN, 'BEC of identified pions and kaons in pp, pPb, PbPb'),
            (0.17, YEL, 'R:  1 -> 5 fm,  grows with multiplicity'),
            (0.29, WHITE, 'same multiplicity  ->  nearly the same size'),
            (0.49, BLUE, 'pp, pPb:  source stretched along the beam'),
            (0.57, PINK, 'R shrinks with pair momentum:  expansion')]
    for i, (f, colr, tx) in enumerate(rows):
        y = 180 + i * 108
        T = Text(f * d, tx, 200, y, 56, colr, mw=1620, cps=26)
        e += [T, check(f * d + T.dur + 0.1, 100, y + 78)]
    T = Text(0.70 * d, 'A common freeze-out density in all these collisions', 960, 760, 62, YEL, center=True, mw=1700)
    e += [T, rect(0.70 * d + T.dur, 960 - T.width / 2 - 30, 767, T.width + 60, 115, YEL, 5, 0.8)]
    e += [Text(0.89 * d, 'More particles need more room.', 560, 920, 54, PINK, center=True)]
    e += [Text(0.95 * d, 'Thanks for watching!', 1400, 920, 54, WHITE, center=True)]
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
        outd = os.path.join(WORK, 'preview'); os.makedirs(outd, exist_ok=True)
        for i in ([int(a) for a in sys.argv[2:]] or range(1, NS + 1)):
            n = nfr[i - 1]; f = n - int(0.6 * FPS) - 2
            got = E.render_scene(sc[i - 1], n, board, grain, None, {f})
            got[f].resize((1280, 720), Image.LANCZOS).save(os.path.join(outd, 's%02d.png' % i)); print('preview', i, flush=True)
        return
    out = sys.argv[1]; wavp = os.path.join(WORK, 'narration_all.wav')
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
