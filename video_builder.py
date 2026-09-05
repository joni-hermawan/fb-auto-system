"""
video_builder.py
Menggabungkan: video background (spesifik per nabi) + teks quote + voiceover
menjadi 1 video Reels-ready (portrait, 1080x1920), dengan:
  - Warna aksen unik per nabi
  - Bumper intro singkat "Kisah Nabi" di awal (identitas visual series)
  - Efek zoom halus (Ken Burns) pada background biar tidak terasa statis

Butuh moviepy + ffmpeg terinstall di sistem.
"""

import os
import random
import glob
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    ColorClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

from nabi_meta import get_accent_color

BACKGROUND_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
MUSIC_DIR = os.path.join(os.path.dirname(__file__), "assets", "music")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

TARGET_W, TARGET_H = 1080, 1920  # portrait untuk Reels
INTRO_DURATION = 1.8  # detik, bumper identitas series
ZOOM_RATE = 0.008  # kecepatan zoom-in per detik (halus, tidak norak)


def _pick_random_file(directory: str, extensions: tuple[str, ...]) -> str | None:
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, f"*{ext}")))
    return random.choice(files) if files else None


def _apply_ken_burns(clip):
    """Efek zoom-in halus supaya background tidak terasa statis/monoton."""
    return clip.resize(lambda t: 1 + ZOOM_RATE * t)


def _build_intro_bumper(accent_color: str, duration: float = INTRO_DURATION):
    """Bumper pembuka singkat sebagai identitas visual series 'Kisah Nabi'."""
    bg = ColorClip(size=(TARGET_W, TARGET_H), color=(15, 15, 20), duration=duration)
    label = (
        TextClip(
            "📖 KISAH NABI",
            fontsize=72,
            color=accent_color,
            font="DejaVu-Sans-Bold",
            method="caption",
            size=(TARGET_W - 200, None),
            align="center",
        )
        .set_position("center")
        .set_duration(duration)
        .fadein(0.3)
        .fadeout(0.3)
    )
    return CompositeVideoClip([bg, label]).set_duration(duration)


def build_video(
    quote_text: str,
    voiceover_path: str,
    output_name: str,
    nabi: str = "",
    background_path: str | None = None,
) -> str:
    """
    Susun video akhir. Return path file video hasil.

    Args:
        quote_text: judul singkat ditampilkan di layar
        voiceover_path: path file audio narasi
        output_name: nama file output
        nabi: nama nabi (untuk pilih warna aksen)
        background_path: path video background spesifik. Kalau None,
            fallback ke folder assets/backgrounds/ generik.
    """
    accent_color = get_accent_color(nabi) if nabi else "#D4AF37"

    bg_path = background_path or _pick_random_file(BACKGROUND_DIR, (".mp4", ".mov"))
    if not bg_path:
        raise FileNotFoundError(
            "Tidak ada video background ditemukan. "
            "Jalankan assets_fetcher.ensure_background_for_nabi() dulu, "
            "atau tambahkan manual video di assets/backgrounds/."
        )

    voice = AudioFileClip(voiceover_path)
    duration = max(voice.duration + 1.5, 8)

    bg = VideoFileClip(bg_path)
    if bg.duration < duration:
        n_loops = int(duration // bg.duration) + 1
        bg = CompositeVideoClip([bg] * n_loops).set_duration(duration)
    else:
        bg = bg.subclip(0, duration)

    bg = bg.resize(height=TARGET_H)
    if bg.w < TARGET_W:
        bg = bg.resize(width=TARGET_W)
    bg = bg.crop(x_center=bg.w / 2, y_center=bg.h / 2, width=TARGET_W, height=TARGET_H)

    # Efek zoom halus (Ken Burns) supaya background terasa hidup, bukan statis
    bg = _apply_ken_burns(bg)

    txt_clip = (
        TextClip(
            quote_text,
            fontsize=64,
            color="white",
            font="DejaVu-Sans-Bold",
            method="caption",
            size=(TARGET_W - 160, None),
            align="center",
            stroke_color=accent_color,
            stroke_width=2,
        )
        .set_position("center")
        .set_duration(duration)
        .fadein(0.5)
    )

    audio_tracks = [voice.set_start(0.5)]
    music_path = _pick_random_file(MUSIC_DIR, (".mp3", ".wav"))
    if music_path:
        music = AudioFileClip(music_path).volumex(0.15).set_duration(duration)
        audio_tracks.append(music)
    final_audio = CompositeAudioClip(audio_tracks)

    main_content = CompositeVideoClip([bg, txt_clip]).set_audio(final_audio).set_duration(duration)

    # Gabungkan bumper intro + konten utama
    intro = _build_intro_bumper(accent_color)
    final = concatenate_videoclips([intro, main_content], method="compose")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_name)
    final.write_videofile(
        output_path, fps=30, codec="libx264", audio_codec="aac", threads=4, logger=None
    )

    voice.close()
    bg.close()
    final.close()

    return output_path
