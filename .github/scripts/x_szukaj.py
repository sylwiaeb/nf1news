import os, requests
from requests_oauthlib import OAuth1
auth = OAuth1(*[os.environ[k] for k in ("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")])
text = open(".github/scripts/post.txt", encoding="utf-8").read().strip()
quote = "2117172113291260219"
r = requests.post("https://api.x.com/2/tweets", auth=auth, timeout=30, json={"text": text, "quote_tweet_id": quote})
print("quote:", r.status_code, r.text)
if r.status_code >= 300:
    r = requests.post("https://api.x.com/2/tweets", auth=auth, timeout=30,
                      json={"text": text + "\nhttps://x.com/NewsMED_pl/status/" + quote})
    print("fallback:", r.status_code, r.text)
