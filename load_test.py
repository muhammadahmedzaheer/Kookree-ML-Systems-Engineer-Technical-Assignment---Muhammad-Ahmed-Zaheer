import grpc
import time
import inference_pb2
import inference_pb2_grpc

def send_request(image_data):
    channel = grpc.insecure_channel("localhost:50051")
    stub = inference_pb2_grpc.InferenceServiceStub(channel)
    request = inference_pb2.ImageRequest(image_data=image_data)
    return stub.Predict(request)

if __name__ == "__main__":
    with open("sample.jpg", "rb") as f:
        image_data = f.read()

    start = time.time()
    total = 50
    for _ in range(total):
        send_request(image_data)
    end = time.time()

    duration = end - start
    print(f"Sent {total} requests in {duration:.2f}s")
    print(f"Avg latency: {duration/total:.4f}s")
    print(f"Throughput: {total/duration:.2f} FPS")