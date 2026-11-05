"""Ręczne działania na X: odpowiedź pod postem, usunięcie posta albo nowy post.

Uruchamiane z zakładki Actions (workflow_dispatch). Dane wejściowe
przychodzą w zmiennych środowiskowych AKCJA, TWEET_ID i TEKST.
"""
import os
import sys

import requests
from requests_oauthlib import OAuth1

API = "https://api.x.com/2/tweets"


def main():
    auth = OAuth1(*[os.environ[k] for k in
                    ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET")])
    akcja = os.environ.get("AKCJA", "").strip()
    tweet_id = os.environ.get("TWEET_ID", "").strip()
    tekst = os.environ.get("TEKST", "").strip().replace("\\n", "\n")
    if akcja == "odpowiedz" and tweet_id and tekst:
        r = requests.post(API, json={"text": tekst, "reply": {"in_reply_to_tweet_id": tweet_id}},
                          auth=auth, timeout=30)
    elif akcja == "usun" and tweet_id:
        r = requests.delete(f"{API}/{tweet_id}", auth=auth, timeout=30)
    elif akcja == "post" and tekst:
        r = requests.post(API, json={"text": tekst}, auth=auth, timeout=30)
    else:
        print("Brak wymaganych danych dla tej akcji.")
        sys.exit(1)
    print(f"{akcja}: {r.status_code} {r.text}")
    sys.exit(0 if r.status_code < 300 else 1)


if __name__ == "__main__":
    main()
