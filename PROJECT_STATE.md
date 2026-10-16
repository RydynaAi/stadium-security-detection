# Project State

Last updated: 2026-10-12

## Current phase

Phase 1 (package structure) is complete except one open acceptance item: the command line run on a video file was tested on one short clip only. Phase 2 (thrown objects) has not started.

## Done

- Phase 0: cleaned the repository, pinned dependency versions, added AGPL-3.0 license and `test_camera.py`.
- Package `stadiumguard` with: `config.py`, `video_source.py`, `events.py`, `alerts.py`, `people.py`, `detectors/base.py`, `detectors/thrown_object.py`, `cli.py`, `__main__.py`.
- Run with `python -m stadiumguard --source 0` or `--source <video file>`.
- Frame timestamps come from the frame index and the video frame rate, so alert times can be compared with labeled intervals. For a live camera they come from elapsed time.
- Alerts do not block the video loop. Each event is written to `events.csv` with a snapshot, and the cooldown is per event type and based on video time.
- The original single-file script was removed. It stays available in git history (commit `fc7b7b6`).

## Evidence

- No `winsound` or `tkinter` anywhere in the package.
- Camera run: the window opened, people were boxed, one alert was logged with a snapshot.
- Video file run on `data/dev/test_01.mp4` (624x848, 30 fps, 214 frames, compressed by a messaging app): the window opened and people were boxed. The log contained zero alerts.
- Diagnosis on the same clip: thrown-object motion regions between 4.83 s and 5.43 s were mostly under the 1500 pixel area threshold, and almost all of them were inside the person box, which the overlap rule discards. One frame was checked: person box (245, 110, 362, 543) against a motion region (281, 202, 313, 297).

## Baseline

The thrown object detector ported from the original script finds no thrown objects on `test_01.mp4`. The throw happens around second 5. This is the starting point for Phase 2. It is one clip, so it is not a performance claim.

## Decisions

- Python 3.12 for this project. MediaPipe, needed in Phase 6, does not list 3.13 as supported.
- License: AGPL-3.0, because Ultralytics is AGPL-3.0 or paid Enterprise. Review before Phase 8.
- On Windows, camera sources use the DirectShow backend, because the default backend returned a black frame on this laptop.
- Test material: iPhone clips (Most Compatible, 1080p, 30 fps, fixed mount, normal video mode, not slow motion). Public datasets are a separate supplementary evaluation. Videos are never committed. Data split by recording session, and the test set stays untouched until Phase 7.
- Training is optional and happens only in Phase 5 and Phase 6, after the rule-based baseline is measured.
- Stampede and gestures are the first candidates to ship as experimental.

## Open problems

- `evaluate.py` has not been shared yet.
- The thrown object detector uses a fixed confidence of 1.0 because the original script had none.
- The alert log folder is created before the video source is checked, so a bad path leaves an empty run folder.
- The room used for laptop camera tests is dimly lit. Real clips need good light.
- The clip `test_01.mp4` is compressed and portrait. Real recordings should be sent uncompressed and in landscape.
- Compatibility of the DirectShow fix on other systems is untested.
- Dataset licenses not fully verified: UMN (no license text on the page), Hockey Fight, Violent-Flows, XD-Violence. RWF-2000 videos are currently unavailable from the official site. HaGRIDv2 license text must be read before use.
- The README has no results yet.

## Next

Phase 2: improve the thrown object detector (blur, morphology, tracking across frames, cooldown on video time). First record 20 to 30 throws in varied conditions plus negative footage, with labeled time intervals.
## Phase 2 progress (2026-10-13)

- Added `stadiumguard/evaluation.py`: precision, recall, F1, false alarms per minute and mean delay. Checked against numbers computed by hand on two synthetic cases, including the case with zero alerts.
- Added `stadiumguard/annotations.py` and the annotation format: `data/annotations/<set>.csv` with columns `video,event_type,start_s,end_s`. Negative clips are not listed, and their duration is read from the video.
- Added `evaluate.py` in the repository root. It runs the real package over every clip in a folder without a window, reads the alert logs, and prints the metrics together with the thresholds used.
- The alert matching tolerance defaults to 1.0 second. It is a placeholder decision, not a measured value. Fix it after the real clips are recorded.
- The original `evaluate.py` was not found, so this one is new.

## Baseline (before any Phase 2 change)

Command: `python evaluate.py --videos data/dev --annotations data/annotations/dev.csv`

Thresholds: motion_threshold 25, motion_min_area 1500, cooldown 3.0 s, person confidence 0.25.

Result on `test_01.mp4` (one clip, one annotated throw): events 1, detected 0, alerts 0, false alarms 0, recall 0.0, precision and F1 not defined. The end time 5.6 s in `dev.csv` is a guess, but it does not matter here because there are no alerts. This is one clip, so it is not a performance claim.

## Next

Record the Phase 2 clips (throws with labeled times plus negative footage, uncompressed, landscape, good light), then run the first experiment: blur and morphology. Compare against the baseline above with the same command.

## Phase 2 baseline on the real development clips (2026-10-16)

Command: `python evaluate.py --videos data/dev --annotations data/annotations/dev.csv`

Thresholds: motion_threshold 25, motion_min_area 1500, cooldown 3.0 s, person confidence 0.25, tolerance 1.0 s.

Data: 5 clips with one annotated throw each (`throw_001` to `throw_005`) and 4 clips without a throw (`neg_001` to `neg_004`). All are iPhone clips, 1080x1920, about 60 fps, 4 to 7.4 seconds each. Annotated times are estimates read from frame grids at 0.1 to 0.4 second spacing.

Result: events 5, detected 4, alerts 10, false alarms 6, precision 0.4, recall 0.8, F1 0.533, false alarms per minute 6.699, mean delay 0.127 s.

This is a baseline for the original detector, not a performance claim. The sample is tiny. `neg_001` to `neg_003` may show the same scene recorded more than once.
