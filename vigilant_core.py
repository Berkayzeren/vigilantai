import os
import sys
import time
import cv2
from dotenv import load_dotenv
from ultralytics import YOLO


class VigilantCore:
    def __init__(self):
        """
        Sistem konfigürasyonlarını başlatır ve çevre değişkenlerini (ENV) yükler.
        """
        # 1. Ortam değişkenlerini (Environment Variables) yükle
        load_dotenv()

        # --- VIGILANT AI SİSTEM AYARLARI ---
        # .env dosyasından okur, yoksa varsayılan değerleri döndürür
        self.kamera_adresi = os.getenv("KAMERA_ADRESI", "0")
        self.model_adi = os.getenv("MODEL_ADI", "yolov8n.pt")
        self.sistem_ismi = "VIGILANT AI - Saha Gozu v2.0"

        self.cap = None
        self.model = None

        # Durum değişkenleri
        self.current_rotation = 0
        self.is_fullscreen = True
        self.prev_time = 0

    def load_model(self):
        """YOLOv8 modelini belleğe yükler."""
        print(f"--- {self.sistem_ismi} BAŞLATILIYOR ---")
        print(f"[Sistem]: Model yükleniyor ({self.model_adi})...")
        try:
            self.model = YOLO(self.model_adi)
        except Exception as e:
            print(f"[Hata]: Model yüklenemedi. Kütüphaneler eksik olabilir. Hata: {e}")
            sys.exit(1)

    def connect_camera(self):
        """Kamera veya ağ (IP) video akışına bağlanır."""
        print(f"[Sistem]: Kamera sinyali aranıyor ({self.kamera_adresi})...")

        # Eğer adres sadece rakamsa (örn: 0, 1) web kamerası için tam sayı tipine çevirir.
        cam_source = (
            int(self.kamera_adresi)
            if self.kamera_adresi.isdigit()
            else self.kamera_adresi
        )
        self.cap = cv2.VideoCapture(cam_source)

        if not self.cap.isOpened():
            print("\n!!! BAĞLANTI HATASI !!!")
            print(f"Sistem '{self.kamera_adresi}' kaynağından görüntü alamadı.")
            print("ÇÖZÜM ADIMLARI:")
            print(
                "1. .env dosyasındaki KAMERA_ADRESI değerini doğru yapılandırdığınızdan emin olun."
            )
            print(
                "2. Telefonunuzda ağ kamerası (örn: iVCam) kullanıyorsanız yayının aktif olduğunu kontrol edin."
            )
            print(
                "3. Telefon ve Bilgisayarın aynı Wi-Fi ağında bağlandığını onaylayın."
            )
            print("4. Linux güvenlik duvarı video portunu engelliyor olabilir.")
            sys.exit(1)

        print("[Sistem]: BAĞLANTI KURULDU! Analiz başlıyor...")

    def setup_window(self):
        """OpenCV pencere arayüzünü (GUI) yapılandırır."""
        cv2.namedWindow(self.sistem_ismi, cv2.WINDOW_NORMAL)
        if self.is_fullscreen:
            cv2.setWindowProperty(
                self.sistem_ismi, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
            )

    def process_rotation(self, frame):
        """Mevcut duruma göre rotasyon matrisini (rotate) uygular."""
        if self.current_rotation == 1:
            return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif self.current_rotation == 2:
            return cv2.rotate(frame, cv2.ROTATE_180)
        elif self.current_rotation == 3:
            return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return frame

    def draw_hud(self, frame):
        """Görüntü (Frame) üzerine bilgi arayüzünü (HUD) çizer."""
        curr_time = time.time()
        fps = (
            1 / (curr_time - self.prev_time) if (curr_time - self.prev_time) > 0 else 0
        )
        self.prev_time = curr_time

        # Sol Üst: Marka Logosu ve Kontrol Bilgileri
        cv2.rectangle(frame, (10, 10), (300, 90), (0, 0, 0), -1)
        cv2.putText(
            frame,
            "VIGILANT AI",
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            frame,
            "LIVE MONITORING",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            1,
        )
        cv2.putText(
            frame,
            "'r': Dondur | 'f': Pencere | 's': Cikis",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1,
        )

        # Sol Alt: Dinamik FPS Göstergesi
        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        return frame

    def handle_keyboard(self):
        """Döngü içerisinde anlık klavye yönlendirmelerini yakalar. True dönerse çıkış yapılır."""
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == ord("s"):
            return True
        elif key == ord("r"):
            self.current_rotation = (self.current_rotation + 1) % 4
            print(
                f"[Sistem]: Döndürme modu asimetrik olarak güncellendi: {self.current_rotation}"
            )
        elif key == ord("f"):
            self.is_fullscreen = not self.is_fullscreen
            prop = cv2.WINDOW_FULLSCREEN if self.is_fullscreen else cv2.WINDOW_NORMAL
            cv2.setWindowProperty(self.sistem_ismi, cv2.WND_PROP_FULLSCREEN, prop)
        return False

    def run(self):
        """Sistemin ana yaşam döngüsünü (Life Cycle) kontrol eder."""
        self.load_model()
        self.connect_camera()
        self.setup_window()
        self.prev_time = time.time()

        try:
            while True:
                ret, frame = self.cap.read()

                # Kamera sinyali var mı diye kontrol et (Bağlantı koptuğunda kilitlenme yapmaması için)
                if not ret:
                    print(
                        "[Uyarı]: Kamera sinyali koptu veya hedeflenen kaynağın sonuna gelindi."
                    )
                    break

                # 1. Aşama: Görüntü Düzenleme (Örn: Cihazı yan tutma durumu)
                frame = self.process_rotation(frame)

                # 2. Aşama: Otonom Yapay Zeka Çıkarımı (Inference). stream=True ile bellek dostu analiz
                results = self.model(frame, stream=True, verbose=False)

                # 3. Aşama: Bounding Box Çizimi
                for r in results:
                    frame = r.plot()

                # 4. Aşama: HUD (O.S.D) İlavesi
                frame = self.draw_hud(frame)

                # 5. Aşama: Sonucu Terminal (Pencere) Aktarımı
                cv2.imshow(self.sistem_ismi, frame)

                # 6. Aşama: Asenkron Manuel Müdahale Kontrolü
                if self.handle_keyboard():
                    break

        except KeyboardInterrupt:
            print("\n[Sistem]: Zorunlu kapatma (KeyboardInterrupt) tespit edildi.")
        except Exception as e:
            print(
                f"\n[Hata]: Main Loop içerisinde beklenmeyen runtime (çalışma zamanı) hatası: {e}"
            )
        finally:
            # İşlem nasıl sonlanırsa sonlansın mutlaka kaynakların bırakılmasını garanti eder
            self.cleanup()

    def cleanup(self):
        """Portları serbest bırakarak güvenli kapanış (Graceful Shutdown) sağlar."""
        print("[Sistem]: Tüketilen port ve ram kaynakları serbest bırakılıyor...")
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print(f"[Sistem]: {self.sistem_ismi} başarılı şekilde kapatıldı.")


if __name__ == "__main__":
    app = VigilantCore()
    app.run()
