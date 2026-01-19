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

