import csv
from pathlib import Path

import cv2


def load_events(path, event_type):
    with Path(path).open(newline="") as file:
        return [
            (row["video"], float(row["start_s"]), float(row["end_s"]))
            for row in csv.DictReader(file)
            if row["event_type"] == event_type
        ]


def load_alerts(path, video, event_type):
    with Path(path).open(newline="") as file:
        return [
            (video, float(row["video_time_s"]))
            for row in csv.DictReader(file)
            if row["event_type"] == event_type
        ]


def video_duration(path):
    capture = cv2.VideoCapture(str(path))
    frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = capture.get(cv2.CAP_PROP_FPS)
    capture.release()
    return frames / fps if fps else 0.0
