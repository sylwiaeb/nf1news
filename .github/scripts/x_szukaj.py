import os, requests
from requests_oauthlib import OAuth1
auth = OAuth1(*[os.environ[k] for k in ("X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET")])
q = '(neurofibromatoza OR neurofibromatozy OR neurofibromatozą OR neurofibromatozami OR #NF1 OR nf1news OR "nf1news.pl" OR @nf1news OR rasopatie OR rasopatiami) -is:retweet'
r = requests.get("https://api.x.com/2/tweets/search/recent", auth=auth, timeout=30, params={
    "query": q, "start_time": "2026-11-01T23:00:00Z", "max_results": 100,
    "tweet.fields": "created_at,public_metrics,lang,author_id",
    "expansions": "author_id", "user.fields": "username,name"})
print(r.status_code)
d = r.json()
users = {u["id"]: u for u in d.get("includes", {}).get("users", [])}
for t in d.get("data", []):
    u = users.get(t["author_id"], {})
    print("=====", t["created_at"], "@" + u.get("username", "?"), u.get("name", ""), t.get("lang"), t.get("public_metrics"))
    print("https://x.com/i/status/" + t["id"])
    print(t["text"])
if "data" not in d:
    print(d)
