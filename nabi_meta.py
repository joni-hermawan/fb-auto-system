"""
nabi_meta.py
Metadata visual per-nabi: tema background yang relevan dengan kisahnya,
dan warna aksen supaya tiap nabi punya identitas visual yang beda.
"""

# Tema pencarian video background yang relevan dengan kisah masing-masing nabi
# (tetap non-figuratif -- tidak ada sosok manusia/wajah)
NABI_THEMES = {
    "Adam": ["lush green garden nature", "paradise forest sunlight"],
    "Idris": ["ancient stars astronomy sky", "old scroll manuscript writing"],
    "Nuh": ["stormy sea waves dark", "flood rain ocean clouds"],
    "Hud": ["desert sand storm wind", "dust storm desert"],
    "Saleh": ["rocky canyon mountain desert", "carved rock cliff desert"],
    "Ibrahim": ["fire flames night desert", "bonfire embers dark"],
    "Luth": ["dark storm clouds ruins", "ancient ruins desert"],
    "Ismail": ["desert oasis palm water", "desert well spring"],
    "Ishaq": ["olive tree hills landscape", "green hills countryside"],
    "Yaqub": ["desert caravan starry night", "night desert stars"],
    "Yusuf": ["egypt desert pyramid", "ancient egyptian architecture"],
    "Ayyub": ["healing spring water desert", "clear water spring nature"],
    "Syu'aib": ["ancient marketplace desert", "desert trade route caravan"],
    "Musa": ["red sea waves shore", "desert parted horizon dramatic"],
    "Harun": ["desert mountain sinai", "rocky desert mountain"],
    "Zulkifli": ["calm desert dusk peaceful", "quiet desert sunset"],
    "Daud": ["ancient fortress hills", "stone castle ruins"],
    "Sulaiman": ["golden palace interior islamic", "islamic palace architecture ornate"],
    "Ilyas": ["dry cracked earth drought", "arid drought landscape"],
    "Ilyasa": ["green valley river nature", "river flowing valley"],
    "Yunus": ["deep ocean dark water", "underwater ocean depth"],
    "Zakaria": ["ancient temple jerusalem stone", "old stone temple architecture"],
    "Yahya": ["peaceful river nature flow", "river jordan landscape"],
    "Isa": ["olive garden ancient landscape", "jerusalem hills ancient"],
    "Muhammad": ["mecca mountain desert cave", "desert mountain cave landscape"],
}

# Warna aksen unik per nabi (hex) -- dipakai untuk warna teks/garis di video
# supaya penonton bisa "mengenali" episode nabi mana secara visual
_PALETTE = [
    "#D4AF37",  # emas
    "#2E7D6B",  # hijau tosca
    "#1E3A5F",  # biru navy
    "#8B4513",  # coklat tanah
    "#6B2D5C",  # ungu tua
    "#B85C38",  # terracotta
    "#3D5A80",  # biru abu
    "#7A5C61",  # mauve
]

NABI_COLORS = {
    nabi: _PALETTE[i % len(_PALETTE)]
    for i, nabi in enumerate(NABI_THEMES.keys())
}


def get_theme_queries(nabi: str) -> list[str]:
    return NABI_THEMES.get(nabi, ["desert landscape nature", "night sky stars"])


def get_accent_color(nabi: str) -> str:
    return NABI_COLORS.get(nabi, "#D4AF37")
