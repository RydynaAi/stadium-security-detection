import pytest

from stadiumguard.evaluation import score


def test_mixed_case():
    events = [("a.mp4", 5.0, 5.6), ("b.mp4", 2.0, 2.5)]
    alerts = [("a.mp4", 5.3), ("a.mp4", 9.0), ("c.mp4", 4.0)]
    durations = {"a.mp4": 10.0, "b.mp4": 5.0, "c.mp4": 20.0}
    result = score(events, alerts, durations, 1.0)
    assert result.events == 2
    assert result.detected == 1
    assert result.alerts == 3
    assert result.false_alarms == 2
    assert result.precision == pytest.approx(1 / 3)
    assert result.recall == pytest.approx(0.5)
    assert result.f1 == pytest.approx(0.4)
    assert result.false_alarms_per_minute == pytest.approx(2 / (35 / 60))
    assert result.mean_delay_s == pytest.approx(0.3)


def test_no_alerts():
    result = score([("a.mp4", 5.0, 5.6)], [], {"a.mp4": 8.0}, 1.0)
    assert result.detected == 0
    assert result.precision is None
    assert result.recall == 0.0
    assert result.f1 is None
    assert result.false_alarms_per_minute == 0.0
    assert result.mean_delay_s is None


def test_alert_outside_tolerance_is_false():
    result = score([("a.mp4", 5.0, 5.6)], [("a.mp4", 8.0)], {"a.mp4": 10.0}, 1.0)
    assert result.detected == 0
    assert result.false_alarms == 1


def test_alert_inside_tolerance_counts():
    result = score([("a.mp4", 5.0, 5.6)], [("a.mp4", 4.5)], {"a.mp4": 10.0}, 1.0)
    assert result.detected == 1
    assert result.mean_delay_s == pytest.approx(-0.5)


def test_alert_in_other_video_is_false():
    result = score([("a.mp4", 5.0, 5.6)], [("b.mp4", 5.3)], {"a.mp4": 10.0, "b.mp4": 10.0}, 1.0)
    assert result.detected == 0
    assert result.false_alarms == 1


def test_several_alerts_for_one_event_detect_it_once():
    result = score([("a.mp4", 5.0, 5.6)], [("a.mp4", 5.1), ("a.mp4", 5.4)], {"a.mp4": 10.0}, 1.0)
    assert result.detected == 1
    assert result.false_alarms == 0
    assert result.precision == pytest.approx(1.0)
