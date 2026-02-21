<h1 align="center">🖼️ Image Toolkit Pro</h1>
<h3 align="center">// convert & compress any image. 100% offline.</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=flat-square&logo=windows" />
  <img src="https://img.shields.io/badge/Language-Python-green?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Version-1.0-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Offline-100%25-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Made%20by-Skyvee Tech-red?style=flat-square" />
</p>

---

## 📌 About

**Image Toolkit Pro** by SKYVEE TECH adalah kumpulan dua tool pengolah gambar berbasis terminal yang bekerja **100% offline**.

Tidak perlu upload foto ke website, tidak perlu internet, tidak perlu khawatir privasi. Semua proses dilakukan langsung di PC kamu.

> 🔒 **Your images never leave your PC.**

---

## 📦 Tools yang Tersedia

| Tool | File | Fungsi |
|------|------|--------|
| 🔄 Image Converter | `SKYVEE_TECH_IMG_CONVERTER.exe` | Convert gambar ke format apapun |
| 🗜️ Image Compressor | `SKYVEE_TECH_IMG_COMPRESSOR.exe` | Compress gambar, kurangi ukuran file |

---

## 🔄 Image Converter

### Features
- Convert 1 file atau seluruh folder sekaligus
- Support 8 format input dan 8 format output
- ICO Generator otomatis berbagai ukuran (256x256 sampai 16x16)

### Supported Formats

| | Format |
|--|--------|
| **Input** | JPG, JPEG, PNG, BMP, WEBP, TIFF, GIF, ICO |
| **Output** | JPG, JPEG, PNG, BMP, WEBP, TIFF, GIF, ICO |

### Cara Pakai
1. Jalankan `SKYVEE_TECH_IMG_CONVERTER.exe`
2. Pilih `[1]` untuk convert 1 file atau `[2]` untuk convert seluruh folder
3. Masukkan path file atau folder
4. Pilih format output
5. Hasil tersimpan di folder `converted/`

```
  [?] Path file    : D:\Photos\foto.png

  Pilih format output:
  [1]  JPG   [2]  PNG   [3]  BMP   [4]  WEBP
  [5]  TIFF  [6]  ICO   [7]  GIF   [8]  JPEG

  [+] Berhasil!
  Format asal   : PNG  →  Format baru : ICO
  Size sebelum  : 245.3 KB
  Size sesudah  : 12.1 KB
  Output        : D:\Photos\converted\foto.ico
```

---

## 🗜️ Image Compressor

### Features
- Compress 1 foto atau seluruh folder sekaligus
- Mode kualitas: High (85%), Medium (65%), Low (40%), Custom
- Mode target ukuran: tentukan ukuran output yang diinginkan (contoh: 500kb, 1mb)
- Auto binary search untuk menemukan kualitas terbaik sesuai target

### Cara Pakai
1. Jalankan `SKYVEE_TECH_IMG_COMPRESSOR.exe`
2. Pilih `[1]` untuk compress 1 foto atau `[2]` untuk compress seluruh folder
3. Masukkan path file atau folder
4. Pilih mode kompresi:
   - `[1]` Berdasarkan Kualitas (High/Medium/Low/Custom %)
   - `[2]` Berdasarkan Target Ukuran (contoh: `500kb`, `1mb`)
5. Hasil tersimpan di folder `compressed/`

```
  [?] Path foto    : D:\Photos\foto.jpg
  
  Pilih mode kompresi:
  [1]  Berdasarkan Kualitas
  [2]  Berdasarkan Target Ukuran

  [?] Target size  : 500kb

  [*] Mencari kualitas terbaik...

  [+] Berhasil!
  Size sebelum  : 3.20 MB
  Size sesudah  : 498.7 KB
  Hemat         : 84.7%
  Output        : D:\Photos\compressed\foto.jpg
```

---

## 💡 Kenapa Pakai Ini vs Website Online?

| | Image Toolkit Pro | Website Online |
|--|--|--|
| Internet | ❌ Tidak butuh | ✅ Wajib |
| Privasi | ✅ Foto tidak kemana-mana | ⚠️ Foto diupload ke server |
| Batch Convert | ✅ Ratusan foto sekaligus | ❌ Satu-satu |
| Kecepatan | ✅ Langsung di PC | ⏳ Tergantung koneksi |
| Gratis | ✅ Selamanya | ⚠️ Kadang ada limit |

---

## 🚀 Download & Install

1. Pergi ke halaman **[Releases](../../releases)**
2. Download file `.exe` yang diinginkan
3. Double klik untuk menjalankan
4. Done! Tidak perlu install apapun.

> ⚠️ Jika Windows Defender memblokir, klik **More Info** lalu **Run Anyway**. Ini adalah False Positive dari PyInstaller.

---

## 🛠️ Developer Guide

### Requirements
- Python 3.8+
- pip

### Clone Repository

```bash
git clone https://github.com/Skyvee-Tech/Image-Toolkit.git
cd Image-Toolkit
```

### Install Dependencies

```bash
pip install Pillow colorama
```

### Jalankan Script

```bash
# Image Converter
python SKYVEE_TECH_IMG_CONVERTER.py

# Image Compressor
python SKYVEE_TECH_IMG_COMPRESSOR.py
```

### Build ke .exe

```bash
pip install pyinstaller

# Image Converter
pyinstaller --onefile --icon=icon.ico SKYVEE_TECH_IMG_CONVERTER.py

# Image Compressor
pyinstaller --onefile --icon=icon.ico SKYVEE_TECH_IMG_COMPRESSOR.py
```

### Struktur File

```
📁 Image-Toolkit
├── SKYVEE_TECH_IMG_CONVERTER.py    <- source code converter
├── SKYVEE_TECH_IMG_COMPRESSOR.py   <- source code compressor
├── SKYVEE_TECH_IMG_CONVERTER.exe   <- executable converter
├── SKYVEE_TECH_IMG_COMPRESSOR.exe  <- executable compressor
├── README.md
└── LICENSE
```

### Dependencies

| Library | Fungsi | Install |
|---------|--------|---------|
| `Pillow` | Baca, tulis, konversi gambar | `pip install Pillow` |
| `colorama` | Tampilan berwarna di terminal | `pip install colorama` |

---


## ⚠️ Disclaimer

Tool ini dibuat untuk keperluan **edukasi dan penggunaan pribadi**.
Developer tidak bertanggung jawab atas penyalahgunaan tool ini.

---

## 📜 License

MIT License — bebas dipakai, dimodifikasi, dan disebarkan.
Tetap cantumkan credit ya. 😎

---

<p align="center">Made with 💻 by <a href="https://github.com/Skyvee-Tech">Skyvee Tech</a></p>