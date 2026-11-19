# Video-making scripts

These scripts draw the chalkboard videos on this site. They are kept here so a video can be re-rendered or used as a starting point for the next one.

## What is here

| File | What it does |
| --- | --- |
| `chalk.py` | The chalkboard renderer (text written stroke by stroke, chalk lines, taped-on paper figures) plus the scenes of the Lévy femtoscopy video |
| `levy/prep.py` | Figure crops and narration text for the Lévy video |
| `chalk_pp.py` | The scenes of the pp 13 TeV video; uses the renderer in `chalk.py` |
| `pp/prep.py` | Figure crops and narration text for the pp 13 TeV video |
| `chalk_ppb.py` | The scenes of the pp / pPb / PbPb video; uses the renderer in `chalk.py` |
| `ppb/prep.py` | Figure crops and narration text for the pp / pPb / PbPb video |
| `chalk_euler.py` | The scenes of the video on Euler's equations for a rigid body (drawings only, no paper figures); writing is timed to phrases of the narration |
| `euler/prep.py` | Narration text for the Euler's equations video (`tts` only) |
| `chalk_hic.py` | The scenes of the video on the review "Heavy Ion Collisions: The Big Picture, and the Big Questions" (drawings only, no paper figures) |
| `hic/prep.py` | Narration text for the heavy-ion review video (`tts` only) |

Figures, audio and previews are generated into each video's folder and are not committed.

## Requirements

- Windows (the handwriting fonts `Inkfree.ttf` and `segoepr.ttf` are read from `C:\Windows\Fonts`)
- Python 3 with `pip install pillow numpy pymupdf edge-tts`
- ffmpeg on the PATH

## Rendering a video

Run from this folder. The pp 13 TeV video is shown; for the Lévy video use `levy/prep.py` and `chalk.py`.

```
python pp/prep.py crops path/to/paper.pdf
python pp/prep.py tts
python chalk_pp.py preview 3
python chalk_pp.py out.mp4
```

- `crops` cuts the figures out of the paper PDF.
- `tts` makes the narration with the `en-US-AvaNeural` voice. It sends the narration text to Microsoft's online speech service.
- `preview` writes still frames of the listed scenes (all scenes if none are listed) to `pp/preview/`.
- The last command renders the full video, which takes several minutes, and prints the chapter start times.

Then publish it with `add_video.py` in the repository root.

## Making a new video

1. Copy `pp/prep.py` to `<name>/prep.py`; set the crop boxes and write one narration paragraph per scene.
2. Copy `chalk_pp.py` to `chalk_<name>.py`; point its folders at `<name>/`, set `NS` to the number of scenes and rewrite `scenes()`.
3. Each element's start time is a fraction of that scene's narration length, so the writing follows the voice.
