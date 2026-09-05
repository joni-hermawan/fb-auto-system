"""
content.py
Ambil narasi Kisah Nabi per-episode dari content_bank.py (GRATIS, sudah ditulis
sekali di awal, tanpa API berbayar).

Kalau ANTHROPIC_API_KEY diisi di .env, sistem bisa opsional generate variasi
narasi baru via Claude API -- tapi ini TIDAK WAJIB, sistem tetap 100% gratis
dan otomatis tanpa API key sama sekali.
"""

import os
from content_bank import NABI_STORIES


def generate_episode_narration(nabi: str, part: int, total_parts: int, is_new_nabi: bool) -> str:
    """
    Ambil narasi episode dari bank lokal (gratis).
    Kalau ANTHROPIC_API_KEY tersedia, bisa dipakai untuk membuat variasi baru
    (opsional, tidak wajib).
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    use_ai_variation = os.getenv("USE_AI_VARIATION", "false").lower() == "true"

    if api_key and use_ai_variation:
        try:
            return _generate_via_claude(nabi, part, total_parts, is_new_nabi, api_key)
        except Exception as e:
            print(f"[content.py] Gagal generate via Claude, pakai bank lokal: {e}")

    # Default: pakai bank lokal (gratis, tanpa API)
    stories = NABI_STORIES.get(nabi)
    if not stories or part > len(stories):
        return (
            f"Materi untuk Nabi {nabi} bagian {part} belum tersedia di content_bank.py. "
            "Silakan tambahkan narasinya di file tersebut."
        )
    return stories[part - 1]


def _generate_via_claude(nabi: str, part: int, total_parts: int, is_new_nabi: bool, api_key: str) -> str:
    """Opsional: buat variasi narasi baru via Claude API (berbayar, tidak wajib)."""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    context_instruction = (
        f"Ini adalah AWAL kisah Nabi {nabi} (bagian 1 dari {total_parts})."
        if is_new_nabi
        else f"Ini LANJUTAN kisah Nabi {nabi}, bagian {part} dari {total_parts}."
    )

    prompt = (
        f"Tuliskan narasi video pendek (90-130 kata) tentang Kisah Nabi {nabi} "
        f"dalam Bahasa Indonesia. {context_instruction}\n"
        "Rujuk kisah yang sudah umum dikenal dalam riwayat Islam, jangan mengarang detail baru, "
        "jangan mendeskripsikan wajah/rupa nabi. Bahasa santun untuk konten dakwah keluarga. "
        "Jawab HANYA teks narasinya."
    )

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def build_title(nabi: str, part: int, total_parts: int) -> str:
    """Judul singkat untuk ditampilkan di layar video."""
    return f"Kisah Nabi {nabi}\nBagian {part}/{total_parts}"
