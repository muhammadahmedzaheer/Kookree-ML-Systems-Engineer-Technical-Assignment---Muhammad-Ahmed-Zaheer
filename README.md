# Kookree-ML-Systems-Engineer-Technical-Assignment---Muhammad-Ahmed-Zaheer

A complete deep learning microservice pipeline for real-time image classification using PyTorch and gRPC, deployed inside Docker containers and integrated with Redpanda (Kafka-compatible) for streaming simulation.

---

## 📦 Project Structure

```
.
├── client.py               # Simple client to test gRPC server
├── consumer.py             # Kafka consumer that calls gRPC inference
├── producer.py             # Kafka producer that streams video frames
├── server.py               # gRPC server exposing inference and healthcheck
├── model.py                # PyTorch ResNet18 model with preprocessing
├── load_test.py            # gRPC load test script
├── inference_pb2.py        # Generated protobuf classes
├── inference_pb2_grpc.py   # Generated protobuf gRPC classes
├── imagenet_classes.json   # Class label mapping
├── Dockerfile              # Multi-stage build
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ Prerequisites

- Make sure **Docker Desktop / Docker Engine** is installed and **running**.
- It’s recommended to run this project in **Visual Studio Code** for a better development and debugging experience.
- Python 3.8+ environment (virtual environment suggested)

---

## 🚀 How to Run

### 1. Build Docker Image for gRPC Server
```bash
docker build -t kookree-inference .
```

### 2. Run the Docker Container
```bash
docker run -p 50051:50051 kookree-inference
```

### 3. Start Redpanda Kafka Broker
Make sure you replace the IP address with your local IP (e.g., `192.168.18.75`):

```bash
docker run -d --name redpanda -p 9092:9092 -p 9644:9644 redpandadata/redpanda:latest redpanda start --overprovisioned --smp 1 --memory 512M --reserve-memory 0M --node-id 0 --check=false --kafka-addr PLAINTEXT://0.0.0.0:9092 --advertise-kafka-addr PLAINTEXT://192.168.18.75:9092
```

### 4. Start the Consumer
```bash
python consumer.py
```

### 5. Start the Producer
Ensure `video.mp4` exists in the root directory.
```bash
python producer.py
```

### 6. Run gRPC Load Test (Optional)
```bash
python load_test.py
```

---

## 🧪 Features

✅ Pretrained PyTorch ResNet18  
✅ Inference over gRPC with health check  
✅ Docker multi-stage image build  
✅ Redpanda-based video stream simulation  
✅ Frame-by-frame classification  
✅ Performance logging (latency, throughput)  
✅ TorchScript optimization  
✅ Automatic GPU/CPU fallback  
✅ Load testing support

---

## 🧑‍💻 Bonus Objectives Achieved

| Bonus Feature                  | Status   |
|-------------------------------|----------|
| TorchScript optimization      | ✅ Done  |
| Prometheus metrics endpoint   | ❌ Skipped |
| Logging to file               | ✅ Done  |
| GPU/CPU fallback toggle       | ✅ Done  |
| Load test script              | ✅ Done  |

---

## 📄 Health Check

You can test the gRPC health check manually using the client:
```bash
python client.py
```

---

## 📚 Requirements

Install required Python packages:
```bash
pip install -r requirements.txt
```

---
