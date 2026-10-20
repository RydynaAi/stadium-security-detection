import numpy as np

from stadiumguard.alerts import AlertManager
from stadiumguard.events import Event, EventLog


def make_manager(tmp_path, cooldown=3.0):
    log = EventLog(tmp_path)
    return AlertManager(log, cooldown), log


def read_rows(log):
    return log.path.read_text().splitlines()[1:]


def test_cooldown_suppresses_repeat_of_same_type(tmp_path):
    manager, log = make_manager(tmp_path)
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    results = [manager.handle(Event("thrown_object", 1.0, t, int(t * 30)), image) for t in (1.0, 2.0, 4.5)]
    assert results == [True, False, True]
    assert len(read_rows(log)) == 2


def test_cooldown_is_per_event_type(tmp_path):
    manager, log = make_manager(tmp_path)
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    assert manager.handle(Event("thrown_object", 1.0, 1.0, 30), image)
    assert manager.handle(Event("stampede", 0.7, 1.5, 45), image)
    assert len(read_rows(log)) == 2


def test_event_log_writes_row_and_snapshot(tmp_path):
    log = EventLog(tmp_path)
    log.record(Event("thrown_object", 0.8, 1.5, 45), np.zeros((20, 20, 3), dtype=np.uint8))
    assert read_rows(log) == ["1.500,thrown_object,0.80,000045_thrown_object.jpg"]
    assert (log.snapshots / "000045_thrown_object.jpg").stat().st_size > 0


def test_event_box_is_optional():
    assert Event("thrown_object", 1.0, 1.5, 45).box is None
    assert Event("thrown_object", 1.0, 1.5, 45, (1, 2, 3, 4)).box == (1, 2, 3, 4)
