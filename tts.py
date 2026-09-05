"""
tts.py
Mengubah teks quote jadi file audio voiceover.
Pakai gTTS (gratis, butuh internet, kualitas cukup bagus untuk Bahasa Indonesia).

Alternatif berbayar dengan kualitas lebih natural: ElevenLabs API (tinggal ganti isi fungsi ini).
"""

from gtts import gTTS
import os


def generate_voiceover(text: str, output_path: str, lang: str = "id") -> str:
    """Generate file audio .mp3 dari teks. Return path file audio."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    return output_path
