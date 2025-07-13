import torch
import torchvision.models as models
import cv2
import numpy as np
import json
import os

class ImageClassifier:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = "resnet18_scripted.pt"

        if os.path.exists(self.model_path):
            self.model = torch.jit.load(self.model_path).to(self.device)
        else:
            model = models.resnet18(pretrained=True)
            model.eval()
            scripted_model = torch.jit.script(model)
            scripted_model.save(self.model_path)
            self.model = scripted_model.to(self.device)

        with open("imagenet_classes.json", "r") as f:
            self.class_names = json.load(f)

    def predict(self, image_bytes):
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return "Invalid image", 0.0

        # Resize and center crop
        image = cv2.resize(image, (256, 256))
        center = image.shape[0] // 2
        image = image[center - 112:center + 112, center - 112:center + 112]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Normalize
        image = image.astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = (image - mean) / std

        # Format to tensor
        image = np.transpose(image, (2, 0, 1))
        input_tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            top1_idx = torch.argmax(probs).item()
            confidence = probs[top1_idx].item()
            label = self.class_names[str(top1_idx)]

        return label, confidence