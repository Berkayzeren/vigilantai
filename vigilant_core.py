from ultralytics import YOLO
import cv2
import time
import sys

# --- VIGILANT AI SİSTEM AYARLARI ---
# Hedef IP (Senin telefonun)
KAMERA_ADRESI = "http://192.168.1.104:4747/video"
MODEL_ADI = "yolov8n.pt"
SISTEM_ISMI = "VIGILANT AI - Saha Gozu v1.0"

print(f"--- {SISTEM_ISMI} BAŞLATILIYOR ---")

# 1. Modeli Yükle
print(f"[Sistem]: Model yükleniyor ({MODEL_ADI})...")
try:
    model = YOLO(MODEL_ADI)
except Exception as e:
    print(f"[Hata]: Model yüklenemedi. Kütüphaneler eksik olabilir. Hata: {e}")
    sys.exit()

# 2. Kameraya Bağlan
print(f"[Sistem]: Kamera sinyali aranıyor ({KAMERA_ADRESI})...")
cap = cv2.VideoCapture(KAMERA_ADRESI)

if not cap.isOpened():
    print(f"\n!!! BAĞLANTI HATASI !!!")
    print(f"Sistem '{KAMERA_ADRESI}' kaynağından görüntü alamadı.")
    print("ÇÖZÜM ADIMLARI:")
    print("1. Telefonunda iVCam uygulamasının açık ve ekranda görüntünün aktığını kontrol et.")
    print("2. Telefon ve Bilgisayar aynı Wi-Fi ağında mı?")
    print("3. Linux güvenlik duvarı portu engelliyor olabilir.")
    sys.exit()

print("[Sistem]: BAĞLANTI KURULDU! Analiz başlıyor...")

# FPS ve Zamanlayıcılar
prev_time = 0

# --- PENCERE AYARLARI ---
cv2.namedWindow(SISTEM_ISMI, cv2.WINDOW_NORMAL)
# EKLEME: Pencereyi monitöre tam ekran yayar
cv2.setWindowProperty(SISTEM_ISMI, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# --- ROTASYON AYARLARI ---
# 0, 1 (90 CW), 2 (180), 3 (270 CW / 90 CCW)
# OpenCV rotate kodları ile eşleşmesi için mantık kuracağız.
current_rotation = 0 
is_fullscreen = True

while True:
    ret, frame = cap.read()
    if not ret:
        print("[Uyarı]: Kamera sinyali koptu.")
        break
    
    # --- GÖRÜNTÜ DÖNDÜRME ---
    if current_rotation == 1:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif current_rotation == 2:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    elif current_rotation == 3:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


    # --- YAPAY ZEKA MOTORU ---
    # stream=True: Hızlı akış için
    results = model(frame, stream=True, verbose=False)

    # Tespitleri çiz
    for r in results:
        frame = r.plot()

    # --- HUD (Head-Up Display) ARAYÜZÜ ---
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Marka ve İstatistikler
    # Sol Üst: Marka
    cv2.rectangle(frame, (10, 10), (300, 90), (0, 0, 0), -1) # Arka plan siyah kutu
    cv2.putText(frame, "VIGILANT AI", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2) # Sarı yazı
    cv2.putText(frame, "LIVE MONITORING", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1) # Yeşil yazı
    cv2.putText(frame, "'r': Dondur | 'f': Pencere | 's': Cikis", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1) # Gri talimat


    # Sol Alt: FPS
    cv2.putText(frame, f"FPS: {int(fps)}", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Görüntüyü Göster
    cv2.imshow(SISTEM_ISMI, frame)

    # 'q' tuşu ile çıkış
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('s'):
        break
    elif key == ord('r'):
        current_rotation = (current_rotation + 1) % 4
        print(f"[Sistem]: Döndürme modu: {current_rotation}")
    elif key == ord('f'):
        is_fullscreen = not is_fullscreen
        if is_fullscreen:
             cv2.setWindowProperty(SISTEM_ISMI, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
             cv2.setWindowProperty(SISTEM_ISMI, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)



cap.release()
cv2.destroyAllWindows()
print(f"[Sistem]: {SISTEM_ISMI} kapatıldı.")