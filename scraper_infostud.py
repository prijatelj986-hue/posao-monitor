"""Scraper za poslovi.infostud.com — koristi keyword URL-ove sajta
(npr. https://poslovi.infostud.com/oglasi-za-posao-kalkulant), koji su
server-side renderovani pa ih requests+BeautifulSoup mogu pročitati."""

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; posao-monitor/1.0)"}

# Slug-ovi za pretragu (mala slova, crtice umesto razmaka)
SLUGS = ["kalkulant", "normiranje", "tehnicka-priprema", "tender"]


def fetch_infostud():
    results = []
    for slug in SLUGS:
        url = f"https://poslovi.infostud.com/oglasi-za-posao-{slug}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code != 200:
                print(f"[infostud] {slug}: HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select("a[href*='/posao/']"):
                href = a.get("href", "")
                if not href:
                    continue
                if not href.startswith("http"):
                    href = "https://poslovi.infostud.com" + href
                href = href.split("?")[0]

                title_el = a.select_one("h2, h3")
                title = title_el.get_text(strip=True) if title_el else a.get_text(strip=True)
                if not title:
                    continue

                job_id = href.rstrip("/").split("/")[-1]
                results.append({
                    "id": f"infostud-{job_id}",
                    "title": title,
                    "url": href,
                    "source": "Infostud",
                })
        except Exception as e:
            print(f"[infostud] greška za '{slug}': {e}")
    return results


if __name__ == "__main__":
    for job in fetch_infostud():
        print(job)
