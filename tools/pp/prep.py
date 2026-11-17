"""Crop figures from the pp 13 TeV paper (JHEP 03 (2020) 014) and synthesize narration (edge-tts).

  python prep.py crops path/to/paper.pdf     -> figs/*.png
  python prep.py tts                         -> audio/sNN.wav (sends the narration text to Microsoft's online TTS)
"""
import asyncio, os, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs'); AUD = os.path.join(HERE, 'audio')
os.makedirs(FIG, exist_ok=True); os.makedirs(AUD, exist_ok=True)

# name, page, box in 60-dpi page pixels (x0, y0, x1, y1)
CROPS = [('fig3a', 13, 64, 70, 233, 223), ('fig3b', 13, 261, 228, 430, 377),
         ('fig4top', 15, 68, 68, 432, 216), ('fig4botL', 15, 68, 224, 234, 373),
         ('fig5', 17, 68, 68, 432, 224), ('fig6', 19, 68, 68, 432, 224), ('fig7', 20, 68, 68, 432, 222)]

NARR = [
"When two protons collide at the Large Hadron Collider, how big is the region where the new particles are born? And does that tiny region behave like the hot fluid that is created when heavy nuclei collide? In this video, we look at a measurement by the CMS experiment. It uses proton proton collisions at 13 tera electron volts, and a quantum effect called Bose Einstein correlations.",
"First, some background. When heavy nuclei, such as lead, collide, they create a quark gluon plasma: a droplet of hot matter that flows like a fluid. A proton is far smaller than a lead nucleus, so nobody expected the same from proton collisions. Most proton collisions produce only a handful of particles. But a rare few produce more than a hundred. And in those rare, high multiplicity events, physicists found surprising hints of fluid like behavior. Is something like a tiny fireball being formed? One way to find out is to measure the size of the particle source, and to see how it changes.",
"The measuring tool is quantum mechanics. Most of the produced particles are pions, and pions are bosons. Identical bosons tend to come out with nearly the same momentum. So, if we count pairs of same charge particles as a function of their momentum difference, q, we find an excess at small q. And here is the key point. The width of that peak is inversely related to the size of the source. A wide peak means a small source. A narrow peak means a large source. The peak is fitted with a simple formula, which gives two numbers. R is the radius of the source, also called the length of homogeneity. And lambda is the strength of the correlation. In these data, an exponential shape works much better than a Gaussian.",
"The data were recorded in 2015, in special runs with very few simultaneous collisions. That way, each recorded event is one clean proton proton collision. A dedicated trigger collected the rare events with many particles, up to about 250 charged particles in a single collision. The results are then studied as a function of the number of particles, called the multiplicity, and of the transverse momentum of the pair.",
"In proton collisions, there is a catch. Quantum statistics is not the only reason why particles come out close together. Particles from the same jet, or from the decay of the same parent particle, are also close in momentum. That fakes part of the peak. So the team used three different methods to remove this background. The first divides the data by a simulation that has no Bose Einstein effect. The second uses opposite charge pairs from the data itself. They contain the background, but no Bose Einstein effect. The third is a hybrid of the two. Here are two real examples. Black points are same charge pairs, with the Bose Einstein peak. Blue points are opposite charge pairs. On the left is a low multiplicity class. On the right, high multiplicity: the peak is narrower, so the source is larger.",
"First result. The radius grows with multiplicity, from about 0.8 femtometers in the emptiest events, to about 3 femtometers in the busiest. For comparison, the radius of a proton itself is a little under one femtometer. All three methods agree on the radius. It rises steeply at first, changes slope around twenty to thirty particles, and then tends to level off. The strength lambda, on the right, drops quickly at very low multiplicity, and then stays roughly constant.",
"Does the collision energy matter? Here, the new results at 13 tera electron volts, in red, are compared with earlier measurements at 7 tera electron volts, from CMS and from the ATLAS experiment. They agree. At the same multiplicity, the source has the same size. So what sets the size is not the energy of the collision, but how many particles are produced.",
"Now plot the radius against the cube root of the multiplicity. If the number of particles grows with the volume of the source, the radius should follow a straight line. And over most of the range, it does. That is what hydrodynamic models, which treat the system as a fluid, predict. On the right, the data are compared with a different idea, the color glass condensate, which describes the dense gluons inside the colliding protons. Its predicted radius, the blue curve, is much too small, probably because that calculation gives only the initial size, and leaves out the later expansion. But it does predict the shape: a rise, and then a plateau. And above about a hundred particles, the data hint at such a levelling off.",
"One more test. In an expanding source, fast pairs come from a smaller region than slow pairs. So the radius should shrink as the pair momentum grows. And that is what is seen, on the left. Hydrodynamics goes further. One over R squared should rise in a straight line with the transverse mass of the pair. On the right, the data do follow straight lines, just as in collisions of heavy nuclei. The slope tells us how fast the source expands, like a Hubble constant for the fireball. It comes out between about 0.17 and 0.3 per femtometer, comparable to the values found in gold gold collisions. And the expansion is slower in high multiplicity events, the same pattern that is seen when going from glancing to head on collisions of nuclei.",
"Let us sum up. Bose Einstein correlations measure the size of the particle source in proton proton collisions. The radius grows from about 0.8 to 3 femtometers as the multiplicity increases, following the cube root of the number of particles, with a possible saturation at the highest multiplicities. It does not depend on the collision energy. And it shrinks with pair momentum, the signature of an expanding source. So, a proton proton collision that produces many particles looks, in several ways, like a miniature heavy ion collision. Why that is so is still an open question. Thanks for watching.",
]


def crops(pdf):
    import pymupdf
    d = pymupdf.open(pdf); k = 72 / 60
    for name, pg, x0, y0, x1, y1 in CROPS:
        pm = d[pg - 1].get_pixmap(dpi=330, clip=pymupdf.Rect(x0 * k, y0 * k, x1 * k, y1 * k))
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
