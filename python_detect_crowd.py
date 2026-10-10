import cv2
import numpy as np
from ultralytics import YOLO
import winsound
import tkinter as tk
from tkinter import messagebox
import time

# ---- Alert setup ----
root = tk.Tk()
root.withdraw()

# Cooldown to prevent the alert from firing on every single frame (in seconds)
ALERT_COOLDOWN = 3
last_alert_time = 0


def send_alert():
    global last_alert_time
    now = time.time()
    if now - last_alert_time < ALERT_COOLDOWN:
        return  # Still within cooldown period, skip this alert
    last_alert_time = now
    winsound.Beep(1000, 500)
    messagebox.showwarning("Alert!", "A non-human object was thrown!")


# ---- Load YOLOv8 model ----
model = YOLO("yolov8n.pt")  # lightweight version

# ---- Open the camera ----
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: could not open the camera")
    exit()

ret, prev_frame = cap.read()
if not ret:
    print("Error reading the first frame")
    exit()


# ---- Function to detect moving objects ----
def detect_non_human_objects(prev_frame, frame, min_area=1500):
    # Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Difference between frames
    diff = cv2.absdiff(prev_gray, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    moving_objects = []
    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            moving_objects.append((x, y, w, h))
    return moving_objects


# ---- Main loop ----
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame from camera")
        break

    # Detect people using YOLO
    results = model(frame)
    annotated_frame = results[0].plot()

    # Store bounding boxes of detected people
    human_boxes = []
    for det in results[0].boxes.data:
        x1, y1, x2, y2, conf, cls_id = det
        if int(cls_id) == 0:  # 0 = person
            human_boxes.append((int(x1), int(y1), int(x2), int(y2)))

    # Detect non-human moving objects
    moving_objects = detect_non_human_objects(prev_frame, frame)
    for (x, y, w, h) in moving_objects:
        # Ignore any moving object that overlaps a person's bounding box
        # (treated as normal human movement)
        overlap = False
        for (hx1, hy1, hx2, hy2) in human_boxes:
            if x < hx2 and x + w > hx1 and y < hy2 and y + h > hy1:
                overlap = True
                break

        if not overlap:
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                annotated_frame,
                "Alert!",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )
            send_alert()  # Trigger sound + warning popup

    prev_frame = frame.copy()
    cv2.imshow("Stadium Security", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
