# 🎹 Virtual Camera Keyboard (Freehands)

A **virtual keyboard controlled with your hand and a webcam**.  
No physical keyboard needed — just move your hand in front of the camera to type letters on a virtual QWERTY layout.  

## ✨ Features
- 🖐️ **Hand tracking** powered by [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker).
- 🎯 Two typing modes:  
  - **Pinch Mode** → bring your index finger and thumb together to press a key.  
  - **Hover Mode** → hold your fingertip over a key for ~1 second to type.  
- ⌨️ On-screen QWERTY keyboard with special keys (Space, Backspace).  
- 📝 Real-time display of typed text.  
- ⏩ (Optional) Send keystrokes directly to other apps using **PyAutoGUI**.  

## 🖼️ How It Works
1. The webcam feed is captured with OpenCV.  
2. MediaPipe detects **21 hand landmarks** in real time.  
3. The program tracks your **index fingertip** (landmark 8) and optionally your **thumb tip** (landmark 4).  
4. If your fingertip overlaps a key and you pinch/hover, that key is pressed.  
5. Typed text is displayed at the top of the screen or sent to the OS.  

## 🚀 Installation
```bash
# Clone this repo
git clone https://github.com/naz-02/Virtual-Keyboard-Freehands.git
cd Virtual-Keyboard-Freehands

# (Optional) Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
