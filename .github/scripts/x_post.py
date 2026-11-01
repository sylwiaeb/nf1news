"""Publikuje nowe wpisy bloga na X.

Tekst bierze z pola `tweet:` w nagłówku wpisu (pisze go Claude przy
przygotowaniu wpisu). Bez tego pola używa samego tytułu. Link do wpisu
jest dodawany automatycznie na końcu. Przed wysłaniem czeka, aż wpis
będzie widoczny na stronie.
"""
import os
import re
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import yaml
from requests_oauthlib import OAuth1

SITE = "https://nf1news.pl"
TZ = ZoneInfo("Europe/Warsaw")


def read_post(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    meta = yaml.safe_load(m.group(1)) if m else {}
    return meta or {}


def post_url(path, meta):
    name = os.path.basename(path)[:-3]
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)", name)
    y, mo, d, slug = m.groups()
    date = meta.get("date")
    if isinstance(date, datetime):
        local = date.astimezone(TZ) if date.tzinfo else date
        y, mo, d = f"{local.year:04d}", f"{local.month:02d}", f"{local.day:02d}"
    return f"{SITE}/{y}/{mo}/{d}/{slug}/"


def wait_until_live(url, minutes=15):
    for _ in range(minutes * 4):
        try:
            if requests.get(url, timeout=10).status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(15)
    return False


def main():
    paths = [p.strip() for p in open(sys.argv[1]) if p.strip()]
    if not paths:
        print("Brak nowych wpisów.")
        return
    keys = [os.environ.get(k) for k in
            ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")]
    if not all(keys):
        print("Brak kluczy X w sekretach repozytorium, pomijam.")
        return
    auth = OAuth1(*keys)
    failed = False
    for path in paths:
        meta = read_post(path)
        if meta.get("tweet") is False:
            print(f"{path}: tweet: false, pomijam.")
            continue
        url = post_url(path, meta)
        text = str(meta.get("tweet") or meta.get("title", "")).strip()
        text = f"{text}\n\n{url}"
        if not wait_until_live(url):
            print(f"{path}: wpis nie pojawił się pod {url}, pomijam.")
            failed = True
            continue
        r = requests.post("https://api.x.com/2/tweets", json={"text": text}, auth=auth, timeout=30)
        print(f"{path}: {r.status_code} {r.text}")
        if r.status_code >= 300:
            failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
