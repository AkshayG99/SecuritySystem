# Arduino Home Security System

A proximity-triggered security prototype connecting an Arduino ultrasonic sensor to a Python webcam capture script. When an object is detected within 10 cm, the Arduino activates LED and speaker outputs and signals the computer to save a timestamped image.

## How it works

1. The Arduino measures distance using an ultrasonic sensor.
2. A reading below 10 cm sets the LED and speaker outputs HIGH and sends `1` over USB serial. Other readings send `0`.
3. Python reads the serial signal and saves an image from the default webcam when it receives `1`.
4. Images are stored in `captured_images/` with timestamped filenames.

The Arduino samples approximately once per second. Python waits one second between iterations; serial reads can add up to five seconds.

## Hardware

- Arduino-compatible board and USB cable
- Trigger/echo ultrasonic distance sensor
- LED with a suitable current-limiting resistor
- Compatible buzzer or speaker module, with a driver if required
- Computer with a webcam
- Breadboard and jumper wires

### Pin assignments

| Signal | Arduino pin |
| --- | --- |
| Ultrasonic echo | D7 |
| Ultrasonic trigger | D8 |
| LED output | D2 |
| Speaker/buzzer output | D3 |
| Additional output, held HIGH | D6 |

Use the correct power, ground, and signal levels for your board and components. The sketch drives D6 HIGH, but its physical purpose is not documented in this repository.

## Setup

### 1. Upload the Arduino sketch

Open `summative2.ino` in the Arduino IDE. If prompted, move it into a sketch folder named `summative2`. Select your board and port, then upload it.

Close the Arduino Serial Monitor before running Python so it does not occupy the serial port.

### 2. Install Python dependencies

Use Python 3 with a local desktop session that supports OpenCV windows.

```bash
git clone https://github.com/AkshayG99/ArduinoHomeSecuritySystem.git
cd ArduinoHomeSecuritySystem
python3 -m venv .venv
source .venv/bin/activate
python -m pip install opencv-python pyserial
```

On Windows, activate the environment with `.venv\Scripts\activate`.

### 3. Configure the serial port

In `all.py`, replace `/dev/tty.usbserial-14110` with the port shown in the Arduino IDE. Keep the baud rate at `9600` to match the sketch. Windows ports may look like `COM3`.

The script uses camera index `0`; change `cv2.VideoCapture(0)` if your intended webcam uses another index.

### 4. Start capturing

```bash
python all.py
```

Allow camera access if prompted. Move an object within 10 cm of the sensor, then check `captured_images/` for saved JPEGs. Press **Ctrl+C** in the terminal to stop.

## Repository files

| File | Purpose |
| --- | --- |
| `summative2.ino` | Distance measurement, LED/speaker outputs, and serial signaling |
| `all.py` | Serial input, webcam capture, image storage, and brief image display |

## Current limitations

- Serial connection or parsing errors default to `person = 1`, so images can be captured even when the Arduino is disconnected.
- The sensor detects nearby objects; it does not identify people.
- Capturing continues while the input is `1`; there is no one-shot trigger or cooldown.
- The speaker output uses a steady digital HIGH rather than an audio waveform; sound depends on the hardware.
- There is no network notification, authentication, or remote dashboard.

This is a local hardware/software prototype. Images remain in the local capture directory.
