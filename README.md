# Multi-Angle Cow Face Data Collection

A simple Raspberry Pi GUI application to collect cow face images from **four different angles** using **4 USB webcams**. The system provides live preview, alignment assistance, and synchronized multi-camera image capture.

## 📷 Features

- **Live Preview** from each camera with alignment box
- **Auto cow ID management** and image folder organization
- **Simultaneous image capture** from 4 webcams using multithreading
- **GUI interface** for previewing, directory creation, and data capture

## 🐮 Use Case

Designed for collecting facial images of cows from different angles for machine learning datasets (e.g., face recognition, behavior analysis).

## 💻 Requirements

- Raspberry Pi 4 (or similar)
- 4 USB cameras (accessible via `/dev/video0`, `/dev/video2`, etc.)
- Python 3 with the following packages:
  - `opencv-python`
  - `Pillow`
  - `tkinter` (usually pre-installed)

Install required Python packages:
```bash
pip install opencv-python Pillow
```

## 🗂 Directory Structure
Captured images are saved under:

```swift
/home/pi/Desktop/NTU20250509/<cow_id>/
```
Each image is named with a timestamp, e.g.:
```cam1_20250509_142301_123456.jpg```

## 🚀 Usage
Run the script:

```bash
python multi-angle_cap.py
```
1. Click Create Directory to assign a new cow ID and folder.
2. Click Show Initial View to verify camera alignment.
3. Click Capture Images to capture 60 images per camera.

Images will be saved to the current cow's directory.

## 📦 Files
* `multi-angle_cap.py` – main GUI app for capture
* `camera_alignment_gui.py` – alternate GUI for camera preview and alignment (optional)
* `cow_id.txt` – stores the current cow ID for auto-increment

## 🧹 Cleanup
The app automatically releases all camera resources on exit.

## Credits:
Thanks to Ian for the HW design and Chuck for the idea💡
