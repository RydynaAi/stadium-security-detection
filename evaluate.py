import argparse
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from stadiumguard.annotations import load_alerts, load_events, video_duration
from stadiumguard.cli import run
from stadiumguard.config import Config
from stadiumguard.evaluation import score

VIDEO_SUFFIXES = {".mp4", ".mov", ".avi", ".mkv"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--videos", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--event-type", default="thrown_object")
    parser.add_argument("--tolerance", type=float, default=1.0)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main():
    args = parse_args()
    videos = sorted(p for p in args.videos.iterdir() if p.suffix.lower() in VIDEO_SUFFIXES)
    events = load_events(args.annotations, args.event_type)
    missing = {name for name, _, _ in events} - {video.name for video in videos}
    if missing:
        raise SystemExit(f"Annotated videos not found in {args.videos}: {sorted(missing)}")
    root = args.output_dir / datetime.now().strftime("eval_%Y%m%d_%H%M%S")
    alerts = []
    durations = {}
    for video in videos:
        out = root / video.stem
        run(Config(source=str(video), output_dir=out, show_window=False))
        log = next(out.glob("run_*/events.csv"))
        alerts += load_alerts(log, video.name, args.event_type)
        durations[video.name] = video_duration(video)
    result = score(events, alerts, durations, args.tolerance)
    print({k: v for k, v in asdict(Config()).items() if k not in ("source", "output_dir", "show_window")})
    print(f"videos={len(videos)} tolerance={args.tolerance}")
    for key, value in asdict(result).items():
        print(f"{key}: {round(value, 3) if isinstance(value, float) else value}")


main()
