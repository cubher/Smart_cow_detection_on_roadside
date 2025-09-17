import os
import random
import numpy as np
import tensorflow as tf
# from tensorflow.keras.preprocessing import image
from tensorflow import keras
from tensorflow.keras.preprocessing import image


# Paths
model_path = "cow_model.tflite"
dataset_dir = "dataset"
class_names = ["cow", "notcow"]
img_height, img_width = 64, 64

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Collect 50 random images
all_images = []
for cls in class_names:
    folder = os.path.join(dataset_dir, "train", cls)
    files = [(os.path.join(folder, f), cls) for f in os.listdir(folder)]
    all_images.extend(files)

random.shuffle(all_images)
sampled_images = all_images[:50]

# Evaluate
correct = 0
for img_path, actual_cls in sampled_images:
    img = image.load_img(img_path, target_size=(img_height, img_width), color_mode="grayscale")
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32) / 255.0

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    pred_class = class_names[np.argmax(output_data[0])]
    confidence = np.max(output_data[0]) * 100

    if pred_class == actual_cls:
        correct += 1

    print(f"🖼️ {img_path} → Pred: {pred_class} ({confidence:.2f}%) | Actual: {actual_cls}")

accuracy = correct / len(sampled_images) * 100
print(f"\n✅ Tested {len(sampled_images)} images | Accuracy: {accuracy:.2f}%")
