import sqlite3
import tkinter as tk
from tkinter import messagebox
import cv2 
import pandas as pd
import xlwt
from datetime import datetime
import os
from PIL import Image, ImageTk

# Ana pencereyi oluştur
ana_pencere = tk.Tk()
ana_pencere.title("GİRİŞ")
ana_pencere.geometry("550x250")
ana_pencere["bg"] = "#1C2833"

kullanici_adi = tk.StringVar()
sifre = tk.StringVar()
mesaj = tk.StringVar()

# Veritabanı bağlantısı ve giriş fonksiyonu
def login():
    k_adi = kullanici_adi.get()
    parola = sifre.get()

    if not k_adi or not parola:
        mesaj.set("Lütfen tüm alanları doldurun")
        return

    try:
        conn = sqlite3.connect("personeller.db")
        cursor = conn.execute('SELECT * FROM personeller WHERE ADI=? AND PAROLA=?', (k_adi, parola))
        if cursor.fetchone():
            yoklama_penceresi()
        else:
            mesaj.set("KULLANICI ADI VEYA ŞİFRE HATALI!!!")
    except sqlite3.Error as e:
        mesaj.set(f"Veritabanı hatası: {e}")
    finally:
        if conn:
            conn.close()

# Yoklama penceresini aç
def yoklama_penceresi():
    pencere = tk.Toplevel()
    pencere.geometry("400x300")
    pencere.title("Yoklama Sistemi")

    tk.Button(pencere, text="Yoklama Al", font=("Arial", 16), command=YoklamaAlma,
              bg="light green", fg="black", width=15, height=2).pack(pady=20)

    tk.Button(pencere, text="Kaydet & Çıkış", font=("Arial", 16), command=kaydet_ve_cikis,
              bg="red", fg="white", width=15, height=2).pack(pady=10)

# Excel dosyasını kaydet ve programı kapat
def kaydet_ve_cikis():
    wb.save(f'Yoklama/yoklama_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xls')
    print("[INFO] Excel dosyası kaydedildi ve program kapatılıyor.")
    ana_pencere.quit()

# Yoklama alma fonksiyonu
def YoklamaAlma():
    global cam, wb, ws

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet('Gelenler', cell_overwrite_ok=True)

    df = pd.read_excel('sinif_listesi.xlsx')
    ad, soyad, no = df['Adı'], df['Soyad'], df['Numara']
    uzunluk = len(df)

    # Başlıkları yaz
    ws.write(0, 0, 'Numara')
    ws.write(0, 1, 'Adı')
    ws.write(0, 2, 'Soyad')
    ws.write(0, 3, 'Durum')
    ws.write(0, 4, 'Tarih ve Saat')

    for i in range(uzunluk):
        ws.write(i + 1, 0, no[i])
        ws.write(i + 1, 1, ad[i])
        ws.write(i + 1, 2, soyad[i])
        ws.write(i + 1, 3, "YOK")  # Varsayılan olarak 'YOK'

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        messagebox.showerror("Hata", "Kamera açılamadı!")
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('egitim/egitim.yml')

    def kamera_guncelle():
        ret, frame = cam.read()
        if not ret:
            print("Kamera görüntüsü alınamadı.")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (150, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

            durum = "TANIMIYOR"
            if conf < 50:
                for i in range(uzunluk):
                    if str(Id) == str(no[i]):
                        ws.write(i + 1, 3, "VAR")  # 'VAR' olarak güncelle
                        ws.write(i + 1, 4, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        durum = f"{ad[i]} {soyad[i]}"
                        print(f"[INFO] Tanımlanan Kişi: {durum}")

            cv2.putText(frame, durum, (x, y - 10), font, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)

        kamera_label.imgtk = imgtk
        kamera_label.configure(image=imgtk)
        kamera_label.after(10, kamera_guncelle)

    # Kamera arayüzü
    kamera_pencere = tk.Toplevel()
    kamera_pencere.geometry("800x600")
    kamera_pencere.title("Yüz Tanıma")

    kamera_label = tk.Label(kamera_pencere)
    kamera_label.pack()

    tk.Button(kamera_pencere, text="Kapat", command=kamera_pencere.destroy, font=("Arial", 16),
              bg="red", fg="white", width=10, height=2).pack(pady=10)

    kamera_guncelle()

# Giriş arayüzü
tk.Label(ana_pencere, text="GİRİŞ FORMU", bg="#0E6655", fg="white", font=("Arial", 12, "bold")).pack()
tk.Label(ana_pencere, text="Kullanıcı Adı", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(x=20, y=40)
tk.Entry(ana_pencere, textvariable=kullanici_adi).place(x=120, y=42)
tk.Label(ana_pencere, text="Şifre", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(x=20, y=80)
tk.Entry(ana_pencere, textvariable=sifre, show="*").place(x=120, y=82)
tk.Label(ana_pencere, text="", textvariable=mesaj, bg="#1C2833", fg="white").place(x=110, y=170)
tk.Button(ana_pencere, text="GİRİŞ", command=login).place(x=115, y=130)
tk.Button(ana_pencere, text="ÇIKIŞ", command=ana_pencere.quit).place(x=230, y=130)

ana_pencere.mainloop()



def YeniAkademisyenKaydet():
    kayit_penceresi = Toplevel()
    kayit_penceresi.configure(background='light blue')
    kayit_penceresi.title("Akademisyen Kayıt Formu")
    kayit_penceresi.geometry("500x300")

    # Akademisyen bilgileri giriş alanları
    Label(kayit_penceresi, text="Yeni Akademisyen Kayıt Et", bg="light blue", font=yazi_tipi).grid(row=0, column=1)
    Label(kayit_penceresi, text="Ad", bg="light blue").grid(row=1, column=0)
    Label(kayit_penceresi, text="Soyad", bg="light blue").grid(row=2, column=0)
    Label(kayit_penceresi, text="Mail", bg="light blue").grid(row=3, column=0)
    Label(kayit_penceresi, text="Parola", bg="light blue").grid(row=4, column=0)

    ad_field = Entry(kayit_penceresi)
    soyad_field = Entry(kayit_penceresi)
    mail_field = Entry(kayit_penceresi)
    parola_field = Entry(kayit_penceresi)

    ad_field.grid(row=1, column=1, ipadx="100")
    soyad_field.grid(row=2, column=1, ipadx="100")
    mail_field.grid(row=3, column=1, ipadx="100")
    parola_field.grid(row=4, column=1, ipadx="100")

    # Kayıt butonu işlevi
    def AkademisyeniKaydet():
        if ad_field.get() == "" or soyad_field.get() == "" or mail_field.get() == "" or parola_field.get() == "":
            messagebox.showerror("Hata!", "Lütfen tüm alanları doldurun!")
            return

        try:
            adi = ad_field.get()
            soyadi = soyad_field.get()
            mail = mail_field.get()
            parola = parola_field.get()

            kaydet_bilgiler(adi, soyadi, mail, parola)
            messagebox.showinfo("Başarılı", f"Akademisyen başarıyla kayıt edildi! \nAdı: {adi}, Soyadı: {soyadi}, Mail: {mail}")

            # Alanları sıfırla
            ad_field.delete(0, END)
            soyad_field.delete(0, END)
            mail_field.delete(0, END)
            parola_field.delete(0, END)
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt işlemi başarısız: {e}")

    # Kaydet butonu
    Button(kayit_penceresi, text="Kaydet", fg="White", bg="Red", command=AkademisyeniKaydet).grid(row=5, column=1, ipadx="50", ipady="20")

    kayit_penceresi.mainloop()
    Button(ana_pencere, text="Akademisyen kaydet", font=yazi_tipi, image=yoklamaResim, compound=TOP,
       bg="light green", fg="blue", command=YeniAkademisyenKaydet).grid(column=1, row=5)