# ✉️ VerifMail by Kaydenzo

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Made with Rich](https://img.shields.io/badge/UI-Rich-28a745)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

> 🔐 Script otomatis untuk **verifikasi email dan deteksi OTP/link verifikasi** dari layanan email sementara.  
> 💡 Cocok untuk testing pendaftaran akun, automation, dan bypass email manual.

---

## 🚀 Fitur Utama

- ✅ Mendukung beberapa layanan email sementara:
  - `mail.tm`
  - `mail.gw`
  - `guerrillamail.com`
  - `mailnesia.com`
- 🔗 Deteksi otomatis:
  - Link verifikasi (termasuk tombol seperti "Verifikasi di sini")
  - OTP (angka 4–8 digit)
- 📩 Preview isi email secara rapi
- 🖥️ Tampilan terminal yang elegan dengan [Rich](https://github.com/Textualize/rich)
- 🔄 Bisa mengulangi proses verifikasi tanpa keluar program

---

## 📥 Instalasi

```bash
git clone https://github.com/username/verifmail.git
cd verifmail
pip install -r requirements.txt
```

---

## ▶️ Cara Menjalankan
```bash
python bot.py
```
Pilih salah satu layanan email sementara (1–4)

Gunakan email tersebut untuk mendaftar di situs target

Setelah email masuk, script akan:

Menampilkan pengirim, subjek, dan isi email

Mendeteksi link verifikasi (jika ada)

Mendeteksi OTP (jika ada)



---

## 📦 Contoh Output
```bash
📩 INFORMASI EMAIL:
Pengirim : support@example.com
Subjek   : Verifikasi Akun Anda

📨 PREVIEW EMAIL:
Halo pengguna,
Silakan klik tombol di bawah untuk memverifikasi akun Anda.
Terima kasih telah menggunakan layanan kami.

🔗 Link verifikasi ditemukan: https://example.com/verify/12345
✅ Verifikasi berhasil!

Jika tidak ditemukan:

⚠️ Tidak ada link atau OTP terdeteksi.
```

---

## ⚠️ Catatan Penting

Script ini hanya digunakan untuk keperluan legal dan edukasi.

Beberapa layanan email sementara bisa berubah atau tidak stabil, jadi pastikan mencoba dari beberapa layanan yang tersedia.

Jangan gunakan untuk aktivitas ilegal seperti spam atau phishing.



---

🙋‍♂️ Pembuat

👤 Kaydenzo


---

📄 Lisensi

Proyek ini menggunakan MIT License — silakan gunakan, modifikasi, dan bagikan dengan tetap mencantumkan kredit pembuat.
