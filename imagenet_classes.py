# Run once to convert imagenet_classes.txt to imagenet_classes.json

with open("imagenet_classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

class_dict = {str(i): label for i, label in enumerate(classes)}

import json
with open("imagenet_classes.json", "w") as f:
    json.dump(class_dict, f)