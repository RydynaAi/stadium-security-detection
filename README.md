# stadium-security-detection
Real-time stadium security system using YOLOv8 and OpenCV — detects people via object detection, flags non-human moving objects (e.g. thrown items) that don't overlap with a detected person, and triggers a sound + popup alert.
<div align="center">

# 🏟️ Stadium Security Detection

### Real-time detection of thrown objects in a crowd using YOLOv8 and OpenCV

<p>
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/YOLOv8-Object%20Detection-00FFFF" alt="YOLOv8"/>
  <img src="https://img.shields.io/badge/Ultralytics-YOLO-purple" alt="Ultralytics"/>
</p>

</div>

---

## 📖 About

<p>
This project is a real-time <b>stadium security system</b> that monitors a live camera feed to detect
<b>non-human objects thrown into a crowd</b> (e.g. bottles, flares, or other items). It combines
<b>YOLOv8</b> for person detection with a frame-difference technique to spot movement, then flags any
moving object that does <i>not</i> overlap with a detected person as a potential thrown object — triggering
an audio alert and an on-screen warning popup.
</p>

<table>
<tr>
  <td><b>🎯 Detection Model</b></td>
  <td>YOLOv8 (nano version, <code>yolov8n.pt</code>)</td>
</tr>
<tr>
  <td><b>🎥 Input</b></td>
  <td>Live camera feed (webcam / connected camera)</td>
</tr>
<tr>
  <td><b>⚠️ Alert Method</b></td>
  <td>Audio beep + warning popup, with a cooldown to prevent spam</td>
</tr>
</table>

---

## ✨ Features

<ul>
  <li>🧍 Real-time person detection using YOLOv8</li>
  <li>🎯 Frame-difference based motion detection to catch any moving object</li>
  <li>🚫 Filters out normal human movement — only flags motion that doesn't overlap a detected person</li>
  <li>🔔 Audio + visual alert when a suspicious object is detected</li>
  <li>⏱️ Alert cooldown to avoid repeated triggers while the object is still in frame</li>
</ul>

---

## 🗂️ Project Structure

<pre>
stadium-security-detection/
├── python_detect_crowd.py   # Main detection script
├── test_camera.py           # Simple script to verify the camera works
├── requirements.txt
├── .gitignore
└── README.md
</pre>

---

## 🛠️ Tech Stack

<table>
<tr><th>Layer</th><th>Technology</th></tr>
<tr><td>Object Detection</td><td>YOLOv8 (Ultralytics)</td></tr>
<tr><td>Video / Image Processing</td><td>OpenCV</td></tr>
<tr><td>Numerical Operations</td><td>NumPy</td></tr>
<tr><td>Alerts</td><td>winsound (audio), tkinter (popup)</td></tr>
</table>

---

## ⚡ Getting Started

### Prerequisites
- Python 3.11
- A connected camera (webcam)
- Windows (the alert sound uses the built-in <code>winsound</code> module)

### 1. Clone the repository
<pre>
git clone https://github.com/RydynaAi/stadium-security-detection.git
cd stadium-security-detection
</pre>

### 2. Install dependencies
<pre>
pip install -r requirements.txt
</pre>

### 3. Test the camera (optional but recommended)
<pre>
python test_camera.py
</pre>

### 4. Run the detection system
<pre>
python python_detect_crowd.py
</pre>
<p>Press <code>q</code> at any time to quit. The YOLOv8 weights (<code>yolov8n.pt</code>) will be downloaded automatically on first run.</p>

---

## ⚙️ How It Works

<table>
<tr><th>Step</th><th>Description</th></tr>
<tr><td>1. Person Detection</td><td>Each frame is passed through YOLOv8 to locate all people (class 0)</td></tr>
<tr><td>2. Motion Detection</td><td>The current and previous frames are compared to detect any moving regions</td></tr>
<tr><td>3. Overlap Check</td><td>Each moving region is checked against detected person boxes</td></tr>
<tr><td>4. Alert</td><td>If a moving object does not overlap any person, it's flagged and an alert is triggered</td></tr>
</table>

---

## 👤 Author

<p>Rudyna Al-Qarni</p>

---

<div align="center">
Made with 🎥 and Python
</div>
