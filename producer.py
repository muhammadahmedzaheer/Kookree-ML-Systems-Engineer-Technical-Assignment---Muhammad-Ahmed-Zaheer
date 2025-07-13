import cv2
from confluent_kafka import Producer
import time

VIDEO_PATH = "video.mp4"  # Place your video file in root directory
TOPIC = "frames"

conf = {'bootstrap.servers': '192.168.18.75:9092'}
producer = Producer(conf)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered frame to {msg.topic()}")

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Failed to open video file.")
    exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    producer.produce(TOPIC, buffer.tobytes(), callback=delivery_report)
    producer.poll(0)
    time.sleep(0.1)  # Simulate streaming delay

cap.release()
producer.flush()