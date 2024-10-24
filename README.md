# Yuz-Tanima-Sistemi-Ile-Yoklama-Alma

Bu proje, **OpenCV** kullanarak yüz tanıma işlemleri yapmanızı sağlar. Eğitim aşamasıyla yüzleri tanımak için bir model oluşturur ve bu modeli kullanarak canlı video akışında yüz tanıma gerçekleştirir.

## 📂 Proje İçeriği

- **calistir.bat**: Projeyi hızlı başlatmak için kullanılır.  
- **eğitim.py**: Eğitim süreci için kullanılan betik. Yüz verilerini işler ve tanıma için model oluşturur.  
- **haarcascade_frontalface_default.xml**: Yüz tespiti için OpenCV'nin Haar Cascade sınıflandırıcısı.  
- **yuztanima.py**: Canlı video akışında yüz tanıma işlemini gerçekleştiren ana betik.  

## 🛠️ Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki gereksinimlerin karşılanması gerekir:

- **Python 3.x**  
- Kütüphaneler:
  - OpenCV:  
    ```bash
    pip install opencv-python
    ```
  - NumPy:  
    ```bash
    pip install numpy
    ```

## 🚀 Kurulum ve Çalıştırma

1. **Gerekli kütüphaneleri yükleyin**:
   ```bash
   pip install opencv-python numpy
