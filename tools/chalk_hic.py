# -*- coding: utf-8 -*-
"""Chalkboard video: "Heavy Ion Collisions: The Big Picture, and the Big Questions" (arXiv:1802.04801).
All drawings are made in chalk; no figures from the paper are used."""
import math, os, random, subprocess, sys, wave
from PIL import Image
import chalk as E
from chalk import Text, Path, Dots, line, arrow, ellipse, rect, curve, check, title, scribble, flat
from chalk import WHITE, YEL, PINK, BLUE, GRN, ORG, W, H, FPS, SR, SPF, PAD

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'hic')
AUD = os.path.join(WORK, 'audio'); NS = 10
sys.path.insert(0, WORK)
from prep import NARR


def cloud(seed, cx, cy, r, n):
    rg = random.Random(seed); pts = []
    while len(pts) < n:
        x, y = rg.uniform(-r, r), rg.uniform(-r, r)
        if x * x + y * y < r * r: pts.append((cx + x, cy + y))
    return pts


def boxed(t, T, x, y, h, col=YEL):
    return [T, rect(t + T.dur, x, y, T.width + 40, h, col, 5, 0.7)]


def scenes(D):
    S = []

    def at(i, phrase):
        return D[i] * NARR[i].index(phrase) / len(NARR[i])

    # ---------------- 1 title
    A = lambda p: at(0, p); e = []
    e += [Text(0.4, 'The hottest liquid on Earth', 960, 70, 112, YEL, center=True, cps=16, mw=1750)]
    t = A('when two heavy nuclei')
    e += [ellipse(t, 330, 500, 16, 115, BLUE, 7, 0.5), ellipse(t + 0.5, 790, 500, 16, 115, BLUE, 7, 0.5)]
    e += arrow(t + 1.0, 365, 500, 500, 500) + arrow(t + 1.4, 755, 500, 620, 500)
    e += [Text(t + 1.8, 'Pb', 295, 630, 54, BLUE), Text(t + 2.1, 'Pb', 755, 630, 54, BLUE)]
    e += [Text(A('at almost the speed'), 'almost the speed of light', 560, 720, 46, WHITE, center=True)]
    t = A('they create a tiny droplet')
    e += [scribble(t, 1400, 400, 75, ORG, 1.0), Text(t + 1.0, 'a droplet of quark-gluon plasma', 1400, 520, 56, ORG, center=True)]
    e += [Text(A('at a temperature'), 'a few trillion degrees', 1400, 620, 62, PINK, center=True)]
    e += [Text(A('This video follows'), 'based on the review by   W. Busza,   K. Rajagopal,   W. van der Schee', 960, 810, 44, WHITE, center=True, cps=40)]
    e += [Text(A('Its title is'), '"Heavy Ion Collisions:  The Big Picture, and the Big Questions"', 960, 880, 52, BLUE, center=True, mw=1750, cps=30)]
    e += [Text(A('Its title is') + 2.5, 'Annu. Rev. Nucl. Part. Sci. 68 (2018),   arXiv:1802.04801', 960, 965, 36, WHITE, center=True, cps=60)]
    S.append(e)

    # ---------------- 2 one collision
    A = lambda p: at(1, p); e = title(0.3, 'One collision, step by step')
    t = A('each nucleus is flattened')
    e += [ellipse(t, 230, 330, 16, 115, BLUE, 7, 0.5), ellipse(t + 0.5, 650, 330, 16, 115, BLUE, 7, 0.5)]
    e += arrow(t + 1.0, 265, 330, 390, 330) + arrow(t + 1.4, 615, 330, 490, 330)
    t = A('A lead nucleus is about')
    e += [line(t, 120, 215, 120, 445, WHITE, 3, 0.4), line(t + 0.4, 100, 215, 140, 215, WHITE, 3, 0.1), line(t + 0.5, 100, 445, 140, 445, WHITE, 3, 0.1)]
    e += [Text(t + 0.6, '14\nfm', 40, 280, 44, WHITE)]
    e += [Text(A('its thickness is squeezed'), 'thickness:   14 fm / 2500   (LHC)', 200, 470, 44, BLUE)]
    t = A('The two discs pass')
    e += [ellipse(t, 150, 760, 16, 115, BLUE, 7, 0.5), ellipse(t + 0.4, 730, 760, 16, 115, BLUE, 7, 0.5)]
    e += arrow(t + 0.8, 120, 760, 50, 760, WHITE, 5, 0.3) + arrow(t + 1.1, 760, 760, 830, 760, WHITE, 5, 0.3)
    t = A('they leave behind')
    e += [scribble(t, 440, 760, 95, ORG, 0.9), scribble(t + 0.9, 300, 760, 70, ORG, 0.6), scribble(t + 1.5, 580, 760, 70, ORG, 0.6)]
    e += [Text(t + 2.1, 'a region filled with energy', 210, 900, 44, ORG)]
    e += [Text(A('A very short time later'), 'after  1 fm/c   (light travels 1 fm) :', 920, 190, 46, WHITE)]
    e += boxed(A('the energy density there'), Text(A('the energy density there'), 'energy density  ≈  12 GeV / fm^{3}', 940, 280, 62, YEL, cps=14), 920, 288, 118)
    e += [Text(A('That is about twenty'), '≈  20 ×   inside a hadron  (a proton)', 920, 440, 52, PINK)]
    e += [Text(A('So this matter cannot'), 'not separate protons and neutrons', 920, 560, 50, WHITE)]
    e += [Text(A('It is made of their'), '->   quarks and gluons', 920, 640, 64, GRN)]
    e += [Text(A('In the end'), 'up to  30,000 particles  from one collision', 920, 800, 52, BLUE, mw=950)]
    S.append(e)

    # ---------------- 3 early universe
    A = lambda p: at(2, p); e = title(0.3, 'Why?    1.  The early universe')
    t = A('The first reason')
    e += arrow(t, 90, 255, 1830, 255, WHITE, 5, 0.9) + [Text(t + 0.3, 'Big Bang', 80, 180, 42, YEL), Text(t + 1.2, 'time', 1760, 185, 40, WHITE)]
    t = A('A few microseconds')
    e += [line(t, 420, 235, 420, 275, WHITE, 4, 0.1), Text(t + 0.2, 'a few microseconds', 445, 180, 42, WHITE), Text(A('all of space'), 'quark-gluon plasma', 300, 275, 48, ORG)]
    t = A('As the universe cooled')
    e += [line(t, 1050, 235, 1050, 275, WHITE, 4, 0.1), Text(t + 1.0, 'protons, neutrons', 900, 275, 48, GRN), Text(t + 3.0, 'us', 1640, 275, 48, WHITE)]
    ox, oy = 170, 930
    t = A('Calculations on supercomputers')
    e += arrow(t, ox, oy, ox + 660, oy, WHITE, 4, 0.4) + arrow(t + 0.5, ox, oy, ox, oy - 420, WHITE, 4, 0.4)
    e += [Text(t + 1.0, 'T', ox + 670, oy - 30, 46, WHITE), Text(t + 1.2, 'energy density / T^{4}', ox + 20, oy - 480, 38, WHITE), Text(t + 2.0, 'lattice QCD', ox + 330, oy - 130, 46, BLUE)]
    fn = lambda u: (ox + u * 620, oy - 50 - 280 / (1 + math.exp(-(u - 0.38) * 14)))
    t = A('It was a smooth crossover')
    e += [curve(t, fn, 0, 1, 80, YEL, 8, 1.6), line(t + 1.7, ox + 236, oy, ox + 236, oy - 380, PINK, 3, 0.4, dash=True)]
    e += [Text(A('at a temperature of about 150'), '150 MeV', ox + 160, oy + 5, 42, PINK), Text(t + 2.2, 'hadrons', ox + 20, oy - 150, 40, GRN), Text(t + 2.6, 'QGP', ox + 420, oy - 420, 46, ORG)]
    e += [Text(A('show that this change'), 'not a sharp transition  (like water freezing)', 960, 410, 46, WHITE, mw=900)]
    e += [Text(A('It was a smooth crossover'), 'a smooth crossover  at  T ≈ 150 MeV', 960, 490, 52, YEL, mw=900)]
    e += [Text(A('And a smooth crossover leaves'), 'leaves no trace for telescopes today', 960, 600, 48, PINK, mw=900)]
    e += [Text(A('So, to study'), 'so we have to recreate it', 960, 690, 48, WHITE)]
    e += boxed(A('Heavy ion collisions are'), Text(A('Heavy ion collisions are'), 'heavy ion collisions  =  "little bangs"', 980, 820, 60, YEL, mw=860), 960, 828, 112)
    S.append(e)

    # ---------------- 4 liquid
    A = lambda p: at(3, p); e = title(0.3, 'The surprise:  it is a liquid')
    e += [Text(A('Physicists expected'), 'expected:  a gas of nearly free quarks and gluons', 80, 180, 48, WHITE)]
    e += [Text(A('What they found'), 'found:  a LIQUID', 1250, 172, 62, YEL)]
    t = A('When two nuclei collide off')
    e += [ellipse(t, 220, 500, 135, 135, BLUE, 4, 0.8, dash=True), ellipse(t + 0.8, 390, 500, 135, 135, BLUE, 4, 0.8, dash=True)]
    e += [Text(t + 1.6, 'off-center collision', 130, 660, 40, WHITE)]
    t = A('the overlap region')
    e += [ellipse(t, 305, 500, 48, 100, ORG, 8, 0.7), Text(t + 0.8, 'almond-shaped overlap', 110, 715, 40, ORG)]
    gx, gy = 880, 500
    e += [Text(A('In a gas'), 'gas', gx - 290, 250, 60, WHITE), ellipse(A('In a gas') + 0.5, gx, gy, 45, 92, ORG, 7, 0.6)]
    t = A('They fly off in random')
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        e += arrow(t + 0.2 * k, gx + 110 * math.cos(a), gy + 110 * math.sin(a), gx + 210 * math.cos(a), gy + 210 * math.sin(a), WHITE, 5, 0.2, 16)
    e += [Text(A('the final spray'), 'same in all directions', gx - 190, 740, 44, WHITE)]
    lx, ly = 1500, 500
    e += [Text(A('In a liquid'), 'liquid', lx - 330, 250, 60, GRN), ellipse(A('In a liquid') + 0.5, lx, ly, 45, 92, ORG, 7, 0.6)]
    t = A('so the liquid is pushed')
    for k, a in enumerate((0, 0.32, -0.32, math.pi, math.pi + 0.32, math.pi - 0.32)):
        e += arrow(t + 0.2 * k, lx + 70 * math.cos(a), ly + 70 * math.sin(a), lx + 310 * math.cos(a), ly + 310 * math.sin(a), GRN, 6, 0.25, 20)
    for k, a in enumerate((math.pi / 2, -math.pi / 2)):
        e += arrow(t + 1.4 + 0.2 * k, lx, ly + 105 * math.sin(a), lx, ly + 165 * math.sin(a), GRN, 5, 0.15, 14)
    e += [Text(A('More particles come out'), 'more particles along the short side', lx - 300, 740, 44, GRN)]
    T = Text(A('Hydrodynamics converts'), 'shape in space    ->    pattern in momentum', 960, 835, 64, YEL, center=True)
    e += [T, rect(A('Hydrodynamics converts') + T.dur, 960 - T.width / 2 - 30, 843, T.width + 60, 112, YEL, 5, 0.8)]
    T = Text(A('And that pattern is exactly'), 'exactly what the detectors see', 900, 968, 44, GRN, center=True)
    e += [T, check(A('And that pattern is exactly') + T.dur, 920 + T.width / 2, 1010)]
    S.append(e)

    # ---------------- 5 flow and viscosity
    A = lambda p: at(4, p); e = title(0.3, 'Anisotropic flow')
    ox, oy = 130, 620
    t = A('Physicists count')
    e += arrow(t, ox, oy, ox + 690, oy, WHITE, 4, 0.4) + arrow(t + 0.5, ox, oy, ox, oy - 400, WHITE, 4, 0.4)
    e += [Text(t + 1.0, 'number of particles', ox + 20, oy - 440, 40, WHITE), Text(A('as a function of the angle'), 'angle φ', ox + 560, oy + 5, 44, WHITE)]
    e += [line(t + 1.6, ox, oy - 190, ox + 640, oy - 190, WHITE, 3, 0.4, dash=True)]
    e += [curve(A('and describe the pattern'), lambda u: (ox + u * 640, oy - 190 - 95 * math.cos(u * 4 * math.pi)), 0, 1, 120, YEL, 8, 2.0)]
    e += [Text(A('and describe the pattern'), 'v_{2},   v_{3},   ...', 900, 180, 66, YEL, cps=10)]
    e += [Text(A('V two measures'), 'v_{2} :   the elliptical part', 900, 290, 50, WHITE)]
    e += [Text(A('It grows as'), 'grows for off-center collisions', 900, 355, 44, GRN)]
    e += [Text(A('V three would be'), 'v_{3} :   zero for smooth nuclei ...', 900, 450, 50, WHITE)]
    t = A('It is not zero')
    e += [Text(t, '... but nuclei are lumpy', 900, 515, 48, PINK), Dots(t + 1.0, cloud(5, 1720, 500, 85, 34), BLUE, 10, 1.2)]
    e += [Text(A('For these patterns'), 'for the pattern to survive:  very small viscosity', 130, 690, 48, WHITE)]
    T = Text(A('The key number'), 'η / s   ≈   1 / 4π', 150, 790, 96, YEL, cps=6)
    e += [T, rect(A('For quark gluon plasma') + 2.0, 130, 805, T.width + 40, 160, YEL, 5, 0.8)]
    e += [Text(A('the viscosity divided'), 'viscosity / entropy density', 1000, 790, 44, WHITE)]
    e += [Text(A('That is lower'), 'lower than any other known liquid', 1000, 860, 48, GRN)]
    e += [Text(A('It is nearly'), 'a nearly perfect liquid', 1000, 935, 58, PINK)]
    S.append(e)

    # ---------------- 6 life of the droplet
    A = lambda p: at(5, p); e = title(0.3, 'The life of a droplet')
    e += arrow(0.03 * D[5], 70, 570, 1850, 570, WHITE, 5, 1.0) + [Text(0.03 * D[5] + 1.0, 'time', 1770, 585, 40, WHITE)]
    t = A('Within about one')
    e += [scribble(t, 200, 400, 36, PINK, 0.6), Text(t + 0.6, '~ 1 fm/c', 110, 600, 48, YEL), Text(A('the plasma forms'), 'plasma forms,\nflows as a fluid', 80, 675, 42, WHITE)]
    t = A('It expands')
    e += [scribble(t, 580, 400, 78, ORG, 1.0), Text(t + 1.0, 'expands, cools', 450, 600, 48, ORG)]
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        e += arrow(A('Its own pressure') + 0.2 * k, 580 + 90 * math.cos(a), 400 + 90 * math.sin(a), 580 + 150 * math.cos(a), 400 + 150 * math.sin(a), WHITE, 5, 0.2, 16)
    e += [Text(A('at about half'), 'outward at about\nhalf the speed of light', 420, 675, 42, WHITE)]
    t = A('When the temperature falls')
    e += [ellipse(t, 1030, 400, 115, 115, YEL, 4, 0.8, dash=True), Text(t + 0.8, 'T ≈ 155 MeV', 900, 600, 48, YEL)]
    e += [Dots(A('the liquid turns into hadrons'), cloud(11, 1030, 400, 100, 40), BLUE, 9, 1.4), Text(A('the liquid turns into hadrons'), 'liquid  ->  hadrons', 900, 675, 42, WHITE)]
    e += [Text(A('This is called chemical'), '"chemical freeze-out"', 890, 735, 42, GRN)]
    t = A('The hadrons keep bumping')
    e += [Dots(t, cloud(23, 1450, 400, 135, 34), BLUE, 9, 1.4), Text(A('until about 95'), 'T ≈ 95 MeV', 1340, 600, 48, YEL), Text(A('until about 95') + 1.0, 'last collisions', 1340, 675, 42, WHITE)]
    t = A('After that, they fly')
    for k, dy in enumerate((-70, 0, 70)):
        e += arrow(t + 0.25 * k, 1620, 400 + dy, 1760, 400 + dy * 1.5, BLUE, 5, 0.25, 16)
    e += [rect(t + 0.9, 1790, 250, 34, 300, WHITE, 5, 0.6), Text(t + 1.5, 'detector', 1600, 175, 42, WHITE)]
    e += [Text(A('Everything we know'), 'everything we know comes from these final particles', 960, 880, 58, PINK, center=True, mw=1750)]
    S.append(e)

    # ---------------- 7 quarkonia
    A = lambda p: at(6, p); e = title(0.3, 'Are the quarks really free?')
    e += [Text(A('An Upsilon is'), 'Υ   =   b  +  anti-b', 80, 185, 60, YEL, cps=10)]
    t = A('It comes in several sizes')
    for k, (x, r, nm) in enumerate(((170, 36, '1S'), (430, 66, '2S'), (750, 100, '3S'))):
        e += [ellipse(t + 0.7 * k, x, 420, r, r, WHITE, 5, 0.5), Dots(t + 0.7 * k + 0.5, [(x - 0.55 * r, 420), (x + 0.55 * r, 420)], BLUE, 11, 0.2), Text(t + 0.7 * k + 0.6, nm, x - 28, 535, 46, WHITE)]
    e += [Text(A('the surrounding color charges'), 'in the plasma:  the binding force is screened', 80, 625, 44, ORG, mw=820)]
    t = A('The small, tightly')
    e += [Text(t, 'survives', 80, 705, 48, GRN), check(t + 0.8, 270, 755)]
    t = A('The larger, loosely')
    for k, (x, r) in enumerate(((430, 66), (750, 100))):
        e += [line(t + 0.4 * k, x - r, 420 - r, x + r, 420 + r, PINK, 6, 0.2), line(t + 0.4 * k + 0.2, x + r, 420 - r, x - r, 420 + r, PINK, 6, 0.2)]
    e += [Text(t + 0.8, 'melt', 550, 705, 48, PINK)]
    e += [Text(A('the larger states are strongly'), 'data:  2S and 3S strongly suppressed in PbPb', 80, 810, 46, WHITE, mw=820)]
    t = A('Charm quarks tell')
    e += [line(t - 0.4, 935, 180, 935, 1000, WHITE, 3, 0.5, dash=True), Text(t, 'J/ψ   =   c  +  anti-c', 990, 185, 60, YEL, cps=12)]
    e += [Text(A('about thirty charm'), 'about 30 charm pairs per collision  (LHC)', 990, 290, 46, WHITE, mw=880)]
    t = A('A charm quark can wander')
    e += [ellipse(t - 1.5, 1420, 570, 380, 170, ORG, 4, 1.0, dash=True)]
    e += [Dots(t - 0.8, [(1130, 530), (1700, 520)], GRN, 12, 0.2), Dots(t - 0.5, [(1175, 620), (1640, 630)], PINK, 12, 0.2)]
    e += [Path(t, [(1130, 530), (1200, 480), (1270, 560), (1330, 520), (1392, 562)], GRN, 4, 1.2, amp=3)]
    e += [Path(A('and pair up with'), [(1640, 630), (1580, 660), (1530, 590), (1480, 620), (1436, 578)], PINK, 4, 1.2, amp=3)]
    t = A('making a new J psi')
    e += [Dots(t, [(1396, 566), (1432, 574)], YEL, 12, 0.2), ellipse(t + 0.3, 1414, 570, 50, 40, YEL, 5, 0.5), Text(t + 0.8, 'new J/ψ', 1340, 440, 46, YEL)]
    T = Text(A('Quarks that wander'), 'quarks wander freely:  not confined', 1010, 810, 54, GRN, mw=830)
    e += [T, rect(A('Quarks that wander') + T.dur, 990, 818, T.width + 40, 105, GRN, 5, 0.7)]
    S.append(e)

    # ---------------- 8 jets
    A = lambda p: at(7, p); e = title(0.3, 'Jets:  a second probe')
    cx, cy = 430, 560
    e += [ellipse(0.02 * D[7], cx, cy, 250, 210, ORG, 5, 1.0, dash=True), Text(0.02 * D[7] + 1.0, 'QGP droplet', cx - 120, cy + 225, 44, ORG)]
    hx, hy = 250, 470
    e += [Dots(A('two quarks or gluons collide'), [(hx, hy)], YEL, 13, 0.2), Text(A('two quarks or gluons collide') + 0.3, 'hard collision', 60, 190, 42, YEL)]
    e += arrow(A('two quarks or gluons collide') + 1.0, 180, 250, 235, 440, YEL, 3, 0.3, 14)
    t = A('Each one flies out')
    for k, (dx, dy) in enumerate(((-190, -150), (-215, -105), (-150, -185))):
        e += [line(t + 0.15 * k, hx, hy, hx + dx, hy + dy, WHITE, 5, 0.25)]
    e += [Text(A('called a jet'), 'jet', 30, 380, 50, WHITE)]
    t = A('the jets must plow')
    e += [line(t, hx, hy, 640, 665, PINK, 5, 1.0, dash=True)]
    for k, (dx, dy) in enumerate(((95, 50), (80, 75), (105, 22))):
        e += [line(t + 1.0 + 0.15 * k, 640, 665, 640 + dx, 665 + dy, PINK, 5, 0.2)]
    e += [Text(A('This is called jet'), 'quenched jet', 610, 760, 46, PINK)]
    t = A('It reappears')
    for k, (x, y, dx, dy) in enumerate(((360, 500, 50, -70), (430, 590, -30, 80), (500, 560, 75, -55), (540, 650, -10, 80), (590, 600, 80, -30))):
        e += arrow(t + 0.2 * k, x, y, x + dx, y + dy, BLUE, 4, 0.15, 12)
    e += [Text(A('It reappears') + 1.0, 'wake', 500, 410, 44, BLUE)]
    e += [Text(A('And they lose a lot'), 'jets lose  10 GeV or more  in a few fm', 900, 185, 50, PINK, mw=960)]
    e += [Text(A('This is called jet'), '"jet quenching"', 900, 262, 58, YEL)]
    T = Text(A('Physicists measure it'), 'R_{AA}  =  jets seen / jets expected without QGP', 920, 385, 54, WHITE, mw=920, cps=16)
    e += [T, rect(A('Physicists measure it') + T.dur, 900, 392, T.width + 40, 110, WHITE, 5, 0.7)]
    e += [Text(A('For jets in head on'), 'jets, head-on collisions:    R_{AA}  well below 1', 900, 545, 48, PINK, mw=960)]
    T = Text(A('For photons and Z'), 'photons, Z bosons:    R_{AA} = 1', 900, 625, 48, GRN)
    e += [T, check(A('For photons and Z') + T.dur, 920 + T.width, 672)]
    e += [Text(A('The lost energy'), 'lost energy  ->  many soft particles at wide angles', 900, 750, 46, BLUE, mw=960)]
    e += [Text(A('like a wake'), '(like the wake behind a boat)', 900, 825, 44, WHITE)]
    S.append(e)

    # ---------------- 9 big questions
    A = lambda p: at(8, p); e = title(0.3, 'Big open questions')
    e += [Text(A('One: how'), '1.   How does the plasma form and flow so fast  (~ 1 fm/c) ?', 90, 190, 54, YEL, mw=1740)]
    e += [Text(A('Two: how small'), '2.   How small can a droplet be?', 90, 310, 54, GRN)]
    e += [Text(A('Even collisions'), 'even proton collisions show some of the same flow patterns', 190, 380, 42, WHITE)]
    e += [Text(A('Three: at very'), '3.   How does a strongly coupled liquid emerge', 90, 480, 54, PINK)]
    e += [Text(A('So how does'), 'from weakly interacting quarks and gluons?', 190, 545, 54, PINK)]
    e += [Text(A('Jets may'), 'jets as a microscope', 190, 618, 42, WHITE)]
    e += [Text(A('And four'), '4.   More quarks than antiquarks:  what changes?', 90, 720, 54, BLUE)]
    e += [Text(A('The smooth crossover may'), 'crossover  ->  sharp transition at a "critical point" ?', 190, 790, 46, WHITE)]
    e += [Text(A('Experiments at lower'), 'being searched for at lower collision energies', 190, 855, 42, ORG)]
    e += [Text(A('Experiments at lower') + 2.0, '?', 1580, 560, 300, YEL, cps=2)]
    S.append(e)

    # ---------------- 10 summary
    A = lambda p: at(9, p); e = title(0.3, 'Summary')
    rows = [('Heavy ion collisions recreate', YEL, '"little bangs":  droplets of early-universe matter'),
            ('Within about one', ORG, 'quark-gluon plasma forms within  ~ 1 fm/c'),
            ('It is not a gas', GRN, 'a liquid, not a gas:    η / s  ≈  1 / 4π'),
            ('We see this in the flow', WHITE, 'flow patterns  (v_{2}, v_{3})   ->   it flows like a liquid'),
            ('We see that the quarks', BLUE, 'Υ melting,  J/ψ recombination   ->   quarks are free'),
            ('And we see how strongly', PINK, 'jet quenching   ->   strongly interacting')]
    for i, (ph, colr, tx) in enumerate(rows):
        y = 180 + i * 98
        T = Text(A(ph), tx, 200, y, 54, colr, mw=1640, cps=26)
        e += [T, check(A(ph) + T.dur + 0.1, 100, y + 75)]
    T = Text(A('How such a liquid'), 'Open:  how does this liquid emerge from quarks and gluons?', 960, 800, 58, YEL, center=True, mw=1700)
    e += [T, rect(A('How such a liquid') + T.dur, 960 - T.width / 2 - 30, 808, T.width + 60, 110, YEL, 5, 0.8)]
    e += [Text(A('Thanks for'), 'Thanks for watching!', 960, 945, 54, WHITE, center=True)]
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
