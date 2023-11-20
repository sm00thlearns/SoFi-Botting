from datetime import datetime, timedelta, timezone
import requests
import json
import tweepy
from discord_webhook import DiscordWebhook
import time

# Twitter API keyleriniz
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Tweepy ile Twitter takipçi çekmek için
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Discord Webhook URL'sini buraya ekleyin
discord_webhook_url = ""

# API'den veri çekme işlevi
def activityRes():
	url = "https://api.hub3.ee/api/share/activity"
	response = requests.get(url)
	ahmet = response.json()
	return ahmet

# Twitter takipçi sayısını kontrol etme işlevi
def twitterFollowerCheck(twitterHandle):
	user = api.get_user(screen_name=twitterHandle)
	follower_count = user.followers_count
	return follower_count

# Daha önce yollanan kullanıcıları izlemek için bir set
yollanan_kisiler = set()
checklenen_kisiler = set()
floorprice = 1
floorfollowers = 10000
tradetype = "Bought"

while True:
	activitydata = activityRes()
	
	# Şu anki tarihi ve 20 dakika önceki tarihi hesapla
	now = datetime.now(timezone.utc)
	twenty_minutes_ago = now - timedelta(minutes=180)
	
	for log in activitydata["logs"]:
		if log["type"] == "Bought" and int(log["value"]) < floorprice:
			created_at = datetime.fromisoformat(log["createdAt"])
			if created_at > twenty_minutes_ago and created_at <= now:
				issuer = log["issuer"]
				user_address = log["user"]
				for user in activitydata["users"]:
					if user["shareAddress"] == issuer:
						username = user["username"]
						if username not in yollanan_kisiler:
							follower_count = twitterFollowerCheck(username)
							if follower_count > 20000:
								yollanan_kisiler.add(username)
								message = f"Bought: {log['value']} - Username: {username} - Follower Count: {follower_count}"
								# Discord webhook'u kullanarak mesajı gönder
								webhook = DiscordWebhook(url=discord_webhook_url, content=message)
								webhook.execute()
						else:
							yollanan_kisiler.discard(username)

	time.sleep(2)