#!/usr/bin/env python3
"""Construit le site à partir de src/page.html.

1. Calcule les plages libres de chaque professeur à partir de ses événements
   (data/events-<id>.json, NON publiés : ils restent hors du dépôt).
2. Injecte ces plages dans la page (seules les plages libres sont publiées).
3. Écrit index.html (version en ligne, avec en-tête Google) et
   preview.html (aperçu claude.ai, sans doctype).

Usage : python3 scripts/build.py [--now 2026-10-02T09:00]
"""
import json, sys, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://coursparticulierslille.github.io/Cours-Lille/"

# ---- Règles de disponibilité (communes aux professeurs) ----
RULES = {
    # jour de semaine (0 = lundi) -> (début, fin)
    "plages": {0: ("14:00", "20:00"), 1: ("14:00", "20:00"), 2: ("14:00", "20:00"),
               3: ("14:00", "20:00"), 4: ("14:00", "20:00"), 5: ("10:00", "20:00")},
    "marge_min": 40,          # temps de trajet avant et après chaque événement
    "duree_min": 90,          # une plage doit pouvoir contenir au moins 1 h 30
    "delai_min_h": 24,        # pas de réservation à moins de 24 h
    "horizon_jours": 28,      # créneaux affichés sur 4 semaines
}
PROFS = ["noe", "marie"]


def parse(s):
    return dt.datetime.fromisoformat(s)


def hm(d, s):
    h, m = map(int, s.split(":"))
    return dt.datetime.combine(d, dt.time(h, m))


def free_windows(events, now):
    marge = dt.timedelta(minutes=RULES["marge_min"])
    busy = sorted((parse(a) - marge, parse(b) + marge) for a, b, *_ in events)
    earliest = now + dt.timedelta(hours=RULES["delai_min_h"])
    out = []
    for i in range(RULES["horizon_jours"] + 2):
        day = (now + dt.timedelta(days=i)).date()
        if day.weekday() not in RULES["plages"]:
            continue
        a, b = RULES["plages"][day.weekday()]
        segs = [(max(hm(day, a), earliest), hm(day, b))]
        for bs, be in busy:
            nxt = []
            for s, e in segs:
                if be <= s or bs >= e:
                    nxt.append((s, e)); continue
                if bs > s: nxt.append((s, bs))
                if be < e: nxt.append((be, e))
            segs = nxt
        for s, e in segs:
            if (e - s).total_seconds() / 60 >= RULES["duree_min"]:
                out.append([day.isoformat(), s.strftime("%H:%M"), e.strftime("%H:%M")])
    return out


def main():
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=2))).replace(tzinfo=None)
    if "--now" in sys.argv:
        now = parse(sys.argv[sys.argv.index("--now") + 1])
    data = {"maj": now.strftime("%Y-%m-%dT%H:%M"), "profs": {}}
    for p in PROFS:
        f = ROOT / "data" / f"events-{p}.json"
        data["profs"][p] = free_windows(json.loads(f.read_text())["events"], now) if f.exists() else None

    page = (ROOT / "src" / "page.html").read_text()
    marker = "/*SLOTS*/null"
    assert marker in page, "marqueur /*SLOTS*/null introuvable dans src/page.html"
    page = page.replace(marker, json.dumps(data, ensure_ascii=False))

    (ROOT / "preview.html").write_text(page)

    head_end = page.index("</style>") + len("</style>")
    head, body = page[:head_end], page[head_end:]
    head = head.replace("<title>Encre Bleue</title>",
        "<title>Cours particuliers à domicile à Lille · Maths, Français, Anglais, HGGSP, SES</title>")
    seo = (ROOT / "src" / "seo-head.html").read_text()
    html = ("<!doctype html>\n<html lang=\"fr\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            + head + "\n" + seo + "</head>\n<body>" + body + "\n</body>\n</html>\n")
    (ROOT / "index.html").write_text(html)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{URL}</loc><lastmod>{now.date().isoformat()}</lastmod></url>\n</urlset>\n')
    for p, w in data["profs"].items():
        print(p, "aucun agenda" if w is None else f"{len(w)} plages libres")


if __name__ == "__main__":
    main()
