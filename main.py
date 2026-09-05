"""
main.py
Orkestrasi harian untuk series "Kisah Nabi" (berlanjut tiap hari, seperti sinetron):
  1. Cek episode hari ini (nabi mana, bagian ke berapa) via series_state.py
  2. Generate narasi episode tsb via Claude API (merujuk kisah yang umum dikenal)
  3. Buat voiceover (TTS)
  4. Susun video (background non-figuratif + judul + audio)
  5. Upload otomatis ke Facebook Page

Jalankan manual:
  python main.py              # generate & build, tunggu review
  python main.py --confirm-upload   # generate, build, DAN upload

Jalankan otomatis harian (Linux/Mac, via cron):
  0 19 * * * cd /path/to/fb-auto-system && /usr/bin/python3 main.py --confirm-upload >> log.txt 2>&1
"""

import os
import datetime
from dotenv import load_dotenv

from content import generate_episode_narration, build_title
from series_state import get_current_episode, advance_to_next
from tts import generate_voiceover
from video_builder import build_video
from facebook_poster import upload_video_to_page

load_dotenv()

REVIEW_BEFORE_UPLOAD = True  # set False HANYA kalau sudah yakin mau full-otomatis tanpa review


def main():
    today = datetime.date.today().isoformat()
    print(f"=== Menjalankan series Kisah Nabi untuk tanggal {today} ===")

    # 1. Cek episode hari ini & majukan state utk besok
    episode = get_current_episode()
    nabi = episode["nabi"]
    part = episode["part"]
    total_parts = episode["total_parts"]
    print(
        f"[1/5] Episode hari ini: Nabi {nabi} "
        f"(nabi ke-{episode['nabi_urutan_ke']}/{episode['total_nabi']}), "
        f"bagian {part}/{total_parts}"
    )

    # 2. Generate narasi
    narasi = generate_episode_narration(nabi, part, total_parts, episode["is_new_nabi"])
    print(f"[2/5] Narasi:\n{narasi}\n")

    # >>> TITIK REVIEW MANUAL DISARANKAN DI SINI, terutama untuk konten religi <<<
    # Anda bisa cek isi 'narasi' di atas dulu sebelum lanjut ke voiceover & upload.

    # 3. Generate voiceover
    voice_path = f"output/voice_{today}.mp3"
    generate_voiceover(narasi, voice_path, lang=os.getenv("VIDEO_LANG", "id"))
    print(f"[3/5] Voiceover disimpan di {voice_path}")

    # 3. Pastikan background video tersedia (auto-download gratis, KONTEKSTUAL per nabi)
    from assets_fetcher import ensure_background_for_nabi, get_random_background_for_nabi
    ensure_background_for_nabi(nabi)
    background_path = get_random_background_for_nabi(nabi)

    # 4. Build video (bumper intro + judul singkat + background kontekstual + warna aksen)
    title_text = build_title(nabi, part, total_parts)
    video_name = f"video_{today}.mp4"
    video_path = build_video(
        title_text, voice_path, video_name, nabi=nabi, background_path=background_path
    )
    print(f"[4/5] Video jadi: {video_path}")

    # Review manual sebelum upload
    if REVIEW_BEFORE_UPLOAD:
        print(
            "\n>>> REVIEW_BEFORE_UPLOAD aktif. "
            f"Cek dulu video & narasi di atas.\n"
            ">>> Kalau sudah oke, jalankan ulang: python main.py --confirm-upload\n"
            ">>> (Ini TIDAK akan generate ulang/majukan episode -- lihat catatan di README "
            "soal cara re-run episode yang sama kalau perlu revisi.)\n"
        )
        import sys

        if "--confirm-upload" not in sys.argv:
            return

    # 5. Upload ke Facebook
    caption = (
        f"Kisah Nabi {nabi} - Bagian {part}/{total_parts}\n\n"
        f"{narasi}\n\n"
        "#kisahnabi #islamedukasi #ceritaislami #dakwah"
    )
    result = upload_video_to_page(video_path, caption)
    print(f"[5/5] Upload selesai. Response: {result}")

    # Baru majukan episode SETELAH upload sukses
    advance_to_next()
    print("[series_state] Episode dimajukan untuk besok.")


if __name__ == "__main__":
    main()
