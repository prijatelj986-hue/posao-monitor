import json
from pathlib import Path

from scraper_infostud import fetch_infostud
from scraper_poslovirs import fetch_poslovirs
from scraper_helloworld import fetch_helloworld
from scraper_linkedin import fetch_linkedin
from notify import send_telegram

SEEN_FILE = Path(__file__).parent / "seen_jobs.json"


def load_seen():
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def save_seen(seen):
    SEEN_FILE.write_text(
        json.dumps(sorted(seen), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    first_run = not SEEN_FILE.exists()
    seen = load_seen()

    all_jobs = []
    all_jobs += fetch_infostud()
    all_jobs += fetch_poslovirs()
    all_jobs += fetch_helloworld()
    all_jobs += fetch_linkedin()

    # dedup u okviru ovog pokretanja (isti oglas se može pojaviti dvaput)
    unique = {}
    for job in all_jobs:
        unique[job["id"]] = job
    all_jobs = list(unique.values())

    print(f"Ukupno pronađeno oglasa: {len(all_jobs)}")

    if first_run:
        # Prvi put: samo zapamti trenutno stanje, ne šalji sve odjednom
        print("Prvo pokretanje — čuvam trenutne oglase kao poznate, bez notifikacija.")
        seen = {job["id"] for job in all_jobs}
        save_seen(seen)
        return

    new_jobs = [j for j in all_jobs if j["id"] not in seen]
    print(f"Novih oglasa: {len(new_jobs)}")

    for job in new_jobs:
        msg = f"🆕 <b>{job['title']}</b>\n📍 {job['source']}\n{job['url']}"
        send_telegram(msg)
        seen.add(job["id"])

    save_seen(seen)


if __name__ == "__main__":
    main()
