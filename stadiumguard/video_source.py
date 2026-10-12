import sys
import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class Frame:
    image: np.ndarray
    index: int
    timestamp: float


class VideoSource:
    def __init__(self, source):
        self.is_camera = source.isdigit()
        if not self.is_camera and not Path(source).is_file():
            raise FileNotFoundError(f"Video file not found: {source}")
        backend = cv2.CAP_DSHOW if self.is_camera and sys.platform == "win32" else cv2.CAP_ANY
        self.capture = cv2.VideoCapture(int(source) if self.is_camera else source, backend)
        if not self.capture.isOpened():
            raise RuntimeError(f"Could not open video source: {source}")
        self.fps = self.capture.get(cv2.CAP_PROP_FPS) or 30.0

    def frames(self):
        start = time.monotonic()
        index = 0
        try:
            while True:
                ok, image = self.capture.read()
                if not ok:
                    return
                seconds = time.monotonic() - start if self.is_camera else index / self.fps
                yield Frame(image, index, seconds)
                index += 1
        finally:
            self.capture.release()