# Project State

Last updated: 2026-10-11

## Current phase

Phase 0 (repo cleanup) is complete. Phase 1 (package structure) has not started.

## Done

- Extracted the zip, renamed the files to `requirements.txt` and `.gitignore`, removed the zip.
- Extended `.gitignore` for virtual environments, videos, model weights, run outputs and `.env`.
- Created a virtual environment `.venv` with Python 3.12.1.
- Installed opencv-python 5.0.0 and numpy 2.5.4 in the environment and checked the import.
- Added `test_camera.py`. Result on the laptop camera: `Camera 0 OK: 640x480`.
- Added the AGPL-3.0 `LICENSE`.

## Evidence

- `git ls-files` lists: `.gitignore`, `LICENSE`, `README.md`, `python_detect_crowd.py`, `requirements.txt`, `test_camera.py`.
- HEAD is `d2704f5` and the working tree is clean.

## Decisions

- Python 3.12 for this project. Python 3.13.1 is also installed and is the system default. Reason: the MediaPipe release I checked does not list 3.13 as supported, and MediaPipe is needed in Phase 6.
- License: AGPL-3.0 instead of MIT. Reason: Ultralytics is licensed under AGPL-3.0 or a paid Enterprise license. The owner accepts that others may use and modify the code. Review again before Phase 8.
- Test material: video files recorded on an iPhone (H.264, 1080p, 30 fps, fixed mount), medium to close entrance-style view. Public datasets are used only as a separate supplementary evaluation, never mixed into the main results table.
- Data split by recording session. The test set stays untouched until Phase 7.
- Raw videos are never committed. Participants are adults who gave consent. Faces are blurred in any published media.
- Stampede and gestures are the first candidates to ship as experimental.

## Open problems

- `evaluate.py` has not been shared yet.
- The number and content of the existing test videos are not known yet.
- `requirements.txt` has no version pins. Pin after tested installs.
- Compatibility of OpenCV 5.0.0 with Ultralytics is not verified.
- `python_detect_crowd.py` is unchanged: Windows only, blocking Tkinter popup, camera 0 only.
- Dataset licenses not fully verified: UMN (no license text on the page), Hockey Fight, Violent-Flows, XD-Violence. RWF-2000 videos are currently unavailable from the official site and need a signed agreement. HaGRIDv2 license text must be read before use.
- The README has no results yet.

## Next

Phase 1: split the script into a package with configuration, video source, detectors, alert manager and a CLI entry point.
