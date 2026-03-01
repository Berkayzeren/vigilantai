# Vigilant AI - Field Eye (Saha Gözü)

![Vigilant AI](https://img.shields.io/badge/AI-YOLOv8-blue.svg) ![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green.svg) ![Python](https://img.shields.io/badge/Language-Python-yellow.svg)

Vigilant AI is a real-time object detection and monitoring system built with Object-Oriented Programming (OOP) principles in Python, OpenCV, and the Ultralytics YOLOv8 engine. It acts as a "Field Eye" by connecting to remote camera streams (such as a mobile phone camera using iVCam) and performing high-speed, on-the-fly AI object detection with a built-in Head-Up Display (HUD).

## Architecture
The project is built with production-ready standards:
- **Modular OOP Design**: Clean, readable, and extensible core class (`VigilantCore`).
- **Environment Isolation**: Private values (IP addresses) are kept secure using `.env` files.
- **Graceful Shutdown**: Try-finally blocks guarantee the safe release of hardware resources in edge-cases preventing stalled ports.

## Features

- **Real-Time Object Detection**: Powered by the state-of-the-art YOLOv8 nano (`yolov8n.pt`).
- **Wireless Camera Integration**: Connects to IP cameras or mobile devices over Wi-Fi via HTTP video streaming.
- **Dynamic HUD**: Features an on-screen display showcasing system status, active monitoring mode, and real-time FPS counter.
- **Interactive Controls**: 
  - On-the-fly video rotation correction.
  - Seamless fullscreen toggling.

## Prerequisites

Ensure you have Python 3.8+ installed on your system.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/vigilantai.git
   cd vigilantai
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Duplicate the `.env.example` file and rename it to `.env`.
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and update the `KAMERA_ADRESI` variable with your camera's local IP address and stream path (or `0` for default webcam).
   ```env
   KAMERA_ADRESI="http://192.168.1.X:PORT/video"
   ```

## Usage

Run the core script using Python:

```bash
python vigilant_core.py
```

### Keyboard Shortcuts

- `r` : Rotate the camera feed (cycles through 0°, 90°, 180°, 270°).
- `f` : Toggle between fullscreen and windowed mode.
- `q` or `s` : Safely exit the application.

## Troubleshooting

- **Connection Error (`!!! BAĞLANTI HATASI !!!`)**: 
  - Ensure your phone and computer are on the exact same Wi-Fi network.
  - Verify that your IP camera application (like iVCam) is actively streaming.
  - Check your firewall settings.
- **ModuleNotFoundError ("No module named 'dotenv'")**: Make sure you ran `pip install -r requirements.txt`.

## License

This project is open-source and available under the MIT License.
