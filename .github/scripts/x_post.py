"""Publikuje nowe wpisy bloga na X.

Tekst bierze z pola `tweet:` w nagłówku wpisu (pisze go Claude przy
przygotowaniu wpisu). Bez tego pola używa samego tytułu. Link do wpisu
trafia automatycznie do pierwszego komentarza pod postem (przy
`link_w_komentarzu: false` jest dopisywany na końcu posta). Przed wysłaniem czeka, aż wpis
będzie widoczny na stronie.

Do posta dołącza grafikę wpisu: `grafika_x:` z nagłówka, a bez niej
kwadratową wersję obrazka z `image:` (plik `…-kwadrat.png` obok), a gdy jej
nie ma, sam obrazek z `image:`. Opis grafiki dla niewidomych bierze z
`grafika_alt:` (albo z tytułu). `grafika_x: false` wysyła post bez grafiki.
Jeśli wysłanie grafiki się nie uda, post idzie bez niej.
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


def find_image(meta):
    if meta.get("grafika_x") is False:
        return None
    candidates = []
    if meta.get("grafika_x"):
        candidates.append(str(meta["grafika_x"]))
    image = meta.get("image")
    if image:
        root, ext = os.path.splitext(str(image))
        candidates += [f"{root}-kwadrat{ext}", str(image)]
    for c in candidates:
        path = c.lstrip("/")
        if os.path.isfile(path):
            return path
    return None


def upload_image(path, alt, auth):
    """Wysyła obrazek do X i zwraca jego media_id (albo None)."""
    try:
        with open(path, "rb") as f:
            r = requests.post("https://api.x.com/2/media/upload", auth=auth, timeout=60,
                              files={"media": (os.path.basename(path), f, "image/png")},
                              data={"media_category": "tweet_image"})
        print(f"grafika {path}: {r.status_code} {r.text[:300]}")
        if r.status_code >= 300:
            return None
        body = r.json()
        media_id = (body.get("data") or {}).get("id") or body.get("media_id_string")
        if media_id and alt:
            m = requests.post("https://api.x.com/2/media/metadata", auth=auth, timeout=30, json={
                "id": media_id, "metadata": {"alt_text": {"text": alt[:1000]}}})
            print(f"opis grafiki: {m.status_code} {m.text[:200]}")
        return media_id
    except (requests.RequestException, ValueError, OSError) as e:
        print(f"grafika {path}: błąd {e}")
        return None


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
        link_in_reply = meta.get("link_w_komentarzu") is not False
        if not link_in_reply:
            text = f"{text}\n\n{url}"
        if not wait_until_live(url):
            print(f"{path}: wpis nie pojawił się pod {url}, pomijam.")
            failed = True
            continue
        payload = {"text": text}
        image = find_image(meta)
        if image:
            alt = str(meta.get("grafika_alt") or meta.get("title", "")).strip()
            media_id = upload_image(image, alt, auth)
            if media_id:
                payload["media"] = {"media_ids": [str(media_id)]}
        r = requests.post("https://api.x.com/2/tweets", json=payload, auth=auth, timeout=30)
        print(f"{path}: {r.status_code} {r.text}")
        if r.status_code >= 300:
            failed = True
            continue
        if link_in_reply:
            tweet_id = r.json()["data"]["id"]
            r = requests.post("https://api.x.com/2/tweets", auth=auth, timeout=30, json={
                "text": url, "reply": {"in_reply_to_tweet_id": tweet_id}})
            print(f"{path} (link w komentarzu): {r.status_code} {r.text}")
            if r.status_code >= 300:
                failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
