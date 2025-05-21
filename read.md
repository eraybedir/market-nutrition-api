## ⚙️ Kurulum ve Çalıştırma (Local veya Sunucu)

### Gerekli yazılımlar:
- Docker
- Docker Compose

### 1. Projeyi bu klasöre yerleştir:
~/DataLayer/

### 2. Terminal aç ve çalıştır:

###
 cd DataLayer
docker-compose up --build

### 3. API’ye eriş: bash
http://localhost:5000/get-products
Eğer sunucuda çalıştırıyorsanız: http://<sunucu-ip>:5000/get-products
###

## Sunucuya Deploy Etme
terminalde

1. Bu projeyi sunucuya aktar:
scp -r ./DataLayer user@sunucu-ip:/home/user/

2. Sunucuda çalıştır:
cd /home/user/DataLayer
docker-compose up --build

3. Tarayıcıdan test et: