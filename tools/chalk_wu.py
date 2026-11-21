# -*- coding: utf-8 -*-
"""Chalkboard video: C. S. Wu's cobalt-60 experiment and the fall of parity conservation.
All drawings are made in chalk; no figures from the paper are used."""
import math, os, random, subprocess, sys, wave
from PIL import Image
import chalk as E
from chalk import Text, Path, Dots, line, arrow, ellipse, rect, curve, check, title, scribble, flat
from chalk import WHITE, YEL, PINK, BLUE, GRN, ORG, W, H, FPS, SR, SPF, PAD

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'wu')
AUD = os.path.join(WORK, 'audio'); NS = 10
sys.path.insert(0, WORK)
from prep import NARR


def boxed(t, T, x, y, h, col=YEL):
    return [T, rect(t + T.dur, x, y, T.width + 40, h, col, 5, 0.7)]


def ball(t, cx, cy, r, up, col=BLUE):
    """A nucleus with a rotation arrow around it; `up` sets the sense of rotation."""
    s = 1 if up else -1
    fn = lambda u: (cx - s * r * 1.3 * math.cos(math.pi * u), cy + r * 0.4 * math.sin(math.pi * u))
    e = [ellipse(t, cx, cy, r, r, col, 6, 0.6), curve(t + 0.6, fn, 0.06, 0.9, 30, WHITE, 4, 0.5)]
    (x0, y0), (x1, y1) = fn(0.84), fn(0.94)
    return e + arrow(t + 1.1, x0, y0, x1, y1, WHITE, 4, 0.1, 18)


def spin(t, cx, cy, r, up, n=150):
    s = 1 if up else -1
    return arrow(t, cx, cy - s * (r + 15), cx, cy - s * (r + n), YEL, 9, 0.4, 26)


def electrons(t, cx, cy, r, col=GRN):
    e = []
    for k, a in enumerate((-0.45, 0.45, -0.95, 0.95)):
        dx, dy = math.sin(a), math.cos(a)
        e += arrow(t + 0.2 * k, cx + dx * (r + 22), cy + dy * (r + 22), cx + dx * (r + 150), cy + dy * (r + 150), col, 5, 0.25, 18)
    return e


def scenes(D):
    S = []

    def at(i, phrase):
        return D[i] * NARR[i].index(phrase) / len(NARR[i])

    # ---------------- 1 title
    A = lambda p: at(0, p); e = []
    e += [Text(0.4, 'The experiment that broke the mirror', 960, 60, 100, YEL, center=True, cps=16, mw=1800)]
    t = A('The world you see')
    e += ball(t, 760, 520, 70, True) + [line(t + 1.2, 960, 300, 960, 760, WHITE, 4, 0.6, dash=True), Text(t + 1.8, 'mirror', 900, 240, 40, WHITE)]
    e += ball(A('Left and right are swapped'), 1160, 520, 70, False)
    e += [Text(A('Left and right are swapped'), 'left  <->  right', 1420, 380, 56, WHITE)]
    e += [Text(A('They called it'), 'conservation\nof parity', 1420, 480, 60, PINK)]
    e += [Text(A('an experiment with radioactive'), 'radioactive cobalt-60', 70, 380, 52, BLUE)]
    e += [Text(A('cooled almost'), 'cooled almost to\nabsolute zero', 70, 470, 52, BLUE)]
    e += [Text(A('in the winter of 1956'), 'winter 1956-57', 70, 640, 48, WHITE)]
    e += [Text(A('showed that nature'), 'nature can tell left from right', 960, 800, 72, ORG, center=True)]
    e += [Text(A('led by'), 'C. S. Wu   (Chien-Shiung Wu)', 960, 920, 60, WHITE, center=True)]
    S.append(e)

    # ---------------- 2 what is parity
    A = lambda p: at(1, p); e = title(0.3, 'What is parity conservation?')
    t = A('Take any experiment')
    e += [rect(t, 110, 255, 380, 215, WHITE, 5, 0.8), Path(t + 0.8, [(220, 295), (220, 420), (330, 420)], YEL, 9, 0.5), Text(t + 1.3, 'experiment', 180, 168, 44, WHITE)]
    t = A('and build its mirror')
    e += [line(t, 600, 200, 600, 640, WHITE, 4, 0.5, dash=True), rect(t + 0.5, 710, 255, 380, 215, WHITE, 5, 0.8)]
    e += [Path(t + 1.3, [(980, 295), (980, 420), (870, 420)], YEL, 9, 0.5), Text(t + 1.8, 'mirror experiment', 730, 168, 44, WHITE)]
    t = A('the mirror experiment gives')
    e += arrow(t, 300, 485, 300, 560, WHITE, 5, 0.2) + arrow(t + 0.3, 900, 485, 900, 560, WHITE, 5, 0.2)
    e += [Text(t + 0.6, 'result', 235, 570, 48, GRN), Text(t + 1.1, 'mirror result', 770, 570, 48, GRN)]
    e += [Text(A('Then no experiment'), 'no experiment can tell the real world from its reflection', 110, 700, 50, PINK, mw=1000)]
    rows = [('Gravity passes', 'gravity', WHITE), ('Electromagnetism passes', 'electromagnetism', WHITE), ('So does the strong', 'strong force', WHITE)]
    for k, (ph, tx, c) in enumerate(rows):
        T = Text(A(ph), tx, 1290, 220 + 95 * k, 56, c)
        e += [T, check(A(ph) + T.dur, 1220, 275 + 95 * k)]
    e += [Text(A('the fourth force'), 'weak force', 1290, 505, 56, YEL), Text(A('which causes beta'), '(beta decay)', 1290, 580, 44, YEL)]
    e += [Text(A('would pass it too'), '?', 1190, 470, 110, PINK, cps=3)]
    e += boxed(A('But nobody had'), Text(A('But nobody had'), 'nobody had actually checked', 1190, 850, 56, YEL), 1170, 858, 105)
    S.append(e)

    # ---------------- 3 tau-theta puzzle
    A = lambda p: at(2, p); e = title(0.3, 'The τ - θ puzzle')
    e += [Text(A('Theta decayed'), 'θ^{+}   ->   π^{+}  +  π^{0}', 100, 190, 66, YEL, cps=10)]
    e += [Text(A('So two pions'), 'two pions:   parity  (-1) × (-1)  =  +1', 100, 290, 46, WHITE)]
    e += [Text(A('Tau decayed'), 'τ^{+}   ->   π^{+}  +  π^{+}  +  π^{-}', 100, 410, 66, BLUE, cps=12)]
    e += [Text(A('and three pions'), 'three pions:   parity  (-1)^{3}  =  -1', 100, 510, 46, WHITE)]
    e += [Text(A('If parity is conserved'), 'parity conserved  ->  two different particles', 100, 640, 48, WHITE)]
    e += [Text(A('But they had exactly'), 'but:   same mass,   same lifetime  !', 100, 730, 58, PINK)]
    t = A('In 1956')
    e += [line(t - 0.5, 1080, 190, 1080, 800, WHITE, 3, 0.5, dash=True), Text(t, 'T. D. Lee  and  C. N. Yang,  1956', 1130, 190, 48, ORG)]
    e += [Text(A('What if it is one'), 'one particle ?', 1130, 290, 54, YEL)]
    e += [Text(A('and the weak force simply'), 'the weak force does not\nconserve parity ?', 1130, 365, 54, YEL)]
    e += [Text(A('found that no experiment'), 'no experiment had ever tested it', 1130, 560, 46, WHITE)]
    e += [Text(A('So they proposed'), '->  they proposed tests', 1130, 640, 46, GRN)]
    T = Text(A('Theta and tau are the same'), 'today:    θ^{+}  =  τ^{+}  =  K^{+}   (the kaon)', 960, 880, 68, GRN, center=True, cps=14)
    e += [T, rect(A('Theta and tau are the same') + T.dur, 960 - T.width / 2 - 30, 888, T.width + 60, 120, GRN, 5, 0.8)]
    S.append(e)

    # ---------------- 4 the idea
    A = lambda p: at(3, p); e = title(0.3, 'How to test mirror symmetry')
    lx, mx, cy, r = 250, 780, 470, 75
    e += ball(A('Take a spinning nucleus'), lx, cy, r, True)
    e += spin(A('Its spin points'), lx, cy, r, True) + [Text(A('Its spin points') + 0.5, 'spin', lx + 30, cy - 230, 44, YEL)]
    e += electrons(A('it sends its electron'), lx, cy, r) + [Text(A('it sends its electron') + 0.8, 'e^{-}', lx - 30, cy + 215, 48, GRN)]
    t = A('Look at this in a mirror')
    e += [line(t, 515, 200, 515, 760, WHITE, 4, 0.6, dash=True), Text(t + 0.6, 'mirror', 455, 765, 40, WHITE)]
    e += ball(A('the nucleus rotates the other'), mx, cy, r, False)
    e += spin(A('so its spin points down'), mx, cy, r, False, 190) + [Text(A('so its spin points down') + 0.5, 'spin', mx + 20, cy + 220, 44, YEL)]
    e += electrons(A('But the electron still'), mx, cy, r)
    e += [Text(A('In the real world'), 'real world', lx - 130, 840, 50, WHITE), Text(A('In the real world') + 1.0, 'e^{-} opposite to spin', lx - 190, 910, 42, GRN)]
    e += [Text(A('In the mirror world'), 'mirror world', mx - 130, 840, 50, WHITE), Text(A('In the mirror world') + 1.0, 'e^{-} along spin', mx - 140, 910, 42, PINK)]
    e += [Text(A('You need something'), 'needed:  something that looks\ndifferent in a mirror', 1080, 185, 46, WHITE)]
    e += [Text(A('The two worlds are different'), 'the two worlds are different !', 1080, 350, 54, PINK)]
    e += [Text(A('Line up the spins'), 'the test:', 1080, 470, 50, YEL), Text(A('Line up the spins') + 0.6, '1.  line up the spins of many nuclei', 1080, 545, 46, WHITE)]
    e += [Text(A('and count the electrons'), '2.  count electrons going up and down', 1080, 615, 46, WHITE)]
    e += [Text(A('If parity is conserved'), 'if parity is conserved:', 1080, 740, 46, WHITE)]
    e += boxed(A('the two numbers must'), Text(A('the two numbers must'), 'N(up)  =  N(down)', 1100, 820, 76, YEL, cps=10), 1080, 830, 125)
    S.append(e)

    # ---------------- 5 cobalt-60
    A = lambda p: at(4, p); e = title(0.3, 'Cobalt-60')
    e += [Text(A('It decays into nickel'), '^{60}Co    ->    ^{60}Ni*   +   e^{-}   +   anti-ν', 960, 175, 76, YEL, center=True, cps=10)]
    e += [Text(A('The nickel then'), 'then    ^{60}Ni*  ->  ^{60}Ni  +  γ  +  γ', 1050, 300, 48, GRN)]
    e += [Text(A('Cobalt 60 has a large'), 'spin 5   (a tiny magnet)', 200, 300, 50, BLUE)]
    rg = random.Random(7)
    t = A('At room temperature')
    e += [rect(t, 110, 430, 400, 270, WHITE, 4, 0.8), Text(t + 0.5, 'warm:  random', 170, 715, 46, WHITE)]
    for k in range(12):
        x, y = 170 + 95 * (k % 4), 480 + 85 * (k // 4); a = rg.uniform(0, 2 * math.pi)
        e += arrow(A('heat shakes') + 0.12 * k, x - 28 * math.cos(a), y - 28 * math.sin(a), x + 28 * math.cos(a), y + 28 * math.sin(a), BLUE, 5, 0.12, 14)
    t = A('To line the spins up')
    e += [rect(t, 620, 430, 400, 270, WHITE, 4, 0.8), Text(t + 0.5, 'very cold + field:  lined up', 600, 715, 46, YEL)]
    for k in range(12):
        x, y = 680 + 95 * (k % 4), 480 + 85 * (k // 4)
        e += arrow(t + 1.0 + 0.1 * k, x, y + 30, x, y - 30, YEL, 5, 0.12, 14)
    e += [Text(A('And a nuclear magnet'), 'a nuclear magnet is very weak', 1130, 440, 46, WHITE)]
    e += [Text(A('you need a strong'), 'needed:', 1130, 520, 46, WHITE)]
    e += boxed(A('and a temperature of about'), Text(A('and a temperature of about'), 'T  ~  0.01 K', 1150, 590, 80, PINK, cps=8), 1130, 600, 130, PINK)
    e += [Text(A('Wu was an expert'), 'C. S. Wu   (Columbia University):   beta decay', 110, 830, 52, YEL)]
    e += [Text(A('she teamed up'), '+   E. Ambler,   R. Hayward,   D. Hoppes,   R. Hudson    (National Bureau of Standards):   the cold', 110, 915, 42, WHITE, mw=1750, cps=34)]
    S.append(e)

    # ---------------- 6 apparatus
    A = lambda p: at(5, p); e = title(0.3, 'The apparatus')
    cx = 580
    t = A('The crystal sat inside')
    e += [rect(t, cx - 150, 300, 300, 590, WHITE, 5, 1.2), Text(t + 1.2, 'cryostat', cx + 170, 300, 42, WHITE)]
    t = A('A thin layer')
    e += [rect(A('a crystal of a special'), cx - 70, 720, 140, 90, BLUE, 5, 0.6), line(t, cx - 66, 716, cx + 66, 716, PINK, 9, 0.4)]
    e += [Text(t + 0.4, 'cobalt-60 layer', 60, 660, 42, PINK)] + arrow(t + 1.2, 380, 700, cx - 80, 714, PINK, 3, 0.3, 12)
    e += [Text(A('a crystal of a special') + 0.6, 'salt crystal\n(cerium magnesium\nnitrate)', 60, 760, 38, BLUE)]
    e += [line(A('a crystal of a special') + 1.6, 400, 790, cx - 78, 775, BLUE, 3, 0.3)]
    e += [Text(A('cooled by liquid helium'), 'liquid helium:   ~ 1 K', 960, 185, 48, BLUE)]
    e += [Text(A('they used a trick'), 'adiabatic demagnetization', 960, 275, 54, YEL)]
    e += [Text(A('First, a strong magnet'), '1.  strong magnet lines up the salt;', 960, 355, 44, WHITE)]
    e += [Text(A('and the helium carries'), 'helium carries the heat away', 1030, 415, 44, WHITE)]
    e += [Text(A('Then the crystal is isolated'), '2.  isolate,  switch the magnet off', 960, 485, 44, WHITE)]
    e += boxed(A('The salt cools itself'), Text(A('The salt cools itself'), '->   T  ≈  0.003 K', 980, 560, 70, PINK, cps=10), 960, 570, 115, PINK)
    t = A('Now a coil applies')
    e += arrow(t, cx + 110, 830, cx + 110, 700, ORG, 6, 0.4, 18) + [Text(t + 0.4, 'B', cx + 90, 630, 46, ORG)]
    e += [Text(t, 'small vertical field  B', 960, 710, 44, ORG)]
    e += [Text(A('and the cobalt spins line up'), '->  cobalt spins line up', 960, 770, 46, YEL)]
    t = A('Just above the cobalt')
    e += [rect(t, cx - 38, 630, 76, 42, GRN, 5, 0.5), Text(t + 0.5, 'scintillator', 100, 560, 42, GRN)] + arrow(t + 1.2, 330, 600, cx - 48, 645, GRN, 3, 0.3, 12)
    e += [Text(t + 0.3, 'scintillator:  a flash for each electron', 960, 850, 44, GRN)]
    t = A('A long plastic rod')
    e += [rect(t, cx - 11, 250, 22, 378, WHITE, 4, 0.9), Text(t + 0.6, 'plastic rod', 130, 400, 42, WHITE)] + arrow(t + 1.3, 350, 435, cx - 20, 450, WHITE, 3, 0.3, 12)
    e += [rect(A('carries the light out'), cx - 60, 180, 120, 68, YEL, 5, 0.6), Text(A('carries the light out') + 0.6, 'light detector', 200, 190, 42, YEL)]
    t = A('Two more counters')
    e += [rect(t, cx + 185, 730, 90, 70, ORG, 5, 0.5), rect(t + 0.5, cx - 55, 930, 110, 70, ORG, 5, 0.5), Text(t + 1.0, 'γ counters', cx + 110, 950, 42, ORG)]
    e += [Text(A('They show how well'), 'γ counters:  how well the spins are lined up', 960, 930, 44, ORG)]
    S.append(e)

    # ---------------- 7 result
    A = lambda p: at(6, p); e = title(0.3, 'The result')
    ox, oy, y1, dy = 190, 900, 590, 170
    t = 0.02 * D[6]
    e += arrow(t, ox, oy, ox + 760, oy, WHITE, 4, 0.5) + arrow(t + 0.5, ox, oy, ox, oy - 660, WHITE, 4, 0.5)
    e += [Text(t + 1.0, 'electron count rate   (warm = 1)', ox + 30, oy - 715, 40, WHITE), Text(t + 2.0, 'time  (minutes)', ox + 470, oy + 10, 40, WHITE)]
    e += [line(t + 2.6, ox, y1, ox + 720, y1, WHITE, 3, 0.5, dash=True), Text(t + 3.0, '1.0', ox - 85, y1 - 30, 40, WHITE)]
    g = lambda u: 1 / (1 + math.exp((u - 0.5) * 11))
    t = A('With the spins pointing away')
    e += [curve(t, lambda u: (ox + 20 + u * 690, y1 - dy * g(u)), 0, 1, 80, PINK, 8, 2.0), Text(t + 0.5, 'spins away from the counter', ox + 40, y1 - dy - 85, 42, PINK)]
    e += [Text(A('about twenty percent higher'), '1.2', ox - 85, y1 - dy - 30, 40, PINK), Text(A('about twenty percent higher'), '+ 20 %', 1040, 330, 66, PINK)]
    t = A('With the spins pointing toward')
    e += [curve(t, lambda u: (ox + 20 + u * 690, y1 + dy * g(u)), 0, 1, 80, BLUE, 8, 2.0), Text(t + 0.5, 'spins toward the counter', ox + 40, y1 + dy + 25, 42, BLUE)]
    e += [Text(A('about twenty percent lower'), '0.8', ox - 85, y1 + dy - 30, 40, BLUE), Text(A('about twenty percent lower'), '- 20 %', 1400, 330, 66, BLUE)]
    e += [Text(A('If parity is conserved'), 'if parity is conserved:\nthe counter should not care', 1040, 180, 46, WHITE)]
    e += [Text(A('Electrons prefer'), 'electrons prefer to leave\nopposite to the nuclear spin', 1040, 440, 50, YEL)]
    e += [Text(A('The crystal slowly warms'), 'the crystal warms up  (minutes):', 1040, 610, 44, WHITE)]
    e += [Text(A('and the two count rates'), 'the two rates drift back together', 1040, 668, 44, GRN), Text(A('and the two count rates') + 1.0, 'warm', ox + 610, y1 - 65, 40, WHITE)]
    e += [Text(A('The effect follows'), 'the effect follows the polarization', 1040, 726, 44, GRN)]
    T = Text(A('Parity is not conserved'), 'Parity is NOT conserved\nin beta decay', 1070, 815, 62, YEL, cps=34)
    e += [T, rect(A('Parity is not conserved') + T.dur, 1040, 825, 760, 190, YEL, 5, 0.5)]
    S.append(e)

    # ---------------- 8 handedness
    A = lambda p: at(7, p); e = title(0.3, 'Why?   Handedness')

    def hand(t, y, right, lab, col):
        out = [Text(t, lab, 80, y, 50, col), Dots(t + 0.6, [(470, y + 45)], WHITE, 12, 0.2)]
        out += arrow(t + 0.8, 495, y + 45, 760, y + 45, WHITE, 4, 0.4, 18)
        out += arrow(t + 1.3, 560, y + 5, 680, y + 5, col, 10, 0.3, 24) if right else arrow(t + 1.3, 680, y + 5, 560, y + 5, col, 10, 0.3, 24)
        return out

    e += hand(A('If it spins like a right'), 200, True, 'right-handed:', PINK)
    e += hand(A('If it spins the other'), 330, False, 'left-handed:', GRN)
    e += [Text(A('Think of a particle'), 'thin arrow = motion,   thick arrow = spin', 80, 440, 38, WHITE)]
    e += [Text(A('The weak force acts'), 'the weak force acts on:', 80, 540, 48, WHITE), Text(A('The weak force acts') + 1.2, 'left-handed particles', 120, 610, 52, GRN)]
    e += [Text(A('and on right handed anti'), 'right-handed antiparticles', 120, 685, 52, PINK)]
    nx, ny = 1330, 560
    t = A('In cobalt decay')
    e += [ellipse(t, nx, ny, 62, 62, BLUE, 6, 0.6), Text(t + 0.5, 'Co', nx - 32, ny - 38, 50, BLUE)]
    e += arrow(t + 1.0, nx - 130, ny + 75, nx - 130, ny - 75, YEL, 10, 0.4, 26) + [Text(t + 1.5, 'spin\n5 -> 4', nx - 320, ny - 60, 46, YEL)]
    t = A('The antineutrino is right')
    e += arrow(t + 0.6, nx, ny - 85, nx, ny - 330, WHITE, 4, 0.5, 18) + arrow(A('so both of their spins'), nx + 50, ny - 150, nx + 50, ny - 260, PINK, 10, 0.3, 24)
    e += [Text(t, 'anti-ν :  right-handed', nx + 110, ny - 300, 46, PINK), Text(A('so it flies off along'), 'flies along the spin', nx + 110, ny - 235, 42, WHITE)]
    t = A('The electron is left')
    e += arrow(t + 0.6, nx, ny + 85, nx, ny + 330, WHITE, 4, 0.5, 18) + arrow(A('so both of their spins') + 0.6, nx + 50, ny + 260, nx + 50, ny + 150, GRN, 10, 0.3, 24)
    e += [Text(t, 'e^{-} :  left-handed', nx + 110, ny + 150, 46, GRN), Text(A('so it flies the opposite'), 'flies opposite to the spin', nx + 110, ny + 215, 42, WHITE)]
    T = Text(A('That is exactly'), 'exactly what Wu saw', 80, 810, 52, YEL)
    e += [T, check(A('That is exactly') + T.dur, 120 + T.width, 860)]
    e += boxed(A('It is as large'), Text(A('And the violation'), 'parity violation is maximal', 100, 920, 58, ORG), 80, 928, 108, ORG)
    S.append(e)

    # ---------------- 9 aftermath
    A = lambda p: at(8, p); e = title(0.3, 'Aftermath')
    e += [Text(A('Within days'), 'within days:   Garwin,  Lederman,  Weinrich  confirm it', 90, 190, 50, YEL)]
    e += [Text(A('using the decays'), 'with decays of pions and muons', 190, 258, 42, WHITE)]
    e += [Text(A('Both papers'), 'both papers:   Physical Review 105,   February 1957', 90, 345, 46, BLUE)]
    e += [Text(A('Wolfgang Pauli'), 'Pauli was ready to bet that nothing would be found', 90, 430, 46, WHITE)]
    e += [Text(A('That same year'), '1957:   Nobel Prize to Lee and Yang', 90, 530, 54, GRN)]
    e += [Text(A('Wu did not share'), 'Wu was not included', 190, 603, 46, PINK)]
    e += [Text(A('She later received'), '1978:   Wu receives the first Wolf Prize in Physics', 90, 690, 50, YEL)]
    e += [Text(A('The experiment also showed'), 'also broken:   C   (matter  <->  antimatter)', 90, 800, 50, WHITE)]
    e += [Text(A('For a while'), 'C P  seemed safe ...', 90, 880, 50, WHITE)]
    e += [Text(A('But in 1964'), '... until 1964:   C P  is broken too  (a little)', 720, 880, 50, ORG)]
    S.append(e)

    # ---------------- 10 summary
    A = lambda p: at(9, p); e = title(0.3, 'Summary')
    rows = [('Parity conservation says', WHITE, 'parity conservation:   the mirror image of an experiment is also possible'),
            ('A puzzle with two', BLUE, 'τ - θ puzzle   ->   Lee and Yang doubt it for the weak force'),
            ('Wu and her colleagues', YEL, 'Wu et al.:   polarized ^{60}Co  at  ~ 0.003 K'),
            ('More electrons came', GRN, 'more electrons leave opposite to the nuclear spin'),
            ('So the mirror world', PINK, 'the mirror world is different from ours')]
    for i, (ph, colr, tx) in enumerate(rows):
        y = 185 + i * 105
        T = Text(A(ph), tx, 200, y, 52, colr, mw=1660, cps=26)
        e += [T, check(A(ph) + T.dur + 0.1, 100, y + 72)]
    T = Text(A('The weak force knows'), 'The weak force knows left from right', 960, 760, 76, YEL, center=True, cps=14)
    e += [T, rect(A('The weak force knows') + T.dur, 960 - T.width / 2 - 30, 772, T.width + 60, 125, YEL, 5, 0.8)]
    e += [Text(A('Thanks for'), 'Thanks for watching!', 960, 950, 54, WHITE, center=True)]
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
