"""Scraper za poslovi.rs — pretraga (JS forma) nije lako dostupna preko
requests-a, pa se umesto nje prate statične kategorije koje odgovaraju
profilu (mašinstvo, građevina, ekonomija/tehnička priprema...), a naslovi
se filtriraju po ključnim rečima."""

import requests
from bs4 import BeautifulSoup

from utils import matches_keywords

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; posao-monitor/1.0)"}

CATEGORIES = [
    "masinstvo",
    "gradevina-i-geodezija",
    "ekonomija-i-menadzment",
    "tehnicke-usluge-i-odrzavanje",
]


def fetch_poslovirs():
    results = []
    for cat in CATEGORIES:
        url = f"https://www.poslovi.rs/category/{cat}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code != 200:
                print(f"[poslovi.rs] {cat}: HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select("a[href*='/job/']"):
                href = a.get("href", "")
                if not href:
                    continue
                if not href.startswith("http"):
                    href = "https://www.poslovi.rs" + href
                title = a.get_text(strip=True)
                if not title or not matches_keywords(title):
                    continue

                job_id = href.rstrip("/").split("/")[-1]
                results.append({
                    "id": f"poslovirs-{job_id}",
                    "title": title,
                    "url": href,
                    "source": "Poslovi.rs",
                })
        except Exception as e:
            print(f"[poslovi.rs] greška za '{cat}': {e}")
    return results


if __name__ == "__main__":
    for job in fetch_poslovirs():
        print(job)
