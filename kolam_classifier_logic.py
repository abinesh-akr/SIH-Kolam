import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import streamlit as st

# --- 1. CONFIGURATION (Copied from your script) ---
MODEL_PATH = "simple_kolam_classifier.pth"
IMAGE_SIZE = 128
CLASS_NAMES = ['Pulli', 'Rangoli', 'butterfly', 'kambi', 'padi', 'sikku']

# --- 2. MODEL DEFINITION (Copied from your script) ---
class SimpleKolamCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleKolamCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.flatten = nn.Flatten()
        self.classifier = nn.Sequential(
            nn.Linear(64 * 16 * 16, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.flatten(x)
        x = self.classifier(x)
        return x

# --- 3. LOAD THE TRAINED MODEL (Adapted for Streamlit) ---
# @st.cache_resource is CRUCIAL. It loads the model only once and keeps it in memory.
@st.cache_resource
def load_model():
    """Loads and returns the trained model."""
    device = torch.device("cpu")
    model = SimpleKolamCNN(num_classes=len(CLASS_NAMES))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
    print("Model loaded successfully!")
    return model

# --- 4. DEFINE PREPROCESSING AND PREDICTION (Adapted for Streamlit) ---
def predict(model, pil_image):
    """
    Takes a model and a PIL image, and returns the model's predictions.
    """
    if pil_image is None:
        return None

    # Define the image transformations (must match training)
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])
    
    image_tensor = transform(pil_image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        
    probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
    confidences = {CLASS_NAMES[i]: float(prob) for i, prob in enumerate(probabilities)}
    
    return confidences