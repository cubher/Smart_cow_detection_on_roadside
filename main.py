import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Path to your dataset
data_dir = "/images"

# Parameters
img_height = 64
img_width = 64
batch_size = 32

# Load dataset (auto-labels based on folder names)
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,   # 80% train, 20% validation
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode="grayscale"  # use grayscale to reduce memory
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode="grayscale"
)

# Normalize images (0-1 range)
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Define a tiny CNN
model = models.Sequential([
    layers.Conv2D(8, (3, 3), activation='relu', input_shape=(img_height, img_width, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(16, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(32, activation='relu'),
    layers.Dense(2, activation='softmax')  # cow vs not_cow
])

# Compile model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20
)

# Save model
model.save("cow_cnn_model.h5")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # quantization
tflite_model = converter.convert()

with open("cow_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Training complete! Model saved as cow_model.tflite")
