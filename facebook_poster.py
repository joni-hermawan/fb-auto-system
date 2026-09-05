"""
facebook_poster.py
Upload video ke Facebook Page menggunakan Graph API.

Butuh:
- FB_PAGE_ID
- FB_PAGE_ACCESS_TOKEN (long-lived Page Access Token)
Keduanya diisi di file .env — lihat README.md untuk cara mendapatkannya.
"""

import os
import requests

GRAPH_API_VERSION = "v21.0"  # cek versi terbaru di developers.facebook.com


def upload_video_to_page(video_path: str, description: str) -> dict:
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")

    if not page_id or not access_token:
        raise ValueError(
            "FB_PAGE_ID atau FB_PAGE_ACCESS_TOKEN belum diisi di .env. "
            "Lihat README.md bagian 'Setup Facebook Developer App'."
        )

    url = f"https://graph-video.facebook.com/{GRAPH_API_VERSION}/{page_id}/videos"

    with open(video_path, "rb") as video_file:
        files = {"source": video_file}
        data = {
            "description": description,
            "access_token": access_token,
        }
        response = requests.post(url, files=files, data=data, timeout=300)

    result = response.json()

    if response.status_code != 200:
        raise RuntimeError(f"Upload gagal: {result}")

    print(f"[facebook_poster.py] Berhasil upload. Video ID: {result.get('id')}")
    return result
