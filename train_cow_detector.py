import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Paths
train_dir = "dataset/train"
test_dir = "dataset/test"

# Parameters
img_height = 64
img_width = 64
batch_size = 32

# Load datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode="grayscale"
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode="grayscale"
)

# Normalize images (0-1 range)
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))

# Define a tiny CNN
model = models.Sequential([
    layers.Conv2D(8, (3, 3), activation='relu', input_shape=(img_height, img_width, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(16, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(32, activation='relu'),
    layers.Dense(2, activation='softmax')  # cow vs notcow
])

# Compile
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train
history = model.fit(train_ds, validation_data=test_ds, epochs=15)

# Evaluate
loss, acc = model.evaluate(test_ds)
print(f"✅ Test Accuracy: {acc:.2f}")

# Save Keras model
model.save("cow_cnn_model.h5")

# Convert to TFLite with quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("cow_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Model training complete! Saved as cow_model.tflite")
