import io

import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms, datasets
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os

# ── Config ──────────────────────────────────────────────────────────────────
MODEL_PATH  = "Classifer/tank_model.pth"
TRAIN_PATH  = r"C:\Users\hussa\Desktop\data_split\train"   # used to recover class names
# ─────────────────────────────────────────────────────────────────────────────

def get_class_names():
    """Load class names from the original training folder if available."""
    if os.path.isdir(TRAIN_PATH):
        dataset = datasets.ImageFolder(TRAIN_PATH)
        return dataset.classes
    # Fallback: return None and we'll show class indices instead
    return None


def load_model(device: torch.device):
    checkpoint = torch.load(MODEL_PATH, map_location=device)

    num_classes = checkpoint["classifier.1.weight"].shape[0]

    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)

    model.load_state_dict(checkpoint)
    model.to(device)
    model.eval()

    return model, num_classes


def pick_image() -> str:
    """Open a file-dialog and return the selected image path."""
    root = tk.Tk()
    root.withdraw()          # hide the empty Tk window
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All files", "*.*")]
    )
    root.destroy()
    return path


def preprocess(file_bytes: bytes):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)   # add batch dimension


def predict(model, tensor: torch.Tensor, device: torch.device, class_names):
    tensor = tensor.to(device)
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]
        confidence, predicted_idx = torch.max(probabilities, 0)

    predicted_idx = predicted_idx.item()
    label = class_names[predicted_idx] if class_names else f"Class {predicted_idx}"
    return label, confidence.item()


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 1. Load the saved model first
    print(f"Loading model from '{MODEL_PATH}'...")
    model, num_classes = load_model(device)
    print(f"Model loaded successfully ({num_classes} classes).\n")

    # 2. Load class names if the training folder is available
    class_names = get_class_names()
    if class_names and len(class_names) != num_classes:
        print("Warning: class names from TRAIN_PATH do not match the saved model output size.")
        class_names = None

    # 3. Pick image via file dialog
    image_path = pick_image()
    if not image_path:
        print("No image selected. Exiting.")
        return

    print(f"Selected image: {image_path}")

    # 4. Preprocess & predict
    tensor = preprocess(image_path)
    label, confidence = predict(model, tensor, device, class_names)

    print(f"\nPrediction : {label}")
    print(f"Confidence : {confidence * 100:.2f}%")


if __name__ == "__main__":
    main()
