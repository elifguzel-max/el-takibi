# 🖐️ El Takibi ve Hareketle Ses Kontrolü (Hand Tracking & Volume Control)

Bu proje, **OpenCV** ve güncel **MediaPipe Tasks API (`HandLandmarker`)** kullanarak gerçek zamanlı el takibi yapan, açık parmak sayısını hesaplayan ve el hareketleriyle (jestlerle) Windows işletim sisteminde bilgisayarın ses seviyesini kontrol etmenizi sağlayan bir bilgisayarla görü (Computer Vision) uygulamasıdır.

---

## ✨ Özellikler

* **Gerçek Zamanlı El İskeleti Çizimi:** Elinizdeki 21 farklı eklem noktasını ve bu noktalar arasındaki bağlantıları canlı kamera görüntüsü üzerinde çizer.
* **Akıllı Parmak Sayma:** Sağ ve sol el ayrımını otomatik olarak algılayarak (aynalama düzeltmesi dahil) kaç parmağınızın açık olduğunu hassas bir şekilde hesaplar.
* **Temassız Ses Kontrolü (Windows):** Ekstra bir ses kütüphanesine ihtiyaç duymadan doğrudan Windows API (`ctypes`) üzerinden sistem sesini kontrol eder:
  * 🖐️ **5 Parmak Açık:** Sesi artırır (`+`)
  * ☝️ **1 Parmak Açık:** Sesi azaltır (`-`)
  * ✌️ **Diğer Durumlar (0, 2, 3, 4 parmak):** Ses seviyesini sabit tutar.
* **Otomatik Kamera Algılama:** Sisteminize bağlı kameraları (`0`, `1`, `2` indeksleri) otomatik olarak tarar ve çalışan ilk kameraya bağlanır.
* **Bilgi Paneli (HUD):** Ekranın sol üst köşesinde açık parmak sayısını ve aktif ses durumunu anlık olarak gösterir.

---

## 🛠️ Gereksinimler

Projeyi çalıştırmak için sisteminizde **Python 3.8+** yüklü olmalıdır. Gerekli Python kütüphaneleri:

* `opencv-python`
* `mediapipe`

*(Not: Ses kontrolü özelliği Windows'un dahili `user32.dll` kütüphanesini kullandığı için yalnızca Windows işletim sistemlerinde aktiftir. Diğer işletim sistemlerinde el takibi ve parmak sayma özellikleri sorunsuz çalışmaya devam eder.)*

---

## 🚀 Kurulum

1. **Projeyi bilgisayarınıza indirin veya klonlayın:**
   ```bash
   git clone https://github.com/kullanici-adiniz/proje-adi.git
   cd proje-adi
   ```

2. **Gerekli kütüphaneleri yükleyin:**
   ```bash
   pip install opencv-python mediapipe
   ```

3. **MediaPipe Model Dosyasını İndirin (Önemli!):**
   Projenin çalışabilmesi için MediaPipe'ın güncel el tespiti modeline ihtiyacı vardır. Aşağıdaki bağlantıdan `hand_landmarker.task` dosyasını indirin ve Python kodunuzla (`el_takibi.py`) **aynı klasörün içine** yerleştirin:
   * 📥 [hand_landmarker.task İndir (Google MediaPipe Resmi Modeli)](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)

---

## 💻 Kullanım

1. Terminal veya komut istemcisini proje klasöründe açın.
2. Uygulamayı başlatın:
   ```bash
   python el_takibi.py
   ```
   *(Not: Dosya adınız `el_takibi.py.py` ise komutu buna göre güncelleyin veya dosya adını `el_takibi.py` olarak düzeltin.)*
3. Kameranın karşısına geçip elinizi gösterin:
   * Elinizi tamamen açtığınızda (**5 parmak**) bilgisayarınızın sesi kademeli olarak artacaktır.
   * Sadece tek parmağınızı kaldırdığınızda (**1 parmak**) ses kademeli olarak azalacaktır.
4. Uygulamadan çıkmak için klavyeden **`q`** tuşuna basın.

---

## 📂 Proje Yapısı

```text
├── el_takibi.py           # Ana uygulama kodu
├── hand_landmarker.task   # MediaPipe el tespiti model dosyası (Manuel indirilmeli)
└── README.md              # Proje dokümantasyonu
```

---

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak isterseniz lütfen bir *Pull Request* gönderin veya yeni özellik önerileri için *Issue* açın.
