import sys

import cv2


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    capture = cv2.VideoCapture(index)
    if not capture.isOpened():
        print(f"Could not open camera {index}")
        return 1
    ok, frame = capture.read()
    capture.release()
    if not ok:
        print(f"Camera {index} opened but returned no frame")
        return 1
    height, width = frame.shape[:2]
    print(f"Camera {index} OK: {width}x{height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
    