import grpc
import cv2

import inference_pb2
import inference_pb2_grpc

def read_image_bytes(path):
    img = cv2.imread(path)
    _, buffer = cv2.imencode(".jpg", img)
    return buffer.tobytes()

def main():
    # Connect to gRPC server
    channel = grpc.insecure_channel("localhost:50051")
    stub = inference_pb2_grpc.InferenceServiceStub(channel)

    # Perform health check
    try:
        health = stub.HealthCheck(inference_pb2.HealthRequest())
        print(f"Health status: {health.status}")
    except grpc.RpcError as e:
        print(f"Health check failed: {e}")
        return

    # Perform image prediction
    image_data = read_image_bytes("sample.jpg")  # Replace with your image path
    request = inference_pb2.ImageRequest(image_data=image_data)
    response = stub.Predict(request)

    print(f"Predicted label: {response.label}")
    print(f"Confidence: {response.confidence:.4f}")

if __name__ == "__main__":
    main()