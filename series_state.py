"""
series_state.py
Melacak progres "series" Kisah Nabi supaya konten berlanjut tiap hari
(bagian 1, 2, 3, ... lalu lanjut ke nabi berikutnya) — seperti sinetron.

State disimpan di output/series_state.json supaya persisten antar-run.
"""

import json
import os

STATE_PATH = os.path.join(os.path.dirname(__file__), "output", "series_state.json")

# Urutan 25 Nabi & Rasul dalam Islam (urutan umum yang diajarkan)
NABI_ORDER = [
    "Adam", "Idris", "Nuh", "Hud", "Saleh", "Ibrahim", "Luth", "Ismail",
    "Ishaq", "Yaqub", "Yusuf", "Ayyub", "Syu'aib", "Musa", "Harun",
    "Zulkifli", "Daud", "Sulaiman", "Ilyas", "Ilyasa", "Yunus", "Zakaria",
    "Yahya", "Isa", "Muhammad",
]

EPISODES_PER_NABI = 4  # jumlah bagian/part per kisah nabi (bisa disesuaikan)


def _load_state() -> dict:
    if not os.path.exists(STATE_PATH):
        return {"nabi_index": 0, "part": 1}
    with open(STATE_PATH, "r") as f:
        return json.load(f)


def _save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f)


def get_current_episode() -> dict:
    """
    Intip episode HARI INI tanpa mengubah state.
    Return: {"nabi": str, "part": int, "total_parts": int, "is_new_nabi": bool, ...}
    Panggil advance_to_next() secara terpisah SETELAH upload berhasil.
    """
    state = _load_state()
    nabi_index = state["nabi_index"]
    part = state["part"]

    if nabi_index >= len(NABI_ORDER):
        # Series 25 nabi sudah selesai semua — ulang dari awal (loop)
        nabi_index = 0
        part = 1
        _save_state({"nabi_index": nabi_index, "part": part})

    nabi_name = NABI_ORDER[nabi_index]
    is_new_nabi = part == 1

    return {
        "nabi": nabi_name,
        "part": part,
        "total_parts": EPISODES_PER_NABI,
        "is_new_nabi": is_new_nabi,
        "nabi_urutan_ke": nabi_index + 1,
        "total_nabi": len(NABI_ORDER),
    }


def advance_to_next() -> None:
    """
    Majukan state ke episode berikutnya. Panggil ini HANYA SETELAH video
    berhasil diupload, supaya episode tidak kelewat kalau Anda cek/generate
    ulang beberapa kali sebelum yakin.
    """
    state = _load_state()
    nabi_index = state["nabi_index"]
    part = state["part"]

    next_part = part + 1
    next_nabi_index = nabi_index
    if next_part > EPISODES_PER_NABI:
        next_part = 1
        next_nabi_index += 1

    _save_state({"nabi_index": next_nabi_index, "part": next_part})


def reset_series() -> None:
    """Reset series dari awal (Nabi Adam, part 1). Berguna kalau mau mulai ulang."""
    _save_state({"nabi_index": 0, "part": 1})
