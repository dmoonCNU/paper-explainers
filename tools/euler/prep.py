"""Narration for the video on Euler's equations for a rotating rigid body (no paper figures).

  python prep.py tts      -> audio/sNN.wav (sends the narration text to Microsoft's online TTS)
"""
import asyncio, os, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, 'audio')

NARR = [
"Take a tennis racket, and toss it in the air with a spin. There are three natural ways to do it. Spin it about its handle, and it turns smoothly. Spin it flat, like a frisbee, and it is smooth again. But flip it end over end, about the remaining axis, and something odd happens. It always adds a half twist, no matter how carefully you throw. A phone does the same thing. Why? The answer is in three short equations, written down by Leonhard Euler more than 250 years ago. They are Euler's equations for a rotating rigid body.",
"Start with what we know. For motion along a line, force equals the rate of change of momentum. For rotation, the rule has the same spirit. Torque equals the rate of change of angular momentum, L. For a wheel on a fixed axle, L is just the moment of inertia, I, times the angular velocity, omega. But a freely tumbling body is harder. In general, L does not even point along omega. The moment of inertia is not a single number; it depends on the axis. And, seen from the room, the body keeps turning, so its inertia keeps changing with time. That makes the equation messy.",
"Two ideas fix this. The first idea: every rigid body, whatever its shape, has three special perpendicular directions, called the principal axes. If the body spins about one of them, L is parallel to omega. Each axis has its own moment of inertia: I one, I two, and I three. For the racket, the smallest is about the handle. The largest is about the axis that goes through the strings. And the third is in between. Along these axes, angular momentum is simple. Its three components are I one omega one, I two omega two, and I three omega three. The second idea: use axes that are glued to the body, and turn with it. In this body frame, the three moments of inertia never change.",
"But there is a price. The body frame is rotating, and Newton's laws hold in a frame that is not. So we need to translate between the two. Picture a vector, A, that is constant as seen from the body. Seen from the room, it is swept around, and its tip moves at a rate omega cross A. So, for any vector, the rate of change seen from the room, equals the rate of change seen from the body, plus omega cross the vector. Now apply this to L. The torque equals the change of L in the body frame, plus omega cross L. This extra term is the whole story. It is a close relative of the centrifugal and Coriolis forces.",
"Now write this out, component by component, along the principal axes. Here is the first one. I one, times the rate of change of omega one, minus, I two minus I three, times omega two, omega three, equals the torque about axis one. The other two follow the same pattern. Just rotate the labels. One goes to two, two goes to three, and three goes to one. These are Euler's equations. Look at their structure. The first term is the familiar one: inertia, times angular acceleration. The second term mixes the other two axes, and it is only there when their moments of inertia are different. It means that the rotation about one axis can change, even with no torque at all.",
"Let us check them on simple cases. Check one: rotation about a single principal axis. Omega two and omega three are zero, so the mixing term vanishes, and we get back the familiar law for a wheel on an axle. Check two: a sphere, with no torque. All three moments are equal, so every mixing term vanishes, and omega stays constant, forever. Check three: any body, with no torque, spinning exactly about one principal axis. Again, nothing changes. So steady rotation about each principal axis is always a solution. The real question is: what happens if the spin is slightly off?",
"First, take a symmetric body, like the Earth, where I one equals I two. With no torque, the third equation says that omega three is constant. The first two say that omega one and omega two chase each other around a circle. So the rotation vector slowly circles the symmetry axis, at a rate capital Omega, equal to I three minus I one, over I one, times omega three. The spin is slightly off, and it stays slightly off. It just wobbles. The Earth is slightly flattened, and Euler predicted that its rotation axis should wander around the pole, with a period of about 305 days. Such a wobble was found, more than a century later, with a period of about 433 days. It is longer, because the Earth is not perfectly rigid.",
"Now, back to the racket, with three different moments: I one, less than I two, less than I three. Spin it mostly about one axis, with a tiny wobble about the other two. Put that into Euler's equations, and the tiny wobble obeys a simple rule: its second derivative equals a constant, k, times itself. And the sign of k depends on which axis we chose. For the axis with the smallest, or the largest, moment of inertia, k is negative. That is the equation of a mass on a spring. The wobble just oscillates, and stays small. The rotation is stable. But for the middle axis, k is positive. The wobble grows exponentially. The rotation is unstable, and the body flips over. This is the tennis racket theorem. In space, it is also called the Janibekov effect, after the cosmonaut who watched a spinning wing nut flip, again and again.",
"Let us sum up. Torque equals the rate of change of angular momentum. For a tumbling body, use the principal axes, glued to the body, so the moments of inertia stay constant. The rotating frame adds one term: omega cross L. Together, they give Euler's three equations. And from them, we learned two things. A symmetric body wobbles steadily, like the Earth. And a body with three different moments spins stably about its smallest and largest axes, but never about the middle one. The same equations are used today to control satellites and spacecraft. So, the next time your phone twists in the air, blame Euler. Thanks for watching.",
]


async def tts(voice='en-US-AvaNeural', rate='-6%'):
    import edge_tts
    os.makedirs(AUD, exist_ok=True)
    for i, t in enumerate(NARR, 1):
        mp3 = os.path.join(AUD, 's%02d.mp3' % i); wav = os.path.join(AUD, 's%02d.wav' % i)
        await edge_tts.Communicate(t, voice, rate=rate).save(mp3)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ar', '22050', '-ac', '1', '-c:a', 'pcm_s16le', wav], check=True)
        with wave.open(wav) as w: print('s%02d: %.1f s' % (i, w.getnframes() / w.getframerate()), flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'tts': asyncio.run(tts())
    else: print(__doc__)
