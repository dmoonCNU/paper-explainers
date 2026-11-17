"""Crop figures from the PbPb Levy paper (Phys. Rev. C 109, 024914) and synthesize narration (edge-tts).

  python prep.py crops path/to/paper.pdf     -> figs/*.png
  python prep.py tts                         -> audio/sNN.wav (sends the narration text to Microsoft's online TTS)
"""
import asyncio, os, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs'); AUD = os.path.join(HERE, 'audio')
os.makedirs(FIG, exist_ok=True); os.makedirs(AUD, exist_ok=True)

# name, page, box (x0, y0, x1, y1) in units of page width / 1652; rendered 3400 px per page width
CROPS = [('fig2', 5, 880, 188, 1505, 640), ('fig4', 7, 108, 1440, 808, 1845), ('fig5', 7, 848, 1418, 1548, 1812),
         ('fig7', 9, 108, 188, 808, 608), ('fig9', 10, 180, 188, 745, 790), ('fig10', 10, 108, 988, 808, 1805)]

# Spellings such as "Lay-vee", "Koh-shee" and "Rick" (RHIC) are there for the voice, not typos.
NARR = [
"What does the hottest matter in the universe look like, when it is only a few millionths of a billionth of a meter across? In this video, we walk through a measurement by the CMS experiment at the Large Hadron Collider. It uses a quantum effect, called Bose Einstein correlations, to take a picture of that matter.",
"At the Large Hadron Collider, lead nuclei are smashed together at almost the speed of light. For a brief instant, the protons and neutrons melt into a quark gluon plasma: a droplet of matter more than a hundred thousand times hotter than the center of the Sun. The droplet expands like a tiny fluid, cools down, and turns into thousands of ordinary particles, mostly pions. It is only about ten femtometers wide, and it lives for an unimaginably short time. No microscope can see it. So, how do we measure its size and its shape?",
"The trick comes from quantum mechanics. Pie-ons are bosons, and identical bosons like to be in the same state. So, two identical pions are found with nearly the same momentum more often than chance would predict. We count pairs as a function of their momentum difference, q, and we compare with pairs that have no quantum effect. The ratio is called the correlation function. It shows a bump at small q. And here is the key. The width of the bump is inversely related to the size of the source. A narrow bump means a large source. A wide bump means a small source. Astronomers Hanbury Brown and Twiss used the same idea with light, to measure the sizes of stars. In nuclear physics, it is called femtoscopy.",
"The bump tells us not only the size, but also the shape of the source. For many years, physicists assumed that the source is a Gaussian, the familiar bell curve. But there is a more general family, called Lay-vee stable distributions. They have a shape parameter, alpha. When alpha equals two, you get a Gaussian. When alpha equals one, you get a Koh-shee distribution, with a very long tail. Why would a tail appear? As the gas of particles expands and thins out, particles can travel farther and farther between collisions. A few very long steps create a long tail. This is called anomalous diffusion.",
"So, the measured bump is fitted with a simple formula. It has three parameters. R is the Lay-vee scale. It tells us the size of the source. Alpha is the shape. Two means Gaussian, and smaller values mean a longer tail. And lambda is the strength of the correlation. It tells us what fraction of the pions comes from the hot central core, and not from a wide halo of long lived particles that decay far away.",
"CMS recorded more than four billion lead lead collisions in 2018, at an energy of 5.02 tera electron volts per nucleon pair. The team paired up charged particles with the same electric charge from the same collision, and divided by pairs taken from different collisions, which cannot have any quantum correlation. After accounting for the electric repulsion between the charges, they fitted the bump with the Lay-vee formula. Here is one example. The black points are the data, and the curve is the fit. This was repeated for six classes of centrality, meaning how head on the collision is, and for twenty four ranges of pair momentum.",
"First result: the size. The Lay-vee scale R ranges from about 1.6 to 5.8 femtometers. On the left, R shrinks as the transverse mass of the pair increases. Transverse mass basically tells us how fast the pair moves sideways. Head on, or central, collisions, shown in black, give the largest sources. Glancing collisions, shown in magenta, give the smallest. That makes sense: more overlapping nucleons make a bigger fireball. In fact, on the right, R grows in a straight line with the cube root of the number of participating nucleons, just as a radius should grow with volume.",
"Why does R shrink with transverse mass? The team plotted one over R squared against transverse mass. Hydrodynamics, the theory of flowing fluids, predicts a straight line. And the data do follow straight lines in every centrality class, even though the source is not Gaussian. The slope tells us how fast the fireball expands. It acts like a Hubble constant, the same quantity that describes the expansion of the universe. Here, it lies between 0.11 and 0.18, in units of the speed of light per femtometer. One puzzle remains. The lines cross the vertical axis below zero, which simple models do not predict.",
"Second result: the shape. Alpha lies between 1.6 and 2. So the source is neither a Koh-shee shape, nor a perfect Gaussian. A full Lay-vee description is needed. Alpha barely depends on the pair momentum, but it rises steadily as the collisions become more central, approaching the Gaussian value of two. It is also about fifty percent larger than the value of 1.2, measured in gold gold collisions at the lower energy collider, Rick. One possible explanation is that the denser matter at the LHC leaves less room for anomalous diffusion.",
"Third result: the strength, lambda. CMS did not identify the particle types here, so some pairs are not really identical pions, and that weakens the bump. After correcting for the fraction of pions, the corrected strength, lambda star, is nearly flat with transverse mass, but it is still below one. In the core halo picture, this means that a noticeable share of the pions comes from the halo. They are born in decays of long lived particles, far from the core. Lambda star also decreases as the collisions become more central.",
"Let us sum up. Using quantum correlations between identical particles, CMS measured the size and the shape of the particle source in lead lead collisions. The source is a few femtometers across, and it grows with the number of participating nucleons. Its size follows the scaling expected for an expanding fluid. Its shape is close to, but not exactly, a Gaussian, with alpha between 1.6 and 2. And part of the pions comes from a surrounding halo. Together, these results give a new and precise picture of the hot matter created in heavy ion collisions. Thanks for watching.",
]


def crops(pdf):
    import pymupdf
    d = pymupdf.open(pdf)
    for name, pg, x0, y0, x1, y1 in CROPS:
        p = d[pg - 1]; k = p.rect.width / 1652; z = 3400 / p.rect.width
        pm = p.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=pymupdf.Rect(x0 * k, y0 * k, x1 * k, y1 * k))
        pm.save(os.path.join(FIG, name + '.png')); print(name, pm.width, pm.height)


async def tts(voice='en-US-AvaNeural', rate='-6%'):
    import edge_tts
    for i, t in enumerate(NARR, 1):
        mp3 = os.path.join(AUD, 's%02d.mp3' % i); wav = os.path.join(AUD, 's%02d.wav' % i)
        await edge_tts.Communicate(t, voice, rate=rate).save(mp3)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ar', '22050', '-ac', '1', '-c:a', 'pcm_s16le', wav], check=True)
        with wave.open(wav) as w: print('s%02d: %.1f s' % (i, w.getnframes() / w.getframerate()), flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'crops': crops(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == 'tts': asyncio.run(tts())
    else: print(__doc__)
