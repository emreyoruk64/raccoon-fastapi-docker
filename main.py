from fastapi import FastAPI, File, UploadFile
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import io
from fastapi import HTTPException
import sys
import traceback

# Colab'de eğitilen modeli burada tanıması için __main__'i bu dosyaya yönlendiriyoruz.
sys.modules['__main__'] = sys.modules[__name__]

## --- 1. MODEL TANIMI ---
class ObjectDetector(nn.Module):
    def __init__(self, baseModel, numClasses):
        super(ObjectDetector, self).__init__()
        # 1. Önceden eğitilmiş ResNet'i al
        self.baseModel = baseModel

        # 2. ResNet'in çıkış katmanındaki özellik sayısını al
        numFeatures = baseModel.fc.in_features

        # 3. Sadece özellik çıkarıcı olarak kullan
        self.baseModel.fc = nn.Identity()

        # 4. Regressor
        self.regressor = nn.Sequential(
            nn.Linear(numFeatures, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 4), # Çıktı: (xmin, ymin, xmax, ymax)
            nn.Sigmoid()      # Çıktıyı 0-1 arasına sıkıştırır
        )

        # 5. Classifier
        self.classifier = nn.Sequential(
            nn.Linear(numFeatures, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, numClasses) # Çıktı: Sınıf sayısı
        )

    def forward(self, x):
        # Resmi ResNet'ten geçir, özellikleri al
        features = self.baseModel(x)

        # Özellikleri gönder
        bboxes = self.regressor(features)
        classLogits = self.classifier(features)

        return (bboxes, classLogits)
    
# --- 3. AYARLAR ---
app = FastAPI(title="Raccoon Detector API")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

model = None

# --- 4. MODEL YÜKLEME (Startup) ---
@app.on_event("startup")
async def load_model():
    global model
    print("⏳ Model yükleniyor...")
    try:
        # HEM CPU AYARI HEM DE GÜVENLİK AYARI 
        model = torch.load(
            "detector.pth", 
            map_location=torch.device('cpu'), 
            weights_only=False  
        )
        model.eval()
        print("Model başarıyla yüklendi!")
    except Exception as e:
        print(f"MODEL YÜKLEME HATASI:\n{e}")
        print(traceback.format_exc())

# --- 5. ENDPOINT ---
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Model yüklenemedi. Logları kontrol edin.")

    try:
        # Resmi Oku
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        
        # Transform
        image_tensor = transform(image).unsqueeze(0)
        
        # Tahmin
        with torch.no_grad():
            (bboxPreds, classPreds) = model(image_tensor)
        
        # Sonuç İşleme
        probs = torch.nn.Softmax(dim=1)(classPreds)
        prob_score = probs[0][1].item()
        
        label = "Raccoon" if prob_score > 0.5 else "Background"
        bbox_coords = bboxPreds[0].tolist()

        return {
            "label": label,
            "confidence": round(prob_score, 4),
            "bbox": {
                "xmin": round(bbox_coords[0], 4),
                "ymin": round(bbox_coords[1], 4),
                "xmax": round(bbox_coords[2], 4),
                "ymax": round(bbox_coords[3], 4)
            }
        }

    except Exception as e:
        print(f"Tahmin Hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))