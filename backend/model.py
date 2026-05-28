import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from pathlib import Path

class RegularizedCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 16 * 16, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, 3)
        )

    def forward(self, x):
        return self.classifier(self.features(x))
    
CLASSES = ['aedes', 'anopheles', 'culex']

TRANSFORM = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

BASE_DIR = Path(__file__).parent.parent
# Apuntando al modelo exportado en la raíz para evitar subir la carpeta pesada mlruns a GitHub
WEIGHTS_PATH = BASE_DIR / 'cnn_regularized.pth'


_model = None

def get_model():
    global _model
    if _model is None:
        model = RegularizedCNN()
        weights = torch.load(WEIGHTS_PATH, map_location='cpu', weights_only=True)
        resultado = model.load_state_dict(weights)
        print("Claves faltantes:", resultado.missing_keys)
        print("Claves inesperadas:", resultado.unexpected_keys)
        model.eval()
        _model = model
    return _model


def predict(image: Image.Image) -> dict:
    model = get_model()
    image = image.convert('RGB')
    tensor = TRANSFORM(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(tensor)
        print("Logits crudos:", output)
        probabilities = torch.softmax(output, dim=1)
        print("Probabilidades:", probabilities)
        confidence, idx = torch.max(probabilities, dim=1)
    
    return {
        'species': CLASSES[idx.item()],
        'confidence': round(confidence.item(), 4)
    }