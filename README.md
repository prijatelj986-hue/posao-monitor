# posao-monitor

Свакодневно прати нове огласе за посао на **Infostud**, **Poslovi.rs**,
**HelloWorld.rs** и **LinkedIn**-у по кључним речима: `kalkulant`,
`normiranje`, `tender`, `tehnička priprema`. Нови огласи стижу као
Telegram порука. Ради на истом принципу као `stan-monitor` (GitHub
Actions + Telegram, потпуно бесплатно).

## Шта прати

| Извор | Начин претраге |
|---|---|
| Infostud | директне keyword странице (`/oglasi-za-posao-kalkulant` итд.) |
| Poslovi.rs | категорије: Машинство, Грађевина и геодезија, Економија и менаџмент, Техничке услуге — филтрирано по кључним речима из наслова |
| HelloWorld.rs | општа листа огласа, филтрирано по кључним речима (сајт је претежно IT, па очекуј мање погодака) |
| LinkedIn | јавна ("guest") претрага послова, локација Србија, последња 48h |

Ако желиш да додаш/промениш кључне речи или категорије, измени листе на
врху фајлова `utils.py` (кључне речи), `scraper_infostud.py` (`SLUGS`),
`scraper_poslovirs.py` (`CATEGORIES`) и `scraper_linkedin.py`
(`SEARCH_TERMS`).

## Подешавање (isto kao stan-monitor)

1. **Направи нови GitHub repo** (нпр. `posao-monitor`) и отпакуј ове
   фајлове у њега (или push-uj их директно).

2. **Додај Telegram Secrets** — Settings → Secrets and variables →
   Actions → New repository secret:
   - `TELEGRAM_BOT_TOKEN` — исти бот токен који већ користиш за
     `stan-monitor` (или направи нови преко @BotFather)
   - `TELEGRAM_CHAT_ID` — исти chat ID као код `stan-monitor`, ако
     желиш нотификације на исто место

3. **Укључи Actions** (ако нису аутоматски укључене) и покрени first-run
   ручно: Actions таб → "Dnevna pretraga poslova" → Run workflow.
   Прво покретање само памти тренутне огласе (`seen_jobs.json`) без
   слања порука — да не добијеш 50 нотификација одједном.

4. Од другог покретања надаље, свако ново поклапање ће стићи као
   Telegram порука. Radni raspored (cron) je podešen na 06:00 UTC
   (~08:00 po srednjeevropskom letnjem vremenu) — po potrebi promeni
   `cron` u `.github/workflows/scan.yml`.

## Локално тестирање

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=xxx
export TELEGRAM_CHAT_ID=yyy
python main.py
```

Или тестирај појединачни извор, нпр.:

```bash
python scraper_infostud.py
python scraper_poslovirs.py
python scraper_linkedin.py
```

## Напомене / могући проблеми

- **LinkedIn** је најосетљивији извор — с времена на време мења HTML
  структуру или ограничава guest приступ. Ако престане да враћа
  резултате, прво провери да ли `scraper_linkedin.py` и даље враћа
  нешто локално (`python scraper_linkedin.py`); можда ће требати
  прилагодити селекторе.
- **Poslovi.rs** нема једноставну GET претрагу (форма је JS-driven),
  па се уместо ње прате категорије и филтрира наслов — ово значи да
  ће понекад проћи и понеки не сасвим релевантан оглас; лако се
  дотерује у `utils.py` (`KEYWORDS`).
- Ако неки сајт промени HTML, scraper за тај сајт ће вратити 0
  резултата (won't crash the whole run) — остали извори настављају
  нормално.
