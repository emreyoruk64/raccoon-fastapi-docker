# Hafif ve çoklu mimari destekleyen (ARM64/AMD64) Python imajı
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle (OpenCV için gerekli minimal kütüphaneler)
# libgl1-mesa-glx: OpenCV'nin çalışması için gerekebilir (cv2 kullanmasak da torchvision isteyebilir)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları ve modeli kopyala
COPY . .

# FastAPI'yi başlat (Port 8000 konteyner içi porttur)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]