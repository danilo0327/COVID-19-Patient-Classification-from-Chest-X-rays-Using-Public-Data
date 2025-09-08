import os
import json
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# Paths
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model_V01.pt")
CLASSES_PATH = os.path.join(BASE_DIR, "classes.json")

# Load checkpoint
checkpoint = torch.load(MODEL_PATH, map_location="cpu")

# Load classes (from json, o directamente de checkpoint si existen)
if "classes" in checkpoint:
    idx_to_class = checkpoint["classes"]
else:
    with open(CLASSES_PATH, "r") as f:
        idx_to_class = json.load(f)

# Define model (must match training)
model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(idx_to_class))

# Load weights from checkpoint
model.load_state_dict(checkpoint["state_dict"])
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def preprocess_image(image_path: str):
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

def make_prediction(image_path: str) -> str:
    tensor = preprocess_image(image_path)
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = outputs.max(1)
        class_idx = predicted.item()   # 👈 ya como entero
    return idx_to_class[class_idx]

