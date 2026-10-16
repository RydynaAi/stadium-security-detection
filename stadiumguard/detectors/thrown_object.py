import cv2

from stadiumguard.detectors.base import Detector
from stadiumguard.events import Event


class ThrownObjectDetector(Detector):
    def __init__(self, threshold, min_area, blur_kernel=0, morph_kernel=0):
        self.threshold = threshold
        self.min_area = min_area
        self.blur_kernel = blur_kernel
        self.morph = (
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel, morph_kernel))
            if morph_kernel
            else None
        )
        self.previous = None

    def update(self, frame, people):
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
        events = []
        for contour in contours:
            if cv2.contourArea(contour) <= self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            if any(x < px2 and x + w > px1 and y < py2 and y + h > py1 for px1, py1, px2, py2 in people):
                continue
            events.append(Event("thrown_object", 1.0, frame.timestamp, frame.index, (x, y, x + w, y + h)))
        return events
