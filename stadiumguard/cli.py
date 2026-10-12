import argparse
from pathlib import Path

import cv2

from stadiumguard.alerts import AlertManager
from stadiumguard.config import Config
from stadiumguard.detectors.thrown_object import ThrownObjectDetector
from stadiumguard.events import EventLog
from stadiumguard.people import PersonDetector
from stadiumguard.video_source import VideoSource


def parse_args(argv):
    defaults = Config()
    parser = argparse.ArgumentParser(prog="stadiumguard")
    parser.add_argument("--source", default=defaults.source)
    parser.add_argument("--model", default=defaults.model_path)
    parser.add_argument("--output-dir", type=Path, default=defaults.output_dir)
    parser.add_argument("--no-window", action="store_true")
    return parser.parse_args(argv)


def draw_event(canvas, event):
    if event.box is None:
        return
    x1, y1, x2, y2 = event.box
    cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.putText(canvas, event.event_type, (x1, max(y1 - 10, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


def run(config):
    people_detector = PersonDetector(config.model_path, config.person_confidence)
    detectors = [ThrownObjectDetector(config.motion_threshold, config.motion_min_area)]
    log = EventLog(config.output_dir)
    alerts = AlertManager(log, config.alert_cooldown_seconds)
    print(f"Logging to {log.directory}")
    try:
        for frame in VideoSource(config.source).frames():
            people = people_detector.detect(frame.image)
            canvas = frame.image.copy()
            for x1, y1, x2, y2 in people:
                cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 255, 0), 2)
            for detector in detectors:
                for event in detector.update(frame, people):
                    draw_event(canvas, event)
                    alerts.handle(event, canvas)
            if config.show_window:
                cv2.imshow("StadiumGuard", canvas)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        cv2.destroyAllWindows()


def main(argv=None):
    args = parse_args(argv)
    config = Config(
        source=args.source,
        model_path=args.model,
        output_dir=args.output_dir,
        show_window=not args.no_window,
    )
    try:
        run(config)
    except (FileNotFoundError, RuntimeError) as error:
        print(error)
        return 1
    except KeyboardInterrupt:
        print("Stopped.")
    return 0