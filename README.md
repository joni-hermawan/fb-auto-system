# Sistem Auto Video Generator + Auto Post Facebook

Pipeline: **Quote → Voiceover (TTS) → Video (background+teks+audio) → Upload otomatis ke Facebook Page**

---

## 1. Install Dependency

```bash
# Install ffmpeg dulu (wajib untuk moviepy)
# Ubuntu/Debian:
sudo apt install ffmpeg
# Mac:
brew install ffmpeg
# Windows: download dari ffmpeg.org, tambahkan ke PATH

# Install Python packages
pip install -r requirements.txt
```

---

## 2. Siapkan Assets

- Masukkan minimal 1 video background (durasi 10–30 detik, portrait/landscape bebas — sistem akan crop otomatis ke 1080x1920) ke folder `assets/backgrounds/`
  - Sumber gratis bebas royalti: **Pexels.com** atau **Pixabay.com** (cari "nature", "city", "sunrise", dll sesuai vibe motivasi)
- (Opsional) Masukkan musik instrumental bebas royalti ke `assets/music/` — sistem otomatis mix volume rendah di belakang voiceover

---

## 3. Setup Facebook Developer App & Page Access Token

Ini bagian paling penting biar sistem bisa upload otomatis ke Page Anda.

### Langkah 1 — Buat App di Meta for Developers
1. Buka https://developers.facebook.com/apps
2. Klik **Create App** → pilih tipe **"Other"** → **"Business"**
3. Isi nama app (bebas, misal "FB Auto Poster") → Create

### Langkah 2 — Tambahkan Produk "Facebook Login" & izinkan Pages API
1. Di dashboard app, klik **Add Product** → pilih **Facebook Login**
2. Buka menu **App Review → Permissions and Features**, cari dan minta akses:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - (Untuk akun baru/testing, izin ini biasanya otomatis tersedia dalam mode Development untuk Page yang Anda kelola sendiri — App Review baru dibutuhkan kalau nanti dipakai orang lain)

### Langkah 3 — Ambil Page Access Token via Graph API Explorer
1. Buka https://developers.facebook.com/tools/explorer/
2. Pilih App Anda di dropdown kanan atas
3. Pilih **"Get Page Access Token"** → pilih Page Anda → izinkan permission yang diminta
4. Token yang muncul ini **short-lived** (berlaku ~1-2 jam), perlu ditukar jadi long-lived

### Langkah 4 — Tukar jadi Long-Lived Token (berlaku ~60 hari)
Jalankan request ini (ganti bagian `{}`):

```
GET https://graph.facebook.com/v21.0/oauth/access_token?
  grant_type=fb_exchange_token&
  client_id={APP_ID}&
  client_secret={APP_SECRET}&
  fb_exchange_token={SHORT_LIVED_TOKEN}
```

`APP_ID` dan `APP_SECRET` ada di **Settings → Basic** pada dashboard app Anda.

Hasilnya adalah `FB_PAGE_ACCESS_TOKEN` yang dipakai di `.env`.

> **Catatan**: Long-lived Page token dari App yang statusnya "Live" biasanya tidak expired selama Anda tidak reset. Kalau App masih "Development", token tetap perlu di-refresh tiap ~60 hari — jalankan ulang langkah 3-4.

### Langkah 5 — Cari FB_PAGE_ID
Buka Page Anda → **About** → scroll ke bawah, cari "Page ID". Atau lihat di URL Page Anda.

### Langkah 6 — Isi file `.env`
```bash
cp .env.example .env
# lalu edit .env, isi FB_PAGE_ID dan FB_PAGE_ACCESS_TOKEN
```

---

## 4. Jalankan Sistem

**Mode manual (generate video, review dulu sebelum upload):**
```bash
python main.py
```
Video akan tersimpan di `output/`. Cek dulu hasilnya.

**Setelah yakin video oke, baru upload:**
```bash
python main.py --confirm-upload
```

**Full otomatis tanpa review** (opsional, edit `REVIEW_BEFORE_UPLOAD = False` di `main.py`) — hanya lakukan ini setelah Anda percaya kualitas video konsisten bagus.

---

## 5. Jadwalkan Otomatis Harian (Cron)

```bash
crontab -e
```
Tambahkan baris ini (jalan tiap hari jam 19:00, otomatis upload tanpa review manual):
```
0 19 * * * cd /path/ke/fb-auto-system && /usr/bin/python3 main.py --confirm-upload >> log.txt 2>&1
```

---

## 6. Versi 100% GRATIS + OTOMATIS (Rekomendasi)

Ringkasan apa yang sudah dibuat gratis dan otomatis:

| Bagian | Solusi Gratis |
|---|---|
| Narasi 100 episode | Sudah ditulis di `content_bank.py` — tidak butuh API key sama sekali |
| Background video | Auto-download dari Pexels API (gratis, sekali daftar akun) |
| Suara (TTS) | gTTS, gratis |
| Jadwal harian | GitHub Actions (`.github/workflows/daily-post.yml`) — jalan di server GitHub, PC Anda tidak perlu nyala |
| Token Facebook | Bisa dibuat tidak pernah expired (lihat langkah di bawah) |

### Setup GitHub Actions (sekali saja)

1. Push folder ini ke repository GitHub baru (boleh **private**, GitHub Actions tetap gratis untuk private repo dengan kuota bulanan yang cukup besar)
   ```bash
   git init
   git add .
   git commit -m "Setup sistem kisah nabi"
   git branch -M main
   git remote add origin https://github.com/USERNAME/NAMA-REPO.git
   git push -u origin main
   ```
2. Di GitHub, buka repo → **Settings → Secrets and variables → Actions → New repository secret**, tambahkan 3 secret:
   - `FB_PAGE_ID`
   - `FB_PAGE_ACCESS_TOKEN`
   - `PEXELS_API_KEY` (daftar gratis di https://www.pexels.com/api/)
3. Selesai. Workflow otomatis jalan tiap hari jam 19:00 WIB. Bisa juga dites manual: tab **Actions** → pilih workflow → **Run workflow**

### Membuat Page Access Token yang TIDAK PERNAH EXPIRED

Token biasa dari Graph API Explorer expired ~60 hari. Untuk token permanen (gratis, resmi dari Meta):
1. Buka https://business.facebook.com/settings/system-users
2. Buat **System User** baru (role: Admin), lalu **Add Assets** → hubungkan ke Page Anda dengan akses penuh
3. Klik **Generate New Token** pada System User tersebut, pilih App Anda, centang izin `pages_manage_posts`, `pages_read_engagement`, `pages_show_list`
4. Pilih durasi token **"Never"** (tidak pernah expired) — ini yang membedakan dari token biasa
5. Gunakan token ini sebagai `FB_PAGE_ACCESS_TOKEN`

### Yang tetap perlu dilakukan manual (bukan soal biaya, tapi kualitas & keamanan)

- **Sekali di awal**: baca ulang 100 narasi di `content_bank.py`, idealnya diperiksa orang yang paham agama, sebelum dijadikan full-otomatis
- **Sekali di awal**: buat akun Pexels (gratis) untuk dapat API key
- **Sesekali**: cek hasil postingan di Facebook untuk pastikan tidak ada error teknis (misal background video habis, dsb — cek log di tab Actions)

Di luar itu, sistem berjalan otomatis tanpa biaya berulang.

---

## 7. Tentang Sistem Series "Kisah Nabi"

### Fitur Anti-Monoton (Background & Visual)
- **Background kontekstual per nabi** (`nabi_meta.py`) — setiap nabi punya tema pencarian sendiri yang relevan dengan kisahnya. Contoh: Nabi Nuh → laut/badai, Nabi Musa → gurun/Laut Merah, Nabi Sulaiman → istana emas, Nabi Ibrahim → api/gurun. Video disimpan terpisah per nabi di `assets/backgrounds/<nama_nabi>/`
- **Warna aksen unik per nabi** — 8 palet warna dirotasi (emas, hijau tosca, navy, coklat, ungu, dll) dipakai sebagai warna outline teks judul, supaya penonton bisa "mengenali" secara visual sedang menonton kisah nabi yang mana
- **Bumper intro "📖 KISAH NABI"** — muncul 1.8 detik di awal setiap video sebagai identitas visual series yang konsisten, memberi kesan "ini bagian dari series", bukan video lepas-lepas
- **Efek zoom halus (Ken Burns)** pada background — video perlahan zoom-in sepanjang durasi, supaya terasa lebih hidup dan sinematik dibanding background video statis begitu saja

Sistem ini otomatis melacak progres cerita supaya berlanjut tiap hari (seperti sinetron):

- Urutan: 25 Nabi & Rasul, tiap nabi dibagi 4 bagian/episode (bisa diubah di `series_state.py` → `EPISODES_PER_NABI`)
- Progres disimpan di `output/series_state.json` — **jangan hapus file ini** kalau tidak ingin series-nya reset
- Episode **baru maju ke bagian berikutnya setelah upload berhasil** — kalau Anda generate & cek berulang kali sebelum yakin, episode tidak akan kelewat
- Setelah 25 nabi selesai (100 episode / ±100 hari), series otomatis mengulang dari Nabi Adam lagi

**Reset series dari awal** (kalau perlu mulai ulang):
```python
python -c "from series_state import reset_series; reset_series()"
```

**Ganti/hapus 1 episode yang sudah kadung dijadwalkan tapi belum diupload:**
Edit langsung `output/series_state.json` untuk mengatur ulang `nabi_index` dan `part` sesuai kebutuhan.

### ⚠️ Review Konten Religi — Sangat Disarankan
- Narasi digenerate AI merujuk kisah yang umum dikenal, tapi **AI tetap bisa salah**. Sebelum `--confirm-upload` dijalankan otomatis via cron, disarankan jalankan mode manual dulu (`python main.py` tanpa flag) selama beberapa hari pertama untuk baca narasinya dulu.
- Kalau memungkinkan, minta seseorang yang paham agama mengecek beberapa episode awal.
- **Background video**: gunakan yang non-figuratif (kaligrafi, alam, pola islami, langit, padang pasir) — HINDARI video dengan sosok manusia yang bisa disalahartikan sebagai penggambaran nabi.

---

## 8. Hal Penting yang Perlu Anda Perhatikan

- **Label konten AI**: Facebook mewajibkan label untuk video yang dibuat/dimodifikasi signifikan oleh AI (suara sintetis, avatar AI, dll). Video sistem ini pakai TTS (suara sintetis) — aktifkan opsi "AI-generated content" di pengaturan post kalau Facebook menampilkannya, atau tambahkan disclosure di caption.
- **Kualitas > kuantitas**: sistem ini mempercepat produksi, tapi kualitas quote & pemilihan background tetap pengaruh besar ke engagement. Sesekali cek & ganti isi `content.py` dengan quote yang lebih personal/otentik.
- **Rate limit Graph API**: jangan upload lebih dari yang wajar (1-3x/hari) untuk hindari flag sistem Facebook.
- **Token expired**: kalau upload tiba-tiba gagal dengan error auth, kemungkinan besar token sudah expired — ulangi Langkah 3-4 di atas.
- **Backup akses**: simpan App ID, App Secret, dan token di tempat aman (password manager), jangan pernah share/publish.

---

## 9. Struktur Folder

```
fb-auto-system/
├── .github/workflows/daily-post.yml   # otomasi harian via GitHub Actions (gratis)
├── .env                  # isi kredensial Anda (jangan share!)
├── .env.example
├── content_bank.py       # 100 narasi kisah nabi siap pakai (gratis, tanpa API)
├── content.py            # ambil narasi dari bank + opsi variasi via Claude (opsional)
├── nabi_meta.py          # tema background & warna aksen per nabi (anti-monoton)
├── series_state.py       # pelacak progres episode/series
├── assets_fetcher.py     # auto-download background video kontekstual dari Pexels
├── tts.py                # text-to-speech
├── video_builder.py      # penyusun video (bumper, zoom, warna aksen)
├── facebook_poster.py    # upload ke Facebook Graph API
├── main.py               # orkestrasi utama
├── requirements.txt
├── assets/
│   ├── backgrounds/      # auto-terisi per nabi (subfolder), atau isi manual
│   └── music/            # opsional, musik instrumental
└── output/               # video, audio, & state series tersimpan di sini
```
