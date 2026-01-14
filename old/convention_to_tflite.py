import tensorflow as tf

# Load your trained .h5 model
model = tf.keras.models.load_model("cow_cnn_model.h5")

# Create a converter
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Ensure compatibility with the Pi runtime
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,       # Use only built-in ops
    tf.lite.OpsSet.SELECT_TF_OPS          # Include TF ops if needed
]
converter._experimental_lower_tensor_list_ops = False

# Convert
tflite_model = converter.convert()

# Save the TFLite model
with open("cow_cnn.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Conversion done: model_pi_compatible.tflite")