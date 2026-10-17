# CompressO - NVIDIA GPU Hızlandırmalı Sürüm (CompressO-GPU)

Bu proje [codeforreal1/compressO](https://github.com/codeforreal1/compressO) projesinin NVIDIA GPU (NVENC / CUDA) donanım hızlandırmalı olarak yeniden yapılandırılmış ve optimize edilmiş sürümüdür.

---

## ⚡ Eklenen GPU Özellikleri

1. **NVIDIA GPU Otomatik Tespiti (WGPU + NVENC)**:
   - Sistemdeki NVIDIA ekran kartları (GeForce RTX/GTX/Quadro) otomatik olarak algılanır.
   - Algılanan GPU adı (örn. *NVIDIA GeForce RTX 3060*) arayüzde gerçek zamanlı durum rozeti olarak gösterilir.

2. **NVENC Donanım Hızlandırmalı Video Kodlama**:
   - **H.264 (NVIDIA GPU ⚡)**: `h264_nvenc` donanım kodlayıcısı.
   - **H.265 / HEVC (NVIDIA GPU ⚡)**: `hevc_nvenc` donanım kodlayıcısı (yüksek sıkıştırma oranı + ultra hızlı).
   - CPU kodlamaya kıyasla **10x - 20x kat daha hızlı** sıkıştırma!

3. **GPU Donanım Tabanlı Kod Çözme (Hardware Decoding)**:
   - Girdi videoları açılırken `-hwaccel auto` desteği ile GPU üzerinden çözümlenir, böylece CPU darboğazı ortadan kalkar.

4. **NVENC için Akıllı Kalite & Preset Eşleme (CQ / Constant Quality)**:
   - NVENC çipleri `-crf` yerine `-rc:v vbr -cq:v <val> -b:v 0` değişken bit hızı / sabit kalite modunu kullanır.
   - "Thunderbolt" profili için düşük gecikmeli hızlı preset (`-preset p2 -tune ll`),
   - "Ironclad" profili için maksimum kalite ve verimlilik preseti (`-preset p6 -tune hq`) otomatik olarak uygulanır.

5. **Kullanıcı Arayüzü (UI) Entegrasyonu**:
   - Video ayarları sekmesinin en üstünde **"GPU Acceleration (NVENC)"** anahtarı eklenmiştir.
   - NVIDIA GPU takılı sistemlerde varsayılan olarak açık gelir; kullanıcı isterse tek tıkla CPU moduna geçiş yapabilir.
   - Codec seçim listesinde `H.264 (NVIDIA GPU ⚡)` ve `H.265 / HEVC (NVIDIA GPU ⚡)` seçenekleri doğrudan seçilebilir.

---

## 🚀 Çalıştırma

Projeyi başlatmak için aşağıdaki yöntemlerden birini kullanabilirsiniz:

### Yöntem 1: Hızlı Başlatıcı (Önerilen)
Klasördeki `run-compressO-gpu.bat` dosyasına çift tıklayarak doğrudan çalıştırabilirsiniz.

### Yöntem 2: Terminalden Çalıştırma
```powershell
# Geliştirici modunda çalıştırmak için:
npx pnpm tauri dev

# Veya derlenmiş binary'yi doğrudan çalıştırmak için:
.\src-tauri\target\debug\compressO.exe
```

---

## 🛠️ Teknik Gereksinimler
- **İşletim Sistemi**: Windows 10/11 64-bit
- **Ekran Kartı**: NVIDIA GeForce GTX / RTX veya Quadro serisi
- **Sürücü**: NVIDIA Game Ready veya Studio Driver (NVENC destekli)
- **FFmpeg**: Proje içerisinde donanım hızlandırma destekli FFmpeg ikilisi yerleşik olarak bulunmaktadır.
