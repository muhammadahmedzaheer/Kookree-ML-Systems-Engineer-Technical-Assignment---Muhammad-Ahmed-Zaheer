import grpc
from concurrent import futures
import time
import logging

import inference_pb2
import inference_pb2_grpc
from model import ImageClassifier

# Setup logging to file
logging.basicConfig(
    filename="inference.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class InferenceServiceServicer(inference_pb2_grpc.InferenceServiceServicer):
    def __init__(self):
        self.classifier = ImageClassifier()

    def Predict(self, request, context):
        label, confidence = self.classifier.predict(request.image_data)
        logging.info(f"Inference: label={label}, confidence={confidence:.4f}")
        return inference_pb2.PredictionResponse(label=label, confidence=confidence)

    def HealthCheck(self, request, context):
        return inference_pb2.HealthResponse(status="READY")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    inference_pb2_grpc.add_InferenceServiceServicer_to_server(InferenceServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("gRPC server started on port 50051")
    print("gRPC server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        logging.info("gRPC server stopped")
        server.stop(0)

if __name__ == "__main__":
    serve()