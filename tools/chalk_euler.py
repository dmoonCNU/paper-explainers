# -*- coding: utf-8 -*-
"""Chalkboard video: Euler's equations for a rotating rigid body (classical mechanics, no paper figures)."""
import math, os, subprocess, sys, wave
from PIL import Image
import chalk as E
from chalk import Text, Path, line, arrow, ellipse, rect, curve, check, title, flat
from chalk import WHITE, YEL, PINK, BLUE, GRN, ORG, W, H, FPS, SR, SPF, PAD

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'euler')
AUD = os.path.join(WORK, 'audio'); NS = 9
sys.path.insert(0, WORK)
from prep import NARR


def racket(t, cx, cy, col=WHITE):
    e = [ellipse(t, cx, cy, 150, 105, col, 7, 0.9)]
    for i, dx in enumerate((-75, 0, 75)):
        h = 100 * math.sqrt(1 - (dx / 150.0) ** 2)
        e += [line(t + 1.0 + 0.1 * i, cx + dx, cy - h, cx + dx, cy + h, col, 2, 0.12)]
    for i, dy in enumerate((-50, 0, 50)):
        h = 145 * math.sqrt(1 - (dy / 105.0) ** 2)
        e += [line(t + 1.3 + 0.1 * i, cx - h, cy + dy, cx + h, cy + dy, col, 2, 0.12)]
    e += [line(t + 1.7, cx + 150, cy, cx + 430, cy, col, 14, 0.5)]
    return e


def axis1(t, cx, cy): return [line(t, cx - 230, cy, cx + 540, cy, GRN, 4, 0.6, dash=True), Text(t + 0.6, '1', cx + 555, cy - 45, 60, GRN)]
def axis2(t, cx, cy): return [line(t, cx + 110, cy + 210, cx + 110, cy - 210, PINK, 4, 0.6, dash=True), Text(t + 0.6, '2', cx + 95, cy - 290, 60, PINK)]
def axis3(t, cx, cy): return arrow(t, cx + 110, cy, cx - 10, cy + 150, BLUE, 6, 0.5) + [Text(t + 0.5, '3', cx - 55, cy + 135, 60, BLUE)]


def scenes(D):
    S = []

    def at(i, phrase):
        return D[i] * NARR[i].index(phrase) / len(NARR[i])

    # ---------------- 1 title
    A = lambda p: at(0, p); e = []
    e += [Text(0.4, 'Why does a tossed racket flip?', 960, 70, 104, YEL, center=True, cps=16, mw=1750)]
    cx, cy = 330, 560
    e += racket(A('toss it'), cx, cy)
    e += axis1(A('Spin it about its handle'), cx, cy) + [Text(A('Spin it about its handle') + 0.5, 'about the handle:  smooth', 1010, 300, 54, GRN)]
    e += axis3(A('Spin it flat'), cx, cy) + [Text(A('Spin it flat') + 0.5, 'flat, like a frisbee:  smooth', 1010, 385, 54, BLUE)]
    e += axis2(A('But flip it'), cx, cy) + [Text(A('But flip it') + 0.5, 'end over end:', 1010, 470, 54, PINK)]
    e += [Text(A('It always adds'), 'always a half twist!', 1340, 470, 54, PINK)]
    e += [Text(A('three short equations'), "Euler's equations", 1400, 600, 124, YEL, center=True, cps=12, mw=880)]
    e += [Text(A('They are Euler'), 'for a rotating rigid body', 1400, 790, 62, WHITE, center=True)]
    e += [Text(A('written down by'), 'Leonhard Euler,  250+ years ago', 1400, 900, 44, BLUE, center=True)]
    S.append(e)

    # ---------------- 2 starting point
    d = D[1]; A = lambda p: at(1, p); e = title(0.3, 'The starting point')
    e += [Text(A('force equals'), 'F  =  dp / dt', 90, 190, 64, WHITE, cps=14)]
    T = Text(A('Torque equals'), 'τ  =  dL / dt', 90, 300, 76, YEL, cps=12)
    e += [T, rect(A('Torque equals') + T.dur, 70, 310, T.width + 40, 130, YEL, 5, 0.7)]
    t = A('For a wheel')
    e += [ellipse(t, 250, 660, 45, 130, BLUE, 7, 0.8), line(t + 0.8, 90, 660, 470, 660, WHITE, 5, 0.4)]
    e += arrow(t + 1.3, 470, 660, 610, 660, YEL, 7, 0.4) + [Text(t + 1.6, 'ω', 630, 610, 60, YEL)]
    e += [Text(t + 0.4, 'wheel on an axle', 110, 820, 44, BLUE)]
    e += [Text(A('L is just'), 'L  =  I ω', 180, 890, 76, GRN, cps=10)]
    e += [line(A('But a freely') - 0.3, 800, 190, 800, 1000, WHITE, 3, 0.6, dash=True)]
    e += [Text(A('But a freely'), 'a freely tumbling body ...', 880, 190, 58, PINK)]
    t = A('In general, L')
    e += arrow(t, 930, 480, 1130, 330, YEL, 7, 0.4) + [Text(t + 0.3, 'ω', 1140, 285, 56, YEL)]
    e += arrow(t + 0.8, 930, 480, 1230, 440, GRN, 7, 0.4) + [Text(t + 1.1, 'L', 1240, 395, 56, GRN)]
    e += [Text(t + 1.5, 'L is not parallel to ω', 1330, 345, 50, WHITE, mw=540)]
    e += [Text(A('The moment of inertia is not'), 'I is not one number:', 900, 560, 52, WHITE)]
    e += [Text(A('it depends on the axis'), 'it depends on the axis', 900, 630, 52, ORG)]
    e += [Text(A('And, seen from the room'), 'seen from the room,', 900, 740, 52, WHITE)]
    e += [Text(A('so its inertia keeps'), 'I keeps changing with time', 900, 810, 52, ORG)]
    e += [Text(A('That makes'), '->  messy!', 1400, 910, 70, PINK)]
    S.append(e)

    # ---------------- 3 principal axes
    d = D[2]; A = lambda p: at(2, p); e = title(0.3, 'Idea 1:  principal axes      Idea 2:  body frame')
    cx, cy = 290, 520
    e += racket(A('every rigid body'), cx, cy)
    t = A('has three special')
    e += axis1(t, cx, cy) + axis2(t + 0.8, cx, cy) + axis3(t + 1.6, cx, cy)
    e += [Text(t + 0.3, '3 special perpendicular axes', 950, 185, 54, WHITE)]
    e += [Text(A('If the body spins'), 'spin about one of them:   L  parallel to  ω', 950, 262, 50, GRN, mw=930)]
    e += [Text(A('Each axis has'), 'moments of inertia:   I_{1},  I_{2},  I_{3}', 950, 350, 54, YEL, mw=930)]
    e += [Text(A('the smallest is'), 'I_{1}  smallest  (handle)', 950, 440, 48, GRN)]
    e += [Text(A('The largest is'), 'I_{3}  largest  (through the strings)', 950, 505, 48, BLUE)]
    e += [Text(A('And the third is'), 'I_{2}  in between', 950, 570, 48, PINK)]
    T = Text(A('Its three components'), 'L  =  ( I_{1}ω_{1} ,  I_{2}ω_{2} ,  I_{3}ω_{3} )', 950, 670, 66, YEL, mw=900, cps=12)
    e += [T, rect(A('Its three components') + T.dur, 930, 678, T.width + 40, 122, YEL, 5, 0.7)]
    e += [Text(A('The second idea'), 'axes glued to the body  =  "body frame"', 120, 850, 56, WHITE)]
    T = Text(A('In this body frame'), 'I_{1},  I_{2},  I_{3}   never change', 120, 935, 60, GRN)
    e += [T, check(A('In this body frame') + T.dur, 150 + T.width, 990)]
    S.append(e)

    # ---------------- 4 rotating frame
    d = D[3]; A = lambda p: at(3, p); e = title(0.3, 'The price of a rotating frame')
    e += [Text(A('The body frame is rotating'), "body frame rotates;  Newton's laws need a frame that does not", 80, 180, 46, WHITE, mw=1760)]
    ox, oy = 300, 900
    t = A('Picture a vector')
    e += arrow(t - 1.5, ox, oy, ox, 330, YEL, 7, 0.5) + [Text(t - 1.0, 'ω', ox - 70, 300, 60, YEL)]
    e += arrow(t, ox, oy, ox + 170, 544, WHITE, 8, 0.5) + [Text(t + 0.5, 'A', ox + 200, 540, 60, WHITE)]
    t = A('it is swept around')
    e += [ellipse(t, ox, 500, 240, 62, BLUE, 4, 1.0, dash=True)]
    e += arrow(A('its tip moves'), ox + 170, 544, ox + 50, 572, PINK, 7, 0.4) + [Text(A('its tip moves') + 0.4, 'ω × A', ox - 200, 585, 54, PINK)]
    e += [Text(A('So, for any vector'), 'for any vector A :', 760, 290, 50, WHITE)]
    e += [Text(A('the rate of change seen from the room'), '(dA/dt)_{room}', 760, 370, 64, BLUE, cps=12)]
    e += [Text(A('equals the rate of change seen from the body'), '=  (dA/dt)_{body}', 1150, 370, 64, GRN, cps=12)]
    e += [Text(A('plus omega cross the vector'), '+  ω × A', 1600, 370, 64, PINK, cps=10)]
    T = Text(A('The torque equals'), 'τ  =  (dL/dt)_{body}  +  ω × L', 780, 560, 80, YEL, cps=10, mw=1050)
    e += [T, rect(A('The torque equals') + T.dur, 760, 572, T.width + 40, 140, YEL, 5, 0.8)]
    e += [Text(A('This extra term'), 'the extra term  ω × L  is the whole story', 780, 780, 52, PINK, mw=1080)]
    e += [Text(A('It is a close relative'), 'a relative of the centrifugal and Coriolis forces', 780, 880, 46, WHITE, mw=1080)]
    S.append(e)

    # ---------------- 5 the equations
    d = D[4]; A = lambda p: at(4, p); e = title(0.3, "Euler's equations")
    e += [Text(A('I one, times'), 'I_{1} dω_{1}/dt', 90, 200, 70, GRN, cps=8)]
    e += [Text(A('minus, I two'), '-  (I_{2} - I_{3}) ω_{2}ω_{3}', 500, 200, 70, PINK, cps=9)]
    e += [Text(A('equals the torque about'), '=  τ_{1}', 1130, 200, 70, YEL, cps=8)]
    t = A('The other two')
    e += [Text(t, 'I_{2} dω_{2}/dt', 90, 345, 70, GRN, cps=20), Text(t + 0.8, '-  (I_{3} - I_{1}) ω_{3}ω_{1}', 500, 345, 70, PINK, cps=22), Text(t + 2.0, '=  τ_{2}', 1130, 345, 70, YEL, cps=20)]
    t = A('One goes to two')
    e += [Text(t, 'I_{3} dω_{3}/dt', 90, 490, 70, GRN, cps=20), Text(t + 0.8, '-  (I_{1} - I_{2}) ω_{1}ω_{2}', 500, 490, 70, PINK, cps=22), Text(t + 2.0, '=  τ_{3}', 1130, 490, 70, YEL, cps=20)]
    t = A('Just rotate the labels')
    e += [Text(t, '1', 1625, 215, 70, WHITE), Text(t + 0.3, '2', 1775, 455, 70, WHITE), Text(t + 0.6, '3', 1475, 455, 70, WHITE)]
    e += arrow(t + 0.9, 1680, 300, 1770, 440, ORG, 5, 0.3) + arrow(t + 1.3, 1750, 510, 1540, 510, ORG, 5, 0.3) + arrow(t + 1.7, 1510, 440, 1610, 300, ORG, 5, 0.3)
    e += [rect(A('These are Euler'), 60, 190, 1310, 440, WHITE, 4, 1.0)]
    e += [Text(A('The first term'), '1st term:  inertia × angular acceleration   (familiar)', 90, 690, 50, GRN, mw=1700)]
    e += [Text(A('The second term'), '2nd term:  mixes the other two axes', 90, 775, 50, PINK)]
    e += [Text(A('and it is only there'), '(only if their moments differ)', 1000, 778, 46, WHITE)]
    T = Text(A('It means that'), 'rotation about one axis can change with NO torque', 960, 885, 60, YEL, center=True, mw=1700)
    e += [T, rect(A('It means that') + T.dur, 960 - T.width / 2 - 30, 893, T.width + 60, 112, YEL, 5, 0.8)]
    S.append(e)

    # ---------------- 6 checks
    d = D[5]; A = lambda p: at(5, p); e = title(0.3, 'Three quick checks')
    e += [Text(A('Check one'), '1)  one principal axis only:   ω_{2} = ω_{3} = 0', 90, 190, 54, WHITE)]
    T = Text(A('and we get back'), '->   I_{1} dω_{1}/dt  =  τ_{1}      (wheel on an axle)', 180, 275, 54, GRN)
    e += [T, check(A('and we get back') + T.dur, 210 + T.width, 325)]
    e += [Text(A('Check two'), '2)  sphere, no torque:   I_{1} = I_{2} = I_{3}', 90, 400, 54, WHITE)]
    T = Text(A('and omega stays'), '->   ω  =  constant', 180, 485, 54, GRN)
    e += [T, check(A('and omega stays') + T.dur, 210 + T.width, 535)]
    e += [Text(A('Check three'), '3)  any body, no torque, spin exactly about a principal axis', 90, 610, 54, WHITE, mw=1740)]
    T = Text(A('Again, nothing'), '->   nothing changes', 180, 695, 54, GRN)
    e += [T, check(A('Again, nothing') + T.dur, 210 + T.width, 745)]
    e += [Text(A('So steady rotation'), 'steady rotation about each principal axis is always a solution', 90, 800, 46, BLUE, mw=1740)]
    T = Text(A('The real question'), 'What if the spin is slightly off?', 960, 900, 70, YEL, center=True)
    e += [T, rect(A('The real question') + T.dur, 960 - T.width / 2 - 30, 908, T.width + 60, 120, YEL, 5, 0.8)]
    S.append(e)

    # ---------------- 7 symmetric body
    d = D[6]; A = lambda p: at(6, p); e = title(0.3, 'Symmetric body:   I_{1} = I_{2}')
    cx, cy = 330, 600
    t = A('take a symmetric')
    e += [ellipse(t, cx, cy, 235, 195, BLUE, 7, 1.0), line(t + 1.1, cx, cy + 290, cx, cy - 330, WHITE, 3, 0.6, dash=True), Text(t + 1.7, '3', cx + 25, cy + 235, 54, WHITE)]
    t = A('So the rotation vector')
    e += arrow(t, cx, cy, cx + 75, cy - 300, YEL, 7, 0.5) + [Text(t + 0.4, 'ω', cx + 95, cy - 350, 60, YEL)]
    e += [ellipse(t + 1.0, cx, cy - 300, 75, 20, PINK, 4, 1.0, dash=True), Text(t + 2.0, 'wobble', cx + 110, cy - 265, 44, PINK)]
    e += [Text(A('With no torque'), 'no torque', 760, 180, 50, WHITE)]
    e += [Text(A('the third equation'), 'ω_{3}  =  constant', 1050, 175, 58, GRN)]
    e += [Text(A('The first two say'), 'dω_{1}/dt  =  - Ω ω_{2}', 760, 270, 58, WHITE, cps=14)]
    e += [Text(A('chase each other'), 'dω_{2}/dt  =  + Ω ω_{1}', 760, 355, 58, WHITE, cps=14)]
    T = Text(A('at a rate capital'), 'Ω  =  (I_{3} - I_{1}) / I_{1}  ·  ω_{3}', 780, 470, 66, YEL, cps=10)
    e += [T, rect(A('at a rate capital') + T.dur, 760, 478, T.width + 40, 122, YEL, 5, 0.7)]
    e += [Text(A('The spin is slightly off'), 'slightly off stays slightly off:  a steady wobble', 760, 640, 48, PINK, mw=1100)]
    e += [Text(A('The Earth is slightly'), 'Earth  (slightly flattened)', 760, 740, 52, BLUE)]
    e += [Text(A('Euler predicted'), 'Euler predicted:   305 days', 760, 815, 54, WHITE)]
    e += [Text(A('Such a wobble'), 'observed (Chandler wobble):   433 days', 760, 890, 54, GRN)]
    e += [Text(A('It is longer'), 'the Earth is not perfectly rigid', 760, 965, 46, ORG)]
    S.append(e)

    # ---------------- 8 tennis racket theorem
    d = D[7]; A = lambda p: at(7, p); e = title(0.3, 'The tennis racket theorem')
    e += [Text(A('with three different'), 'I_{1}  <  I_{2}  <  I_{3}', 90, 185, 64, WHITE, cps=10)]
    e += [Text(A('Spin it mostly'), 'spin about one axis  +  a tiny wobble  ε', 760, 195, 52, BLUE, mw=1100)]
    T = Text(A('its second derivative'), 'd^{2}ε / dt^{2}  =  k ε', 960, 290, 80, YEL, center=True, cps=8)
    e += [T, rect(A('its second derivative') + T.dur, 960 - T.width / 2 - 30, 302, T.width + 60, 135, YEL, 5, 0.7)]
    # stable
    ox, oy = 110, 660
    t = A('For the axis with')
    e += [Text(t, 'smallest or largest  I :    k < 0', 90, 470, 52, GRN, mw=800)]
    e += arrow(t + 2.5, ox, oy, ox + 640, oy, WHITE, 4, 0.5) + [Text(t + 3.0, 't', ox + 650, oy - 25, 44, WHITE)]
    e += [curve(A('The wobble just oscillates'), lambda u: (ox + u * 600, oy - 70 * math.sin(u * 6 * math.pi)), 0, 1, 120, GRN, 7, 2.0)]
    e += [Text(A('That is the equation'), 'like a mass on a spring', 130, 760, 46, WHITE)]
    T = Text(A('The rotation is stable'), 'STABLE', 250, 835, 72, GRN)
    e += [T, check(A('The rotation is stable') + T.dur, 280 + T.width, 905)]
    # unstable
    ox, oy = 1010, 730
    t = A('But for the middle')
    e += [line(t - 0.5, 900, 470, 900, 920, WHITE, 3, 0.5, dash=True)]
    e += [Text(t, 'middle axis  (I_{2}) :    k > 0', 990, 470, 52, PINK, mw=850)]
    e += arrow(t + 1.2, ox, oy, ox + 640, oy, WHITE, 4, 0.5) + [Text(t + 1.6, 't', ox + 650, oy - 25, 44, WHITE)]
    e += [curve(A('The wobble grows'), lambda u: (ox + u * 560, oy - 6 * math.exp(u * 3.4)), 0, 1, 100, PINK, 7, 1.6)]
    e += [Text(A('The wobble grows') + 0.6, 'grows exponentially', 1050, 580, 46, WHITE)]
    e += [Text(A('The rotation is unstable'), 'UNSTABLE:  it flips!', 1100, 835, 72, PINK)]
    e += [Text(A('This is the tennis'), 'k  =  (I_{2}-I_{1})(I_{3}-I_{2}) ω_{2}^{2} / (I_{1}I_{3})  >  0', 90, 950, 50, YEL, cps=30)]
    e += [Text(A('In space'), 'in space:  the Dzhanibekov effect', 1150, 955, 46, BLUE, mw=720)]
    S.append(e)

    # ---------------- 9 summary
    d = D[8]; A = lambda p: at(8, p); e = title(0.3, 'Summary')
    rows = [('Torque equals', YEL, 'τ  =  dL / dt'),
            ('For a tumbling body', GRN, 'principal axes, glued to the body:   I_{1}, I_{2}, I_{3}  constant'),
            ('The rotating frame adds', PINK, 'rotating frame adds   ω × L'),
            ('A symmetric body', BLUE, 'symmetric body:  a steady wobble  (the Earth)'),
            ('And a body with three', ORG, 'smallest, largest axis:  stable.    middle axis:  it flips')]
    for i, (ph, colr, tx) in enumerate(rows):
        y = 180 + i * 100
        T = Text(A(ph), tx, 200, y, 54, colr, mw=1640, cps=26)
        e += [T, check(A(ph) + T.dur + 0.1, 100, y + 75)]
    T = Text(A('they give Euler'), 'I_{1} dω_{1}/dt  -  (I_{2} - I_{3}) ω_{2}ω_{3}  =  τ_{1}     ( + two more )', 960, 700, 60, YEL, center=True, mw=1700, cps=26)
    e += [T, rect(A('they give Euler') + T.dur, 960 - T.width / 2 - 30, 708, T.width + 60, 115, YEL, 5, 0.8)]
    e += [Text(A('The same equations'), 'used today for satellites and spacecraft', 960, 845, 48, WHITE, center=True)]
    e += [Text(A('blame Euler'), 'Phone twists in the air?  Blame Euler.', 600, 940, 52, PINK, center=True)]
    e += [Text(A('Thanks for'), 'Thanks for watching!', 1450, 940, 54, WHITE, center=True)]
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
