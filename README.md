# 🦝 Raccoon Detection API (FastAPI & Docker)

Bu proje, Derin Öğrenme (Deep Learning) tabanlı bir nesne tespit modelini (Object Detection) **FastAPI** kullanarak mikroservis haline getiren ve **Docker** üzerinde sunan bir uygulamadır.

Proje, eğitilmiş bir **ResNet-50** modelini kullanarak görseller üzerindeki rakunları tespit eder ve konumlarını (Bounding Box) JSON formatında döndürür.

---

## 🚀 Özellikler

- **Model:** PyTorch tabanlı Custom ResNet-50 Object Detector.
- **API:** FastAPI ile yüksek performanslı ve asenkron REST API.
- **Dockerize:** `docker-compose` ile tek komutla kurulum.
- **Multi-Arch Desteği:** Hem **Intel (AMD64)** hem de **Apple Silicon (ARM64/M1/M2)** işlemcilerde sorunsuz çalışacak şekilde yapılandırılmıştır (`python:3.9-slim`).
- **CPU Optimizasyonu:** Model, GPU gereksinimi olmadan CPU üzerinde çalışacak şekilde optimize edilmiştir.

---

## 🛠 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için Docker'ın yüklü olması yeterlidir.

### 1. Repoyu Klonlayın
```bash
git clone [https://github.com/emreyoruk64/raccoon-fastapi-docker.git](https://github.com/emreyoruk64/raccoon-fastapi-docker.git)
cd raccoon-fastapi-docker
```

### 2. Docker Konteynerini Başlatın
Aşağıdaki komut, gerekli imajı oluşturacak ve servisi 7001 portunda başlatacaktır:

```bash
docker-compose up --build
```

Terminalde `Uvicorn running on http://0.0.0.0:8000` yazısını gördüğünüzde servis hazırdır.

---

## 🧪 Nasıl Test Edilir?

Servis çalıştığında Swagger UI arayüzü üzerinden interaktif olarak test edebilirsiniz.

1. Tarayıcınızda şu adrese gidin:

    **http://localhost:7001/docs**

2. `POST /predict` endpoint'ine tıklayın.

3. **Try it out** butonuna basın.

4. Bir rakun görseli yükleyin ve **Execute** deyin.

**Örnek Çıktı (JSON):**
```json
{
  "label": "Raccoon",
  "confidence": 0.9706,
  "bbox": {
    "xmin": 0.3537,
    "ymin": 0.3508,
    "xmax": 0.6512,
    "ymax": 0.6843
  }
}
```

---

## 📂 Proje Yapısı

```plaintext
raccoon-fastapi-docker/
├── detector.pth         # Eğitilmiş PyTorch Modeli (ResNet-50)
├── main.py              # FastAPI Uygulaması ve Model Inference Kodları
├── Dockerfile           # Docker İmaj Konfigürasyonu (Python 3.9 Slim)
├── docker-compose.yml   # Konteyner ve Port Ayarları (7001:8000)
├── requirements.txt     # Gerekli Python Kütüphaneleri
└── README.md            # Proje Dokümantasyonu
```

---

## 🔧 Kullanılan Teknolojiler

- **Dil:** Python 3.9
- **Framework:** FastAPI, Uvicorn
- **ML Library:** PyTorch, Torchvision
- **Containerization:** Docker, Docker Compose
- **Image Processing:** PIL (Pillow), Numpy

---


