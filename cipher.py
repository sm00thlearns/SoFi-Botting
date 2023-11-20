from datetime import datetime, timedelta, timezone
import requests
from requests.auth import HTTPProxyAuth
import json
import time
import colorama
import tweepy
from colorama import Fore, Back, Style



#setts
colorama.init()
yollanan_kisiler = set()
webhook_url = ""



def searchxd(aminacoin314169):
	url = "https://cipher.fan/api/search/user-search"
	ahmet31payload = {
		"query" : f"{aminacoin314169}"
	}
	response = requests.post(url,json=ahmet31payload)
	ahmet = response.json()
	return ahmet


for i in range(100, 1001):
	payload = f"{i:03}"

	result = searchxd(payload)

	# "price" 0 olan kullanıcıları bul
	for item in result:
		if "price" in item and item["price"]["raw"] == "0.00006250":
			username = item["username"]["raw"]
			photo_url = item["photourl"]["raw"]

				# Discord Webhook'a mesaj gönder
			if username not in yollanan_kisiler:
				data = {
					"content": f"[{username}](<https://cipher.fan/buy-sell/{username}>) - {item['price']['raw']} - "
				}
				response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
				yollanan_kisiler.add(username)
				if response.status_code == 204:
					print(f"Webhook gönderildi: {username}")
				else:
					print(f"Webhook gönderme başarısız: {username}")
