# dMoon's Chalkboard Physics

Short chalkboard videos that explain physics research papers at an undergraduate level.

Site: https://dmooncnu.github.io/paper-explainers/

## How the site works

- `videos.json` lists every video. The home page (`index.html`) and the player page (`watch.html`) are built from it in the browser.
- Each video lives in `videos/<id>/` as `video.mp4` plus a `poster.jpg` thumbnail.
- GitHub Pages serves the `main` branch, so a push publishes the change within a minute or two.

## Adding a video

Needs Python and ffmpeg.

```
python add_video.py path/to/new.mp4 --id short-name --title "Video title" --summary "One sentence." --cite "Journal ref" --paper-title "Paper title" --authors "Authors" --url https://doi.org/... --tags "tag one, tag two"
git add -A
git commit -m "Add short-name"
git push
```

Optional: add a `chapters` list (`{"t": seconds, "title": "..."}`) to the new entry in `videos.json` to get clickable chapters on the player page.

## Limits

- GitHub rejects single files over 100 MB.
- A GitHub Pages site should stay under about 1 GB in total, which is roughly 25 videos of this length. Beyond that, host the video files elsewhere and put their URL in the `video` field.
