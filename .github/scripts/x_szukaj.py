import os, requests
from requests_oauthlib import OAuth1
auth = OAuth1(*[os.environ[k] for k in ("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")])
me = requests.get("https://api.x.com/2/users/me", auth=auth, timeout=30).json()
print(me)
uid = me["data"]["id"]
r = requests.get(f"https://api.x.com/2/users/{uid}/tweets", auth=auth, timeout=30, params={
    "max_results": 5, "tweet.fields": "created_at,public_metrics,referenced_tweets,entities"})
print(r.status_code)
for t in r.json().get("data", []):
    print("=====", t["created_at"], t["id"], t.get("public_metrics"), t.get("referenced_tweets"))
    print(t["text"])
    print([u.get("expanded_url") for u in t.get("entities", {}).get("urls", [])])
