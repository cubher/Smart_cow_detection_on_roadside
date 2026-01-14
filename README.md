# 🐄 Smart Cow Detection on Roadside (Edge AI)

An **Edge AI–based roadside animal detection system** that performs **real-time cow detection directly on a Raspberry Pi** using a lightweight **CNN deployed with TensorFlow Lite**.  
The system performs **on-device inference**, minimizing latency and bandwidth usage, and reports detections to a **centralized web dashboard** via an HTTP API.

This project is designed as a **production-oriented embedded AI system**, not just a research prototype.

---

## 🔧 System Overview

**Pipeline:**

Camera → Image Preprocessing → CNN Inference (TFLite) → Event Filtering → HTTP API → Web Dashboard

**Key Design Goals**
- Edge-first inference (no cloud dependency)
- Low compute & memory footprint
- Deterministic behavior on embedded Linux
- Scalable multi-node deployment

---

## 🧠 ML Model Architecture

**Task:** Binary image classification (`cow` / `not_cow`)

**Input**
- 64×64 grayscale images
- Normalized to [0,1]

**CNN Architecture**
```
Conv2D (8 filters, 3×3, ReLU)
→ MaxPooling2D (2×2)
→ Conv2D (16 filters, 3×3, ReLU)
→ MaxPooling2D (2×2)
→ Flatten
→ Dense (32, ReLU)
→ Dense (2, Softmax)
```

**Training**
- Framework: TensorFlow / Keras
- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Epochs: 15

**Deployment**
- Converted to TensorFlow Lite
- Post-training quantization enabled
- Optimized for ARMv8 (Raspberry Pi 4)

---

## 📊 Dataset Preparation

**Source**
- COCO Dataset (filtered for cow class)
- Additional open-source images

Refer: https://cocodataset.org/

**Structure**
```
dataset/
 ├── train/
 │   ├── cow/
 │   └── notcow/
 └── test/
     ├── cow/
     └── notcow/
```

**Split**
- Training: 80%
- Testing: 20%

Automated dataset filtering and splitting performed using Python scripts.

---

## 🍓 Edge Deployment (Raspberry Pi)

**Hardware**
- Raspberry Pi 4 Model B
- Raspberry Pi Camera Module
- 32GB MicroSD
- 5V / 3A Power Supply

**Software**
- Raspberry Pi OS (64-bit)
- Python 3
- TensorFlow Lite Runtime
- Picamera2 / libcamera

**Inference Loop**
- Capture image every 15 seconds
- Resize & normalize
- Run TFLite inference
- If `cow` detected → send event to server

**Performance**
- ~5 FPS inference capability
- Stable long-running operation

---

## 🌐 Backend & Dashboard

**Backend**
- PHP REST API
- MySQL / MariaDB
- Stores:
  - Base64 encoded image
  - Timestamp
  - Source ID

**Frontend**
- HTML + CSS
- Displays latest detections
- Lightweight & mobile-friendly

---

## 🔐 Embedded System Fixes & Optimizations

To ensure camera + TFLite stability:

**DMA Heap Permissions**
```
SUBSYSTEM=="dma_heap", GROUP="video", MODE="0660"
```

**User Permissions**
```
sudo usermod -aG video $USER
```

**GPU Memory Allocation**
```
dtoverlay=vc4-kms-v3d,cma-384
```

These fixes eliminate camera initialization and memory allocation issues during inference.

---

## 📈 Results

- Reliable cow detection in roadside environments
- Low false positives after threshold tuning
- Stable end-to-end IoT data flow
- Real-time monitoring via dashboard

---

## 🚀 Applications

- Roadside animal accident prevention
- Smart city surveillance nodes
- Livestock monitoring systems
- Edge AI safety infrastructure
