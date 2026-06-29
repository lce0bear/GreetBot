

# 🤖 Greetbot: Autonomous Edge-AI Interactive Guide

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-000000?style=for-the-badge&logo=espressif&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_LLM-8E75B2?style=for-the-badge&logo=google&logoColor=white)

Greetbot is an autonomous, interactive robotic assistant designed for the Electronics and Communication Engineering (ECE) Department at the Federal Institute of Science And Technology (FISAT).

It utilizes a Master-Slave edge-computing architecture to autonomously detect humans, approach them to an optimal conversational distance using bounding-box depth estimation, and answer complex department-specific questions via a custom RAG (Retrieval-Augmented Generation) pipeline powered by the Gemini 2.5 Flash LLM.

<p align="center">
  <img src="https://github.com/lce0bear/GreetBot/blob/main/GREETBOT.png?raw=true" alt="Greetbot in action" width="600"/>
</p>

## 🚀 Key Features
* **Autonomous Face Tracking:** Utilizes a ResNet-10 SSD Caffe model deployed via OpenCV to detect and track human faces in real-time.
* **Kinematic Depth Estimation:** Calculates proximity based inversely on bounding-box pixel width (105px to 160px target zone) to dynamically adjust motor movement (Forward, Backward, Stop).
* **Multi-Threaded State Machine:** Isolates AI visual-spatial cognition from motor logic to prevent system latency and ALSA audio blocking.
* **Domain-Specific LLM Brain:** Answers are strictly grounded in institutional knowledge (prospectuses, faculty lists, innovation reports) using Gemini's File API.
* **Master-Slave Architecture:** A Raspberry Pi 4 handles high-level Python/AI processing and sends UART serial commands to an Arduino UNO handling low-level L298N motor PWM signals.

## 🛠️ Hardware Architecture
* **Master Node:** Raspberry Pi 4 Model B (Handles Vision, LLM API, TTS, and FSM Logic)
* **Slave Node:** Arduino UNO (Handles Motor Logic via Hardware Serial /dev/ttyACM0)
* **Motor Driver:** L298N Dual H-Bridge
* **Sensors:** Standard USB Webcam
* **Chassis:** Differential Drive (4-Wheel)

## 📁 Repository Structure
* `/arduino_firmware/` - Contains the `.ino` C++ code flashed to the Arduino.
* `/knowledge_base/` - Institutional PDFs and text files used to ground the LLM.
* `/vision_models/` - OpenCV deployment prototxt and pre-trained SSD caffemodel weights.
* `greetbot_master_final.py` - The main Python execution script.

## ⚙️ Setup and Installation

### 1. Install Dependencies
Ensure you are running Python 3.9+. Install the required libraries on your Raspberry Pi:
```bash
pip install -r requirements.txt
```

### 2. API Key Configuration
You must set your Gemini API key as an environmental variable to run the LLM brain securely:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Run the Robot
Ensure the Arduino is connected via USB to the Pi and the USB camera is active, then execute:
```bash
python3 greetbot_master_final.py
```

## 👨‍💻 Project Creators

* Mr. Amarjith
* Mr. Abel Sebastian
* Mr. Albert Chery George
* Ms. Aslaha Shaji
* **Project Guide:** Ms. Dhanya S.

Developed for the S6 B-Tech ECE Mini-Project Exhibition (2019 KTU Scheme) at FISAT.
