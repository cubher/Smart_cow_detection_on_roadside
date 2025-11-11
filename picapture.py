import time
import base64
import requests
import numpy as np
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter
from PIL import Image

# --- CONFIG ---
MODEL_PATH = "cow_model.tflite"
IMG_PATH = "capture.jpg"
IMG_SIZE = (64, 64)
DELAY_SEC = 15
API_URL = "http://10.181.159.160:8080/iot_monitor/api/cow.php"
API_KEY = "K72E1D4G1GFUC4VZ"

# --- LOAD MODEL ---
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# --- CAMERA SETUP ---
picam2 = Picamera2()
picam2.start()

def predict_image(image_path):
    img = Image.open(image_path).convert("L")
    img = img.resize(IMG_SIZE)
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=(0, -1))
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return np.argmax(output_data)

def send_to_api(image_path):
    try:
        with open(image_path, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode("utf-8")

        data = {
            "api_key": API_KEY,
            "value": b64_image,
            "source": "raspi_cam1"
        }

        print("🐄 Cow Detected! Sending image to API...")
        response = requests.post(API_URL, data=data, timeout=10)
        if response.status_code == 200:
            print("✅ API Response:", response.json())
        else:
            print(f"⚠️ API call failed: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Error sending to API:", e)

# --- LOOP ---
print("🚀 Starting live detection (every 15 sec)... Press Ctrl+C to stop.")
while True:
    try:
        picam2.capture_file(IMG_PATH)
        result = predict_image(IMG_PATH)
        if result == 0:
            print("❌ Not Cow")
        else:
            send_to_api(IMG_PATH)
        time.sleep(DELAY_SEC)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
        break