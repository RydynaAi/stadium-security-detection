import csv

from stadiumguard.annotations import load_alerts, load_events


def write_csv(path, header, rows):
    with path.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def test_load_events_filters_by_type(tmp_path):
    path = tmp_path / "dev.csv"
    write_csv(
        path,
        ["video", "event_type", "start_s", "end_s"],
        [["a.mp4", "thrown_object", 5.0, 5.6], ["a.mp4", "stampede", 1.0, 2.0]],
    )
    assert load_events(path, "thrown_object") == [("a.mp4", 5.0, 5.6)]


def test_load_alerts_reads_times_and_filters(tmp_path):
    path = tmp_path / "events.csv"
    write_csv(
        path,
        ["video_time_s", "event_type", "confidence", "snapshot"],
        [["1.500", "thrown_object", "1.00", "a.jpg"], ["2.500", "stampede", "0.70", "b.jpg"]],
    )
    assert load_alerts(path, "clip.mp4", "thrown_object") == [("clip.mp4", 1.5)]
