import cv2
import numpy as np
from PIL import Image
import os

# Verilerin bulunduğu dizin
dataset_path = os.path.join(os.getcwd(), 'datasets')

# LBPH yüz tanıma modeli oluşturuluyor
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Cascade dosyasının yolunu belirleyip yü
# kleyelim
cascade_path = os.path.join(os.getcwd(), "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cascade_path)

# Cascade dosyasının doğru yüklendiğinden emin olalım
if face_cascade.empty():
    raise FileNotFoundError(f"Cascade dosyası bulunamadı: {cascade_path}")

# Resimlerden yüzlerin alınması ve etiketlenmesi için fonksiyon
def getImagesAndLabels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]
    face_samples = []
    ids = []

    for image_path in image_paths:
        try:
            # Dosya adından ID çıkarma
            id = int(os.path.split(image_path)[-1].split(".")[0])
        except ValueError:
            print(f"{image_path} dosyası geçersiz formatta, atlanıyor.")
            continue

        # Resmi gri tonlamaya çevirme
        pil_image = Image.open(image_path).convert('L')
        image_array = np.array(pil_image, 'uint8')

        print(f"[INFO] ID: {id} - Resim: {image_path}")

        # Yüzleri tespit etme
        faces = face_cascade.detectMultiScale(image_array)
        for (x, y, w, h) in faces:
            face_samples.append(image_array[y:y + h, x:x + w])
            ids.append(id)

    return face_samples, ids

try:
    print("\n[INFO] Yüzler eğitiliyor. Bekleyin lütfen...")

    # Yüzlerin ve ID'lerin alınması
    faces, ids = getImagesAndLabels(dataset_path)

    if not faces or not ids:
        raise ValueError("Veri bulunamadı. Lütfen 'datasets' klasörünü kontrol edin.")

    # Modeli eğitme
    recognizer.train(faces, np.array(ids))

    # Eğitim verilerini kaydedecek klasörü oluşturma
    os.makedirs("egitim", exist_ok=True)

    # Eğitilen modeli kaydetme
    model_path = os.path.join("egitim", "egitim.yml")
    recognizer.write(model_path)

    print(f"\n[INFO] {len(np.unique(ids))} yüz eğitildi ve '{model_path}' dosyasına kaydedildi.")

except Exception as e:
    print(f"[HATA] {e}")
