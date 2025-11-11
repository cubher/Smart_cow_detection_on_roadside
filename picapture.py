import time
import numpy as np
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter
from PIL import Image

# --- CONFIG ---
MODEL_PATH = "cow_model.tflite"
IMG_PATH = "capture.jpg"
IMG_SIZE = (64, 64)
DELAY_SEC = 15

# --- LOAD MODEL ---
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# --- CAMERA SETUP ---
picam2 = Picamera2()
picam2.start()

def predict_image(image_path):
    img = Image.open(image_path).convert("L")  # grayscale
    img = img.resize(IMG_SIZE)
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=(0, -1))  # shape (1, 64, 64, 1)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(output_data)
    return prediction

# --- LOOP ---
print("🚀 Starting live detection (every 15 sec)... Press Ctrl+C to stop.")
while True:
    try:
        picam2.capture_file(IMG_PATH)
        result = predict_image(IMG_PATH)
        if result == 0:
            print("❌ Not Cow")
        else:
            print("🐄 Cow Detected!")
        time.sleep(DELAY_SEC)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
        break