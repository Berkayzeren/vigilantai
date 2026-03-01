# Vigilant AI - Field Eye (Saha Gözü)

![Vigilant AI](https://img.shields.io/badge/AI-YOLOv8-blue.svg) ![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green.svg) ![Python](https://img.shields.io/badge/Language-Python-yellow.svg)

Vigilant AI is a real-time object detection and monitoring system built with Python, OpenCV, and the Ultralytics YOLOv8 engine. It is designed to act as a "Field Eye" by connecting to remote camera streams (such as a mobile phone camera using iVCam) and performing high-speed, on-the-fly AI object detection with a built-in Head-Up Display (HUD).

## Features

- **Real-Time Object Detection**: Powered by the state-of-the-art YOLOv8 nano (`yolov8n.pt`) model for high performance and accuracy.
- **Wireless Camera Integration**: Connects to IP cameras or mobile devices over Wi-Fi via HTTP video streaming.
- **Dynamic HUD**: Features an on-screen display showcasing system status, active monitoring mode, and real-time FPS counter.
- **Interactive Controls**: 
  - On-the-fly video rotation correction.
  - Seamless fullscreen toggling.
- **Robust Error Handling**: Built-in connection troubleshooting and library dependency checks.

## Prerequisites

Ensure you have Python 3.x installed on your system. You will also need to install the following dependencies:

```bash
pip install opencv-python ultralytics
```

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/vigilantai.git
   cd vigilantai
   ```

2. **Download YOLOv8 Weights:**
   The script uses `yolov8n.pt`. If it is not present in the directory, the `ultralytics` library will attempt to download it automatically upon the first run.

3. **Configure Camera Source:**
   Open `vigilant_core.py` and update the `KAMERA_ADRESI` variable with your camera's local IP address and stream path (e.g., from iVCam or any IP Webcam app).
   ```python
   KAMERA_ADRESI = "http://192.168.1.X:PORT/video"
   ```

## Usage

Run the core script using Python:

```bash
python vigilant_core.py
```

### Keyboard Shortcuts

While the monitoring window is active, you can use the following keys:
- `r` : Rotate the camera feed (cycles through 0°, 90°, 180°, 270°).
- `f` : Toggle between fullscreen and windowed mode.
- `q` or `s` : Safely exit the application.

## Troubleshooting

- **Connection Error (`!!! BAĞLANTI HATASI !!!`)**: 
  - Ensure your phone and computer are on the exact same Wi-Fi network.
  - Verify that your IP camera application (like iVCam) is actively streaming.
  - Check your firewall settings to ensure the port isn't being blocked.
- **Model Loading Error**: Ensure the `ultralytics` package is correctly installed.

## License

This project is open-source and available under the MIT License.
