"""Crop figures from the pp/pPb/PbPb paper (Phys. Rev. C 97, 064912) and synthesize narration (edge-tts).

  python prep.py crops path/to/paper.pdf     -> figs/*.png
  python prep.py tts                         -> audio/sNN.wav (sends the narration text to Microsoft's online TTS)
"""
import asyncio, os, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs'); AUD = os.path.join(HERE, 'audio')
os.makedirs(FIG, exist_ok=True); os.makedirs(AUD, exist_ok=True)

# name, page, box in 100-dpi page pixels (x0, y0, x1, y1)
CROPS = [('fig1', 4, 140, 88, 700, 330), ('fig3b', 7, 448, 368, 745, 640), ('fig20top', 21, 140, 88, 700, 330),
         ('fig22R', 23, 85, 90, 378, 362), ('fig23R', 23, 452, 90, 745, 362), ('fig24pPb', 24, 403, 332, 712, 585),
         ('fig27top', 26, 140, 88, 700, 338)]

NARR = [
"Protons can collide with protons. Protons can collide with lead nuclei. And lead nuclei can collide with each other. These are three very different collisions. But does the cloud of particles they produce look different? In this video, we look at a measurement by the CMS experiment at the Large Hadron Collider. It uses one and the same quantum ruler, Bose Einstein correlations, on all three.",
"Here are the three systems. Two protons, at collision energies of 0.9, 2.76, and 7 tera electron volts. A proton and a lead nucleus, at 5.02 tera electron volts per nucleon pair. And two lead nuclei, at 2.76 tera electron volts. For lead lead, only the glancing, or peripheral, collisions are used, where the two nuclei barely overlap. Why? Because those produce about as many particles as the busiest proton lead collisions. That lets us ask a sharp question. If two collisions produce the same number of particles, is the source of those particles the same size, no matter what collided?",
"How do you measure something that is only a few femtometers across? A femtometer is a millionth of a billionth of a meter. The answer is quantum statistics. Pions and kaons are bosons, and identical bosons like to come out with nearly the same momentum. So, if we count pairs of identical particles against their momentum difference, q, we see a peak at small q. The width of that peak is inversely related to the size of the source. A narrow peak means a large source. The peak is fitted with an exponential formula. R is the radius of the source, and lambda is the strength of the correlation.",
"The effect only works for identical particles. So it helps to know what each particle is. CMS does this with its silicon tracker. As a charged particle crosses the silicon, it loses a little energy. At the same momentum, a heavier particle moves more slowly, and loses more energy. Plot the energy loss against momentum, and the particles fall into separate bands: pions, kaons, and protons. On the left are all the positive particles. On the right, only those that are identified with a purity above 99.5 percent. This gives clean samples of pions, and of kaons.",
"Before reading off the size, two other effects must be removed. First, electric charge. Two particles with the same charge repel each other, and that eats away the peak at very small q. This is the Coulomb effect, and it can be calculated and corrected. Second, particles that come from the same small jet, or from the decay of the same parent particle, are also close in momentum. The paper calls these clusters. To measure them, the team used pairs with opposite charge. They have no Bose Einstein effect, but they do have the clusters. Here, they show up as a broad bump. Its shape is then scaled, and removed from the same charge pairs. A second, independent method, used for proton proton collisions, divides the data by a simulation that has no Bose Einstein effect. The two methods agree.",
"Now, the first result. These are the cleaned up correlation functions for pion pairs in proton lead collisions. On the left, events with few particles. On the right, events with many. The peak on the right is narrower, so the source is larger. The radius goes from about 2.1 femtometers, to almost 4. And here is the full picture: the radius against the number of charged particles, the multiplicity, for all the systems. In every system, the radius grows steadily with multiplicity, from about 1 femtometer to about 5. In proton proton collisions, it follows the cube root of the multiplicity.",
"Now look at that plot again, and compare the systems. The three proton proton energies, in red, green, and blue, lie on top of each other. Proton lead, in magenta, continues along the same trend. And peripheral lead lead, in orange, is close by, though somewhat larger at high multiplicity. So, to a good approximation, the size of the source is set by how many particles are produced, and not by what was collided, or at what energy. Some differences between the systems do appear at the highest multiplicities.",
"The source also has a shape. So the measurement is repeated in three directions. Long, along the beam. Out, along the direction in which the pair is moving, sideways from the beam. And side, perpendicular to both. In proton proton and proton lead collisions, the long radius is the largest, and the out radius is the smallest. The source is stretched along the beam. In peripheral lead lead collisions, the three radii are about equal. The source is nearly symmetric. The biggest difference between the systems is in the out direction, on the right. That radius is also sensitive to how long the source keeps emitting particles. So this may point to different lifetimes in the three systems.",
"Two more observations. First, the radius becomes smaller when the pair has more transverse momentum. Here, for proton lead, each line is one multiplicity class, and each one bends downward. That is expected if the source is expanding, because fast pairs then come from a smaller patch of it. What is more, the two dependences factorize: the radius is simply a function of the multiplicity, times a function of the pair momentum. Second, kaons. There are about a hundred times fewer kaon pairs than pion pairs, so the uncertainties are larger. The kaon radii also grow with multiplicity, but less than the pion radii.",
"Let us sum up. CMS measured Bose Einstein correlations of identified pions and kaons in three collision systems. The source radius ranges from about 1 to 5 femtometers, and it grows with the number of particles produced. At the same multiplicity, it is nearly the same in proton proton, proton lead, and peripheral lead lead collisions, whatever the energy. In the small systems, the source is stretched along the beam. And it shrinks with pair momentum, as an expanding source should. The takeaway: particles seem to stop interacting, to freeze out, at a common density in all these collisions. More particles simply need more room. Thanks for watching.",
]


def crops(pdf):
    import pymupdf
    d = pymupdf.open(pdf); k = 72 / 100
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
