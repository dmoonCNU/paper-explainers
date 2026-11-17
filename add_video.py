"""Add a video to the site.

    python add_video.py path/to/video.mp4 --id my-topic --title "My title" \
        --summary "One sentence." --cite "Phys. Rev. C 1, 2 (2026)" \
        --paper-title "Paper title" --authors "X Collaboration" \
        --url https://doi.org/... --tags "tag one, tag two" --poster-at 60

Copies the video to videos/<id>/video.mp4, grabs a poster frame with ffmpeg,
reads the duration with ffprobe and adds an entry to videos.json.
Afterwards:  git add -A ; git commit -m "Add <id>" ; git push
"""
import argparse, datetime, json, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video')
    ap.add_argument('--id', required=True, help='short name used in the URL, e.g. levy-femtoscopy')
    ap.add_argument('--title', required=True)
    ap.add_argument('--summary', default='')
    ap.add_argument('--cite', default='', help='journal reference of the paper')
    ap.add_argument('--paper-title', default='')
    ap.add_argument('--authors', default='')
    ap.add_argument('--url', default='', help='link to the paper (DOI or arXiv)')
    ap.add_argument('--tags', default='', help='comma-separated')
    ap.add_argument('--credits', default='')
    ap.add_argument('--poster-at', type=float, default=30, help='time in seconds of the poster frame')
    a = ap.parse_args()

    dest = ROOT / 'videos' / a.id
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(a.video, dest / 'video.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a.poster_at), '-i', str(dest / 'video.mp4'),
                    '-frames:v', '1', '-vf', 'scale=960:-2', '-q:v', '3', str(dest / 'poster.jpg')], check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                str(dest / 'video.mp4')], check=True, capture_output=True, text=True).stdout)
    size_mb = (dest / 'video.mp4').stat().st_size / 1e6

    entry = {
        'id': a.id, 'title': a.title, 'summary': a.summary,
        'date': datetime.date.today().isoformat(), 'duration': round(dur),
        'video': f'videos/{a.id}/video.mp4', 'poster': f'videos/{a.id}/poster.jpg',
        'tags': [t.strip() for t in a.tags.split(',') if t.strip()],
    }
    if a.cite or a.paper_title:
        entry['paper'] = {'authors': a.authors, 'title': a.paper_title, 'cite': a.cite, 'url': a.url}
    if a.credits:
        entry['credits'] = a.credits

    path = ROOT / 'videos.json'
    items = [v for v in json.loads(path.read_text(encoding='utf-8')) if v['id'] != a.id]
    items.append(entry)
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'added {a.id}: {dur:.0f} s, {size_mb:.0f} MB')
    if size_mb > 95:
        print('WARNING: GitHub rejects files over 100 MB. Re-encode the video smaller before pushing.')


if __name__ == '__main__':
    main()
