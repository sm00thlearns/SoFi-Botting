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

#defs
def twitterFollowerCheck(twitterHandle):
	user = api.get_user(screen_name=twitterHandle)
	follower_count = user.followers_count
	return follower_count

def activityRes():
	url = "https://social.kepler.homes/api/social/trade/logs/global"
	headers = {
		'Sec-Ch-Ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
		"Accept": "application/json, text/plain, */*",
		"Ksa": "",
		"Sec-Ch-Ua-Mobile": "?0",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
		"Sec-Ch-Ua-Platform": "Windows",
		"Sec-Fetch-Site": "same-origin",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Dest": "empty",
		"Referer": "https://social.kepler.homes/",
		"Accept-Language": "en-US,en;q=0.9"
	}
	cookies= {	}
	
	try:
		response = requests.get(url, headers=headers, cookies=cookies)
		if response.status_code == 200:
			try:
				data = response.json()
				return data
			except json.JSONDecodeError as e:
				print(f"JSON decoding error: {e}")
	except requests.exceptions.RequestException as e:
		print(f"Request error: {e}")
	
	return None

# Setts
yollanan_kisiler = set()
floorprice = 5

while True:
	gotdelen = activityRes()
	
	if gotdelen is not None and 'data' in gotdelen:
		data_list = gotdelen['data']
		if data_list:
			firstradedata = data_list[0]['trade_time']

		for data in data_list:
			fiyat = int(data['price']) / 10**18  # 'price' verisini float değere dönüştürün.
			if data['subject_address'] not in yollanan_kisiler:
				if fiyat < floorprice and firstradedata - data['trade_time'] < 30 and data['action'] == 1:
					sub_follows = twitterFollowerCheck(data['subject_twitter_username'])

					if sub_follows > 100000:
						color = "FF0000"  # Kırmızı
					elif sub_follows > 50000:
						color = "FFA500"  # Turuncu
					else:
						color = "3498db"  # Mavi (Varsayılan)

					if sub_follows > 1000:
						yollanan_kisiler.add(data['subject_address'])

						embed = DiscordEmbed(title=f"[{data['subject_twitter_username']}](<https://social.kepler.homes/room/{data['subject_address']}>)",description=f"Twitter Follower: {sub_follows}\nPrice: {fiyat} ARB", color=f"{color}")

						embed.set_image(url=data['subject_twitter_pfp_url'])  # 'subject_twitter_pfp_url' kullanın

						message = DiscordWebhook(url=discord_webhook_url)
						message.add_embed(embed)

						response = message.execute()
						if response.status_code == 204:
							print(f"Webhook gönderildi: {data['subject_twitter_username']}")
						else:
							print(f"Webhook gönderme başarısız: {data['subject_twitter_username']}")
					else:
						yollanan_kisiler.add(data['subject_address'])
				else:
					yollanan_kisiler.add(data['subject_address'])
