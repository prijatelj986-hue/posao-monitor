"""Scraper za helloworld.rs. Sajt je pretežno IT-fokusiran, pa se ovde
prati opšta lista oglasa i filtrira po ključnim rečima — najverovatnije
će ređe pogađati nego ostali izvori, ali ne škodi da ostane uključen."""

import requests
from bs4 import BeautifulSoup

from utils import matches_keywords

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; posao-monitor/1.0)"}


def fetch_helloworld():
    results = []
    url = "https://www.helloworld.rs/oglasi-za-posao/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"[helloworld] HTTP {r.status_code}")
            return results
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.select("a[href*='/posao/']"):
            href = a.get("href", "")
            if not href:
                continue
            if not href.startswith("http"):
                href = "https://www.helloworld.rs" + href
            title = a.get_text(strip=True)
            if not title or not matches_keywords(title):
                continue

            job_id = href.rstrip("/").split("/")[-1]
            results.append({
                "id": f"helloworld-{job_id}",
                "title": title,
                "url": href,
                "source": "HelloWorld",
            })
    except Exception as e:
        print(f"[helloworld] greška: {e}")
    return results


if __name__ == "__main__":
    for job in fetch_helloworld():
        print(job)
