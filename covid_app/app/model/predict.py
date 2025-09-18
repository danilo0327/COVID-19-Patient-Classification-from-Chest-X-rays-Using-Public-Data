# covid_app/app/model/predict.py
import os, json, torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model_V02.pt")  # <-- ajusta si tu archivo se llama distinto
CLASSES_PATH = os.path.join(BASE_DIR, "classes.json")
IMAGE_SIZE = 224
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)

def load_classes():
    if "classes" in checkpoint:
        c = checkpoint["classes"]
        if isinstance(c, dict) and "classes" in c:
            return c["classes"]
        return c
    with open(CLASSES_PATH, "r") as f:
        data = json.load(f)
    return data["classes"] if isinstance(data, dict) and "classes" in data else data

CLASSES = load_classes()

# Modelo
model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(CLASSES))
model.load_state_dict(checkpoint["state_dict"])
model.to(DEVICE).eval()

# Transforms (rayos X: L -> 3 canales)
TFM = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.Resize(int(IMAGE_SIZE * 1.14)),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
])

def _preprocess(image_path: str):
    img = Image.open(image_path).convert("L")
    return TFM(img).unsqueeze(0).to(DEVICE)

@torch.no_grad()
def predict_with_probs(image_path: str):
    """
    Return:
      pred_label: str
      probs_dict: Dict[str, float]  # 0-1 por clase
    """
    x = _preprocess(image_path)
    logits = model(x)
    probs = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()
    pred_idx = int(probs.argmax())
    pred_label = CLASSES[pred_idx]
    probs_dict = {CLASSES[i]: float(probs[i]) for i in range(len(CLASSES))}
    return pred_label, probs_dict

# compat: solo clase
def make_prediction(image_path: str) -> str:
    pred, _ = predict_with_probs(image_path)
    return pred

