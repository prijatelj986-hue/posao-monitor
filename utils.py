"""Zajedničke pomoćne funkcije."""

# Ključne reči (stem-ovi, bez dijakritika, mala slova)
# Kalkulant / normiranje / tender / tehnička priprema
KEYWORDS = [
    "kalkulant",
    "normiranj",      # normiranje, normiranju...
    "tender",
    "tehnick",        # tehnička priprema, tehnicki...
]

TRANS = str.maketrans("šđčćžŠĐČĆŽ", "sdcczSDCCZ")


def normalize_text(s: str) -> str:
    """Skida dijakritike i baca u mala slova radi pouzdanijeg poređenja."""
    if not s:
        return ""
    return s.translate(TRANS).lower()


def matches_keywords(title: str) -> bool:
    """Da li naslov oglasa sadrži neku od praćenih ključnih reči."""
    t = normalize_text(title)
    return any(k in t for k in KEYWORDS)
