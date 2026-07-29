"""Scraper za LinkedIn preko javnog 'guest' pretraživača poslova
(ne zahteva prijavu). Ova ruta je poznata po tome da je LinkedIn s
vremena na vreme menja ili ograničava, pa je ovo najosetljiviji deo
sistema — ako prestane da vraća rezultate, najverovatnije treba
prilagoditi 'selectors' ispod ili dodati headere/kašnjenje."""

import time
import requests
from bs4 import BeautifulSoup

from utils import matches_keywords

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
}

SEARCH_TERMS = ["kalkulant", "normiranje tendera", "tehnicka priprema"]


def fetch_linkedin():
    results = []
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    for kw in SEARCH_TERMS:
        params = {
            "keywords": kw,
            "location": "Serbia",
            "f_TPR": "r172800",  # poslednja 48h
            "start": 0,
        }
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=20)
            if r.status_code != 200:
                print(f"[linkedin] '{kw}': HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.select("li"):
                link_el = card.select_one("a.base-card__full-link")
                title_el = card.select_one("h3")
                company_el = card.select_one("h4")
                if not link_el or not title_el:
                    continue
                href = link_el.get("href", "").split("?")[0]
                title = title_el.get_text(strip=True)
                company = company_el.get_text(strip=True) if company_el else ""

                # LinkedIn-ova sopstvena pretraga pogađa i opis posla, ne
                # samo naslov, pa dodatno filtriramo po naslovu da ne
                # dobijemo gomilu nepovezanih oglasa.
                if not matches_keywords(title):
                    continue

                job_id = href.rstrip("/").split("-")[-1]

                results.append({
                    "id": f"linkedin-{job_id}",
                    "title": f"{title} — {company}" if company else title,
                    "url": href,
                    "source": "LinkedIn",
                })
        except Exception as e:
            print(f"[linkedin] greška za '{kw}': {e}")
        time.sleep(1.5)
    return results


if __name__ == "__main__":
    for job in fetch_linkedin():
        print(job)
