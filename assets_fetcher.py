"""
assets_fetcher.py
Otomatis download background video GRATIS dari Pexels, DISESUAIKAN dengan
tema kisah nabi yang sedang berjalan (bukan acak murni) -- supaya lebih
relevan dan tidak monoton.

Struktur folder: assets/backgrounds/<nabi>/video1.mp4, video2.mp4, ...
"""

import os
import random
import requests
from nabi_meta import get_theme_queries

BACKGROUND_DIR = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
MIN_PER_NABI = 2  # minimal video unik per nabi supaya tidak itu-itu saja


def _nabi_folder(nabi: str) -> str:
    slug = nabi.lower().replace("'", "").replace(" ", "_")
    return os.path.join(BACKGROUND_DIR, slug)


def _count_existing(folder: str) -> int:
    if not os.path.isdir(folder):
        return 0
    return len([f for f in os.listdir(folder) if f.endswith((".mp4", ".mov"))])


def ensure_background_for_nabi(nabi: str) -> None:
    """
    Pastikan folder assets/backgrounds/<nabi>/ punya cukup video bertema
    relevan dengan kisah nabi tersebut. Aman dipanggil berkali-kali.
    """
    folder = _nabi_folder(nabi)
    existing = _count_existing(folder)
    if existing >= MIN_PER_NABI:
        return

    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print(
            f"[assets_fetcher] PEXELS_API_KEY belum diisi -- lewati auto-download untuk {nabi}. "
            "Isi manual video di folder tersebut, atau daftar API key gratis di pexels.com/api"
        )
        return

    os.makedirs(folder, exist_ok=True)
    themes = get_theme_queries(nabi)
    needed = MIN_PER_NABI - existing
    headers = {"Authorization": api_key}

    for theme in themes[:needed] if needed < len(themes) else themes:
        try:
            resp = requests.get(
                "https://api.pexels.com/videos/search",
                headers=headers,
                params={"query": theme, "orientation": "portrait", "per_page": 1},
                timeout=30,
            )
            resp.raise_for_status()
            videos = resp.json().get("videos", [])
            if not videos:
                continue

            video_files = sorted(videos[0]["video_files"], key=lambda v: v.get("width", 9999))
            video_url = next(
                (v["link"] for v in video_files if v.get("width", 0) >= 720),
                video_files[-1]["link"],
            )

            out_path = os.path.join(folder, f"{theme.replace(' ', '_')}.mp4")
            data = requests.get(video_url, timeout=60)
            with open(out_path, "wb") as f:
                f.write(data.content)
            print(f"[assets_fetcher] Berhasil download untuk {nabi}: {out_path}")
        except Exception as e:
            print(f"[assets_fetcher] Gagal download tema '{theme}' untuk {nabi}: {e}")


def get_random_background_for_nabi(nabi: str) -> str | None:
    """Ambil path video background acak dari folder nabi tersebut, kalau ada."""
    folder = _nabi_folder(nabi)
    if not os.path.isdir(folder):
        return None
    files = [f for f in os.listdir(folder) if f.endswith((".mp4", ".mov"))]
    if not files:
        return None
    return os.path.join(folder, random.choice(files))
