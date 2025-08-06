import requests
import time

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADXI3QEAAAAA93DB84IMwPjbuKhy0zbHAlWfURc%3DB5rDolwX78m9NLqSiKJUEaTVqB19YIpBmQI2yNup4VjjA9gvl0"
WEBHOOK_URL = "https://discord.com/api/webhooks/1401565637607948400/i1nGLSdR8BVm08TOkYx1YymCOvFNeRYpSYdRKYGO6U_qzb_w1iLBiqqWyZt9EpAQItBR"
TWITTER_USERNAMES = [
    "elonmusk", "ABC", "cb_doge", "nypost", "unusual_whales", "solana",
    "Deltaone", "MarioNawfal", "NBCNews", "Bitcoin", "BTCTN",
    "AP", "DonaldTrump", "realDonaldTrump", "TrumpMobile", "DonaldTrumpJr"
]

HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}
LAST_TWEET_IDS = {}

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/%7Busername%7D"
    resp = requests.get(url, headers=HEADERS)
    return resp.json()["data"]["id"]

def get_last_tweet(user_id):
    url = f"https://api.twitter.com/2/users/%7Buser_id%7D/tweets?max_results=5&tweet.fields=created_at"
    resp = requests.get(url, headers=HEADERS)
    tweets = resp.json().get("data", [])
    return tweets[0] if tweets else None

def send_to_discord(tweet, username):
    tweet_url = f"https://twitter.com/%7Busername%7D/status/%7Btweet['id']%7D"
    data = {"content": f" Nouveau tweet de @{username} :\n{tweet_url}"}
    requests.post(WEBHOOK_URL, json=data)

def main():
    user_ids = {u: get_user_id(u) for u in TWITTER_USERNAMES}
    while True:
        for uname, uid in user_ids.items():
            tweet = get_last_tweet(uid)
            if tweet and tweet["id"] != LAST_TWEET_IDS.get(uname):
                send_to_discord(tweet, uname)
                LAST_TWEET_IDS[uname] = tweet["id"]
        time.sleep(30)

if name == "main":
    main()
