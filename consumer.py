import base64
import cv2
import numpy as np
import grpc
import time
from confluent_kafka import Consumer
import inference_pb2
import inference_pb2_grpc

# gRPC setup
channel = grpc.insecure_channel("localhost:50051")
stub = inference_pb2_grpc.InferenceServiceStub(channel)

# Kafka setup
consumer = Consumer({
    'bootstrap.servers': '192.168.18.75:9092',
    'group.id': 'frame-consumers',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['frames'])

# Performance metrics
latencies = []
frame_count = 0
start_time = time.time()

while True:
    if time.time() - start_time >= 30:
        break

    msg = consumer.poll(1.0)
    if msg is None or msg.error():
        continue

    try:
        # Decode message to image
        frame_data = msg.value()
        np_arr = np.frombuffer(frame_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            continue

        # Start timer
        t1 = time.time()
        _, buffer = cv2.imencode(".jpg", image)
        response = stub.Predict(inference_pb2.ImageRequest(image_data=buffer.tobytes()))
        t2 = time.time()

        latency = t2 - t1
        latencies.append(latency)
        frame_count += 1

        print(f"Predicted: {response.label}, Confidence: {response.confidence:.2f}, Latency: {latency:.3f} sec")

    except Exception as e:
        print(f"Error: {e}")
        continue

# Summary
avg_latency = sum(latencies) / len(latencies) if latencies else 0
throughput = frame_count / 30.0

print("\n--- Performance Summary ---")
print(f"Total frames processed: {frame_count}")
print(f"Average latency per frame: {avg_latency:.3f} sec")
print(f"Average throughput: {throughput:.2f} FPS")