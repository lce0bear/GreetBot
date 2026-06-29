import cv2
import numpy as np
import threading
import time
from google import genai
from google.genai import types
import serial
import os
from gtts import gTTS
# import speech_recognition as sr # Commented out due to exhibition hardware failure

# Init Gemini API - MUST USE ENV VARIABLE OR PLACEHOLDER FOR GITHUB!
client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")

prompt_context = """
You are Greetbot, the official AI Assistant and interactive guide for the Electronics and Communication Engineering (ECE) Department at FISAT (Federal Institute of Science And Technology) located in Kerala.
Project Creators: Mr. Amarjith, Mr. Abel Sebastian, Mr. Albert Chery George, and Ms. Aslaha Shaji.
Guide: Ms. Dhanya S.
Event: S6 B-Tech ECE Mini-Project Exhibition (2019 KTU Scheme).

Instructions:
1. Use live Google Search for facts about FISAT's history, faculty, placements, or syllabus.
2. Act as a polite, welcoming robotic host. 
3. KEEP ANSWERS SHORT (1-2 sentences max) so the TTS doesn't lag.
"""

# Globals for state machine
face_visible = False
face_width = 0
ai_state = "SEARCHING"  
TARGET_WIDTH = 105      
TOO_CLOSE_WIDTH = 160   
shutdown_system = False

print("Waking up Greetbot...")

# Uploading knowledge base files
docs = [
    "Fisat-Hand-book-25-2026.pdf", "Annual-Report-2023-24.pdf",
    "Innovation-NIRF-2025.pdf", "MCA-24-25-prospectus.pdf",
    "M.Tech-Prospectus-2025.pdf", "patents.txt"
]

uploaded_docs = []
for d in docs:
    if os.path.exists(d):
        print(f"Loading {d} into brain...")
        uploaded_docs.append(client.files.upload(file=d))
    else:
        print(f"Warning: {d} not found, skipping.")

# Setup chat session
if uploaded_docs:
    uploaded_docs.append("Use these documents as your primary source of truth.")
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=prompt_context, tools=[{"google_search": {}}]),
        history=[{"role": "user", "parts": uploaded_docs}]
    )
else:
    print("Running in Search-Only mode (No local docs).")
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=prompt_context, tools=[{"google_search": {}}])
    )

# Try connecting to Arduino (Change port if needed: /dev/ttyACM0, /dev/ttyUSB0, etc.)
try:
    esp32 = serial.Serial('/dev/ttyACM0', 115200, timeout=1) 
    print("Arduino linked on /dev/ttyACM0")
except Exception as e:
    print(f"Arduino comms failed. Running headless test mode. ({e})")
    esp32 = None

def talk(text):
    print(f"\n[GREETBOT]: {text}")
    try:
        # Generate and play audio on the fly
        tts = gTTS(text=text, lang='en-in', slow=False)
        tts.save("reply.mp3")
        os.system("mpg123 -q reply.mp3")
    except Exception as e:
        print(f"Audio crash: {e}")

# Teleoperation override for exhibition
def get_user_audio():
    try:
        print("\n" + "-"*30)
        print(">> MIC OVERRIDE: Type question below")
        text_in = input(">> ")
        return text_in if text_in.strip() != "" else None
    except KeyboardInterrupt:
        return 'shut down'
    except Exception:
        return None

def motor_logic_thread():
    global face_visible, face_width, ai_state, shutdown_system
    
    while not shutdown_system:
        if ai_state == "SEARCHING":
            if face_visible:
                # Target acquired, jump to approach logic
                ai_state = "APPROACHING"
                print("\nFace detected. Calculating distance...")
                    
        elif ai_state == "APPROACHING":
            if not face_visible:
                if esp32: esp32.write(b'S')
                ai_state = "SEARCHING"
                
            elif face_width >= TARGET_WIDTH and face_width < TOO_CLOSE_WIDTH:
                # Perfect talking distance
                if esp32: esp32.write(b'S')
                ai_state = "CONVERSING"
                
            elif face_width >= TOO_CLOSE_WIDTH:
                # Too close, back away
                if esp32: esp32.write(b'B')
                
            else:
                # Too far, move in
                if esp32: esp32.write(b'F')
                
        elif ai_state == "CONVERSING":
            talk("Hi, I am Greetbot. How may I assist you today?")
            
            user_text = get_user_audio()
            
            if not user_text:
                if esp32:
                    esp32.write(b'B')
                    time.sleep(1.5)  
                    esp32.write(b'S')
                ai_state = "SEARCHING"
                continue
            
            if 'shut down' in user_text.lower() or 'quit' in user_text.lower():
                talk("Shutting down systems. Have a good day!")
                shutdown_system = True
                break
                
            try:
                reply = chat.send_message(user_text)
                talk(reply.text)
            except Exception as e:
                print(f"Gemini API Error: {e}")
            
            # Reset position after conversation
            if esp32:
                esp32.write(b'B')
                time.sleep(1.5)
                esp32.write(b'S')
                
            time.sleep(2)
            ai_state = "SEARCHING"
            
        time.sleep(0.1)

# Start brain thread
thread = threading.Thread(target=motor_logic_thread, daemon=True)
thread.start()

# Initialize vision model
print("Loading SSD MobileNet...")
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
time.sleep(2) 

# Main loop for camera
while not shutdown_system:
    ret, frame = cap.read()
    if not ret: break
    
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    
    found_face = False
    curr_width = 0
    
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence >= 0.5:
            found_face = True
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            curr_width = endX - startX
            
            color = (0, 255, 0) if ai_state == "SEARCHING" else (0, 165, 255) if ai_state == "APPROACHING" else (0, 0, 255)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.putText(frame, f"W: {curr_width}px | {ai_state}", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

    face_visible = found_face
    face_width = curr_width
    
    cv2.imshow("Greetbot Vision", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()