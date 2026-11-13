import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import ctypes
import time
import os

# Windows dahili ses tuşu simülasyonu (Ekstra kütüphane gerektirmez)
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def ses_degistir(yon):
    try:
        if yon == "artir":
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
        elif yon == "azalt":
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)
    except Exception:
        pass # Windows dışı sistemlerde hata vermesini engeller

# Model dosyasının varlığını kontrol et
model_yolu = "hand_landmarker.task"
if not os.path.exists(model_yolu):
    print(f"HATA: '{model_yolu}' dosyası bulunamadı! Lütfen kodu çalıştırmadan önce model dosyasını aynı klasöre indirin.")
    exit()

# Güncel MediaPipe HandLandmarker kurulumu
base_options = python.BaseOptions(model_asset_path=model_yolu)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6
)
detector = vision.HandLandmarker.create_from_options(options)

# El iskeleti bağlantı çizgileri için nokta çiftleri
EL_BAGLANTILARI = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Başparmak
    (0, 5), (5, 6), (6, 7), (7, 8),        # İşaret
    (5, 9), (9, 10), (10, 11), (11, 12),   # Orta
    (9, 13), (13, 14), (14, 15), (15, 16), # Yüzük
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Serçe ve Avuç
]

TIP_IDS = [4, 8, 12, 16, 20]

# Çalışan kamerayı otomatik bul (0, 1 veya 2)
cap = None
for kamera_idx in [0, 1, 2]:
    temp_cap = cv2.VideoCapture(kamera_idx)
    if temp_cap.isOpened():
        ret, _ = temp_cap.read()
        if ret:
            cap = temp_cap
            print(f"Kamera {kamera_idx} başarıyla açıldı.")
            break
    temp_cap.release()

if cap is None:
    print("HATA: Hiçbir kameraya bağlanılamadı! Kamera izinlerini veya bağlantısını kontrol edin.")
    exit()

son_ses_zamani = 0

while True:
    success, img = cap.read()
    if not success:
        print("Kare okunamadı, çıkılıyor...")
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    
    # MediaPipe için görüntüyü hazırlama
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
    
    # El tespiti yap
    detection_result = detector.detect(mp_image)
    
    acik_parmak_sayisi = 0
    durum_mesaji = "El Bekleniyor..."

    if detection_result.hand_landmarks:
        hand_landmarks = detection_result.hand_landmarks[0]
        handedness = detection_result.handedness[0][0].category_name # 'Left' veya 'Right'
        
        noktalar = []
        for idx, lm in enumerate(hand_landmarks):
            cx, cy = int(lm.x * w), int(lm.y * h)
            noktalar.append((cx, cy))

        # 1. Eklem bağlantı çizgilerini çiz
        for baslangic, bitis in EL_BAGLANTILARI:
            cv2.line(img, noktalar[baslangic], noktalar[bitis], (255, 255, 255), 2)

        # 2. Eklem noktalarını çiz
        for idx, (cx, cy) in enumerate(noktalar):
            renk = (0, 0, 255) if idx in TIP_IDS else (0, 255, 0)
            cv2.circle(img, (cx, cy), 6, renk, cv2.FILLED)

        # 3. Açık parmakları hesapla
        parmaklar = []
        
        # Başparmak (Görüntü aynalandığı için Left/Right ters çalışır)
        if handedness == "Left": # Ekranda sağ el gibi görünür
            parmaklar.append(1 if noktalar[4][0] < noktalar[3][0] else 0)
        else:
            parmaklar.append(1 if noktalar[4][0] > noktalar[3][0] else 0)

        # Diğer 4 parmak
        for id in range(1, 5):
            parmaklar.append(1 if noktalar[TIP_IDS[id]][1] < noktalar[TIP_IDS[id] - 2][1] else 0)

        acik_parmak_sayisi = parmaklar.count(1)

        # 4. BONUS: Parmak sayısıyla ses kontrolü
        # 5 parmak açık -> Ses Artır | 1 parmak açık -> Ses Azalt | Diğerleri -> Sabit
        su_an = time.time()
        if acik_parmak_sayisi == 5:
            durum_mesaji = "Ses Artiriliyor (+)"
            if su_an - son_ses_zamani > 0.15:
                ses_degistir("artir")
                son_ses_zamani = su_an
        elif acik_parmak_sayisi == 1:
            durum_mesaji = "Ses Azaltiliyor (-)"
            if su_an - son_ses_zamani > 0.15:
                ses_degistir("azalt")
                son_ses_zamani = su_an
        else:
            durum_mesaji = "Ses Sabit"

    # Bilgi paneli
    cv2.rectangle(img, (15, 15), (370, 125), (20, 20, 20), cv2.FILLED)
    cv2.putText(img, f"Acik Parmak: {acik_parmak_sayisi}", (30, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f"Durum: {durum_mesaji}", (30, 105), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

    cv2.imshow("YZT - Proje 2: El Takibi", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
