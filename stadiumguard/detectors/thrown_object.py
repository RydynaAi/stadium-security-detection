import math

import cv2

from stadiumguard.detectors.base import Detector
from stadiumguard.events import Event


class ThrownObjectDetector(Detector):
    def __init__(
        self,
        threshold,
        min_area,
        blur_kernel=0,
        morph_kernel=0,
        track_min_frames=0,
        track_min_speed=0.0,
        track_max_distance=150.0,
        track_max_gap=2,
    ):
        self.threshold = threshold
        self.min_area = min_area
        self.blur_kernel = blur_kernel
        self.morph = (
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel, morph_kernel))
            if morph_kernel
            else None
        )
        self.track_min_frames = track_min_frames
        self.track_min_speed = track_min_speed
        self.track_max_distance = track_max_distance
        self.track_max_gap = track_max_gap
        self.tracks = []
        self.previous = None

    def candidates(self, frame, people):
        gray = cv2.cvtColor(frame.image, cv2.COLOR_BGR2GRAY)
        if self.blur_kernel:
            gray = cv2.GaussianBlur(gray, (self.blur_kernel, self.blur_kernel), 0)
        previous, self.previous = self.previous, gray
        if previous is None:
            return []
        difference = cv2.absdiff(previous, gray)
        _, mask = cv2.threshold(difference, self.threshold, 255, cv2.THRESH_BINARY)
        if self.morph is not None:
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.morph)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for contour in contours:
            if cv2.contourArea(contour) <= self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            if any(x < px2 and x + w > px1 and y < py2 and y + h > py1 for px1, py1, px2, py2 in people):
                continue
            boxes.append((x, y, x + w, y + h))
        return boxes

    def update(self, frame, people):
        boxes = self.candidates(frame, people)
        if not self.track_min_frames:
            return [Event("thrown_object", 1.0, frame.timestamp, frame.index, box) for box in boxes]
        return self.track(frame, boxes)

    def track(self, frame, boxes):
        self.tracks = [t for t in self.tracks if frame.index - t["index"] <= self.track_max_gap]
        free = list(self.tracks)
        events = []
        for box in boxes:
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            best = min(free, key=lambda t: math.dist(t["points"][-1][1:], center), default=None)
            if best is not None and math.dist(best["points"][-1][1:], center) <= self.track_max_distance:
                free.remove(best)
                best["points"].append((frame.timestamp, *center))
                best["index"] = frame.index
                track = best
            else:
                track = {"points": [(frame.timestamp, *center)], "index": frame.index, "alerted": False}
                self.tracks.append(track)
            if not track["alerted"] and self.qualifies(track):
                track["alerted"] = True
                events.append(Event("thrown_object", 1.0, frame.timestamp, frame.index, box))
        return events

    def qualifies(self, track):
        points = track["points"]
        if len(points) < self.track_min_frames:
            return False
        (t0, x0, y0), (t1, x1, y1) = points[0], points[-1]
        if t1 <= t0:
            return False
        return math.dist((x0, y0), (x1, y1)) / (t1 - t0) >= self.track_min_speed
