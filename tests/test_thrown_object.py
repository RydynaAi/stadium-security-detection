import numpy as np

from stadiumguard.detectors.thrown_object import ThrownObjectDetector
from stadiumguard.video_source import Frame


def blank():
    return np.zeros((480, 640, 3), dtype=np.uint8)


def with_square(top=100, left=200, size=60):
    image = blank()
    image[top : top + size, left : left + size] = 255
    return image


def test_first_frame_gives_no_event():
    detector = ThrownObjectDetector(25, 1500)
    assert detector.update(Frame(blank(), 0, 0.0), []) == []


def test_moving_square_is_detected_with_its_box():
    detector = ThrownObjectDetector(25, 1500)
    detector.update(Frame(blank(), 0, 0.0), [])
    events = detector.update(Frame(with_square(), 1, 0.033), [])
    assert len(events) == 1
    assert events[0].box == (200, 100, 260, 160)
    assert events[0].event_type == "thrown_object"


def test_motion_inside_a_person_box_is_ignored():
    detector = ThrownObjectDetector(25, 1500)
    detector.update(Frame(blank(), 0, 0.0), [])
    assert detector.update(Frame(with_square(), 1, 0.033), [(190, 90, 270, 170)]) == []


def test_small_motion_is_ignored():
    detector = ThrownObjectDetector(25, 1500)
    detector.update(Frame(blank(), 0, 0.0), [])
    assert detector.update(Frame(with_square(size=20), 1, 0.033), []) == []


def test_blur_and_closing_still_detect_the_square():
    detector = ThrownObjectDetector(25, 1500, 5, 5)
    detector.update(Frame(blank(), 0, 0.0), [])
    events = detector.update(Frame(with_square(), 1, 0.033), [])
    assert len(events) == 1
    assert events[0].box == (199, 99, 261, 161)


def test_tracking_alerts_on_fast_motion_only_once():
    detector = ThrownObjectDetector(25, 1500, 0, 0, 3, 500.0, 150.0, 2)
    counts = [len(detector.track(Frame(None, i, i / 60), [(20 * i, 100, 20 * i + 60, 160)])) for i in range(6)]
    assert counts == [0, 0, 1, 0, 0, 0]


def test_tracking_ignores_slow_motion():
    detector = ThrownObjectDetector(25, 1500, 0, 0, 3, 500.0, 150.0, 2)
    counts = [len(detector.track(Frame(None, i, i / 60), [(2 * i, 100, 2 * i + 60, 160)])) for i in range(6)]
    assert counts == [0, 0, 0, 0, 0, 0]
