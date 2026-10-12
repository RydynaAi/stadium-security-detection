from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class Scores:
    events: int
    detected: int
    alerts: int
    false_alarms: int
    precision: float | None
    recall: float | None
    f1: float | None
    false_alarms_per_minute: float | None
    mean_delay_s: float | None


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def f1_score(precision, recall):
    if precision is None or recall is None:
        return None
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def score(events, alerts, durations, tolerance):
    matched = set()
    delays = []
    for video, start, end in events:
        hits = [
            (time, index)
            for index, (name, time) in enumerate(alerts)
            if name == video and start - tolerance <= time <= end + tolerance
        ]
        if hits:
            delays.append(min(hits)[0] - start)
            matched.update(index for _, index in hits)
    detected = len(delays)
    false_alarms = len(alerts) - len(matched)
    precision = ratio(detected, detected + false_alarms)
    recall = ratio(detected, len(events))
    minutes = sum(durations.values()) / 60
    return Scores(
        events=len(events),
        detected=detected,
        alerts=len(alerts),
        false_alarms=false_alarms,
        precision=precision,
        recall=recall,
        f1=f1_score(precision, recall),
        false_alarms_per_minute=ratio(false_alarms, minutes),
        mean_delay_s=mean(delays) if delays else None,
    )
