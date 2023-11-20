from datetime import datetime, timedelta, timezone
import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import pytz


yollanan_kisiler = set()


authorization_tokens = [
"AUTH TOKEN"
]


turkey_timezone = pytz.timezone('Europe/Istanbul')



while True:
    try:
        url = "https://api.starsarena.com/trade/recent"
        for token in authorization_tokens:
            headers = {
                'authority' : 'api.starsarena.com',
                'accept' : 'application/json',
                'accept-language' : 'en-US,en;q=0.8',
                'authorization' : token,
                'if-none-match' : 'W/"268f-xsTfuBvUBTxGZJTPwIUYOOK4P6c"',
                'origin' : 'https://starsarena.com',
                'sec-ch-ua' : '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile' : '?0',
                'sec-ch-ua-platform' : '"Windows"',
                'sec-fetch-dest' : 'empty',
                'sec-fetch-mode' : 'cors',
                'sec-fetch-site' : 'same-site',
                'sec-gpc' : '1',
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            }

        response = requests.get(url, headers=headers,)

        if response.status_code == 200:
            data = response.json()


            now = datetime.now(timezone.utc)
            five_minutes_ago = now - timedelta(minutes=30)


            for trade in data['trades']:
                avax_price = int(trade['buyPrice']) / 10**18
                floorprice = 0.2
                subject_user = trade['subjectUser']
                trader_user = trade['traderUser']
                twitter_link = f"https://www.starsarena.com/{subject_user['twitterHandle']}"
                created_on_iso = subject_user['createdOn'].split(".")[0]  # Milisaniyeleri kaldırın
                created_on = datetime.fromisoformat(created_on_iso).replace(tzinfo=timezone.utc)
                created_on_tr = created_on.astimezone(tz=turkey_timezone)


                if subject_user['twitterFollowers'] > 100000:
                    embed_color = 0xFF0000  # Kırmızı
                elif subject_user['twitterFollowers'] > 50000:
                    embed_color = 0xFFA500  # Turuncu
                else:
                    embed_color = 0x3498db  # Mavi (Varsayılan)

                if (subject_user['twitterFollowers'] > 5000 and subject_user['id'] not in yollanan_kisiler
                    and created_on >= five_minutes_ago and avax_price <= floorprice):

                    webhook = DiscordWebhook(url="DISCORD_WEBHOOK")
                    embed = DiscordEmbed(title=f"{subject_user['twitterHandle']}", description=f"Twitter Followers: {subject_user['twitterFollowers']}\nGüncel Fiyat: {avax_price} AVAX\n\n\n<https://www.starsarena.com/{subject_user['twitterHandle']}>\n\n\n<https://www.twitter.com/{subject_user['twitterHandle']}>", color=embed_color)
                    embed.set_image(url=f"XXXXXXXXXXXXXXXXXXXX")
                    embed.set_thumbnail(url=f"{subject_user['twitterPicture']}")
                    embed.set_footer(text=f"Oluşturulma Tarihi: {created_on_tr.strftime('%Y-%m-%d %H:%M:%S')} Europe/Istanbul\n", icon_url=f"https://starsarena.com/{subject_user['twitterHandle']}")
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    primt(response)

                    if response.status_code == 204:
                        print(f"{subject_user['twitterHandle']} için Webhook başarıyla gönderildi")
                    else:
                        print(f"{subject_user['twitterHandle']} için Discord webhook gönderilemedi")

                    yollanan_kisiler.add(subject_user['id'])
        else:
            print("API'den veri alınamadı")

    except Exception as e:
        print("Bir hata oluştu:", e)

    time.sleep(0.5)