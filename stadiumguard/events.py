import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2


@dataclass(frozen=True)
class Event:
    event_type: str
    confidence: float
    timestamp: float
    frame_index: int


class EventLog:
    def __init__(self, output_dir):
        name = datetime.now().strftime("run_%Y%m%d_%H%M%S")
        self.directory = Path(output_dir) / name
        self.snapshots = self.directory / "snapshots"
        self.snapshots.mkdir(parents=True)
        self.path = self.directory / "events.csv"
        with self.path.open("w", newline="") as file:
            csv.writer(file).writerow(["video_time_s", "event_type", "confidence", "snapshot"])

    def record(self, event, image):
        snapshot = self.snapshots / f"{event.frame_index:06d}_{event.event_type}.jpg"
        cv2.imwrite(str(snapshot), image)
        with self.path.open("a", newline="") as file:
            csv.writer(file).writerow(
                [f"{event.timestamp:.3f}", event.event_type, f"{event.confidence:.2f}", snapshot.name]
            )
            