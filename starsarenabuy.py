from datetime import datetime, timedelta, timezone
import requests
from requests.auth import HTTPProxyAuth
import json
import time
import colorama
from colorama import Fore, Back, Style
colorama.init()

yollanan_kisiler = set()

authorization_tokens = [
    "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiMDYxMzYzODAtNjEyZC00YzI5LWE4NGItMTAzNjExOGRkNTgwIiwidHdpdHRlcklkIjoiMTcwOTg0MjcyODM2MjU5ODQwMCIsInR3aXR0ZXJIYW5kbGUiOiJFcmVuS3VydHVsNzAxMTkiLCJ0d2l0dGVyTmFtZSI6IkVyZW4gS3VydHVsdXMiLCJ0d2l0dGVyUGljdHVyZSI6Imh0dHBzOi8vcGJzLnR3aW1nLmNvbS9wcm9maWxlX2ltYWdlcy8xNzA5ODQyNzY0NDM3ODgwODMyLzdoOTMxZmFHX25vcm1hbC5wbmciLCJhZGRyZXNzIjoiMHhlNTA0NDJiYjAzNDQ2YzJjOTE0ODdkM2NlODZhZjVhZTRlNzVhMDBiIn0sImlhdCI6MTY5NjQ5MzMwOCwiZXhwIjoxNzA1MTMzMzA4fQ.PyTQevTP6zLQ0k3j4W7CvCVDGiHJ87OX_x4XF_1x-tFiZUOKu3iPlRJQXeclQIi4JA7XTV-NlAYV9TZOq79aoxuMKvnDTdWn9Ex0CViN0_tlu-dhlFtDAeq59T4hFAvz7j-qFPRresP3vjh8pje1H2nBRygSEVhe81yqpdSvBiTGw4l28BlxYznllU2khp_OIwvIcyAQoPdwsl819jSrMj-olq7rJ51sYKvT5BvRUTWjMpiVyxshmdg5Bs2x1FtGUib5jfRIiy9Cv-fnq_tbpX42JVNXkt7oyWGk80xeMehU8wHu5dzdQIydRhNqLWOaNUIP2F1jfwbaCtoxT_pvi3JUIuj32juryELe323jChjqE6UhnoZCLfxGoEskDkldgqufIyIrE7cjA0MHHi6rxtXxDm7cx1BUgR7ru_fnL_dIdXamVpgQhWmwwnw2wCL_--xC2DBp5_2IJGDqB3j0X4Xcan9NpbXKJhY5hjU8EIyu1QyFn1fOphhsOImShOr_3nC-X6CE11kru2fm0JY4u7KsTxq1jKJmDcH6Kusj4WRw712jCrN8bEJEPjdIOdvJllhu8IkdyVUCUfz7put76Er1cnDMIfqohr9sM284ZSE-sTPYDpN1hqZVU06haCDAGcnr8SUVu4veSSH2KVpdSy4dcj8ew3XOWzJHX7VIkFU",
    "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjVmMjNjZDItYTNhNC00NmUxLTk3NWEtYzI5ZjQzM2JjNzk2IiwidHdpdHRlcklkIjoiMTcwOTg0MjAwNjE0NTQyMTMxMiIsInR3aXR0ZXJIYW5kbGUiOiJrdXJ0dWw0NTczOCIsInR3aXR0ZXJOYW1lIjoiZXJlbiBrdXJ0dWx1cyIsInR3aXR0ZXJQaWN0dXJlIjoiaHR0cHM6Ly9wYnMudHdpbWcuY29tL3Byb2ZpbGVfaW1hZ2VzLzE3MDk4NDIwNDU0MjA5MzcyMTYvRENua2VvZjNfbm9ybWFsLnBuZyIsImFkZHJlc3MiOiIweGM2ZDk0MDI1ZTQyNDZkZGFhNjg0NDUwZjllOGNiZTExZTA5MDY3MDMifSwiaWF0IjoxNjk2NDkzMTYzLCJleHAiOjE3MDUxMzMxNjN9.EAHw6cfzuY_1FxOdehSnieWpUJdHPxBxXTCawWDIQM-YPvhG40i-woy0C-xfMjPF5STyTZz8eKD8SKP-SvV4x_3BQDVc55c5_doXPDUhqFzR94-mEL3Bv7HMoniPeL4ehtYyXsWUb8_LRL_PA3wdZrRSOFBi0dpXhMio6c0uBu0AZXbdzOsnO3aaUQLPzqkDKlmYf2WSOck2SIV0Hs329JZ764EKS1n7ybOerKtxJ9vDkC6IGoU1_WTdVYINVyQSXAL1HVLo_0PtsmQV7aFfBXgrur7sZaiYZJTpoUvfmYot5aLfcrmKqzjo5su9HxAF_ldZBq01laGMLUGL88JByQxDZY681JPor3xiVUqYlklgNk5PyJLslAWzEQmYJJ-7Pb75la-hmZ5ajCThcBIYbOm1ynHEX2czbO2jOlpIx3wwIwDddApyKuATDz2DN9M2l0ZjO3nGWmCwOzOFBki20oM3NljWwiMdq4LBdijw0xj7ULss4aIXuu-kZOJgtosWIPmJcrC3RCMQZ-cuaS9hSI8JirQ-Ddc3A2wwtnjfHzaRaPsRrEv3v2v6863OL3abkz0nlajtM5JhLOEsk9dTpi0g5Kq9wYfIn-Vc0KzFLjfm6UfHsFk1eWz5Phc1zeXhgnngbB2VYXatX5x7Gm63OmJBtRY0FhWpUOi9Skiv6JQ",
    "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiMGRkNjZhYzgtNzM0Ny00ODlhLWI1NzYtM2YyMzUzZWMxNzNhIiwidHdpdHRlcklkIjoiMTQ0MzMzODUwMiIsInR3aXR0ZXJIYW5kbGUiOiJlcmVuZ25lbiIsInR3aXR0ZXJOYW1lIjoiRXl1cCBFcmVuIiwidHdpdHRlclBpY3R1cmUiOiJodHRwczovL3Bicy50d2ltZy5jb20vcHJvZmlsZV9pbWFnZXMvMTcwNDU0NDQwNjM3ODc3ODYyNS8yWVNsUEZFMl9ub3JtYWwuanBnIiwiYWRkcmVzcyI6IjB4Y2FhODcxNDQ5ZDAzM2JlY2M0NDcxNDg4NjIwZDQxNDE1YjY1YzU5NSJ9LCJpYXQiOjE2OTYzNDAwNzQsImV4cCI6MTcwNDk4MDA3NH0.WZm1KXgcayQwJqnb-KG5hEpPLlVgULB5Grm9YGQbHAT1V9RsRZFfTWAiktrMW5aAbsd_QyR5tk1Oo4cHYMj1ob4tOQJ9tEii4if0Mo82EHJi9YjhS50Js08YEUZfYQolR7WCUkhgr3-I3jXhzCX0oV0jHsiuMDsTw9Vv76Ef9sqSvgcY7XdBVEGtOvFmOhnQ6Q41QZoGHlG0uDqHra4AZFuPj5dyAMP1dEXXTh3l-dpm5SQ9FLQ6tpY5FiMPO4dXwzduEYWtQ-KiB1CvBgS60VQo2qjMeKrmQCuGoDp-cRDa8i6QW39uDiaYPFJRw1jwjuOgLvR--VoC-lT-SOQ79N2SVxDft-fnLF69PdxEDSWFGIKSpkY9KnEIGHrcjjcVVJ2_zWQWkkyHZ6dmrk3TCYBow2WPWXlqzqdCKpLFb3zi96Tyh_0NJTFKGyLnCmbUZ3DV2j3PoVA9ghN_fMALN5juT1PdhrPq7FYrV3P5HWCnULkl9ZI4AkGQThZmgM830YVLCx1c23eSkiZJUGniSnE4LI9P8uEs3W_FS-bVZZI-6YHT0SqLeF9RU8DpuP8gigRTm0RQTNwMg0NWnuIiBdNjWRzYOLGgqfJpdWQ-InVti1iJ1nnxZ_i47U3D7_BuPam2IDSj0RXpytIlpzcT2PTr5flXpJvJJ3BdGfViRWg",
    # Daha fazla token ekleyin
]

a = 1
b = 1
while True:
    try:
        url = "https://api.starsarena.com/trade/recent"
        proxies = {
            "http" : "https://proxy.snowproxies.digital:8000"
        }
        for token in authorization_tokens:
            headers = {
                "Host": "api.starsarena.com",
                "Authorization": token,
            }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            now = datetime.now(timezone.utc)
            five_minutes_ago = now - timedelta(minutes=15)


            for trade in data['trades']:
                avax_price = int(trade['buyPrice']) / 10**18
                floorprice = 0.7
                subject_user = trade['subjectUser']
                trader_user = trade['traderUser']
                twitter_link = f"https://www.starsarena.com/{subject_user['twitterHandle']}"
                created_on_iso = subject_user['createdOn'].split(".")[0]  # Milisaniyeleri kaldırın
                created_on = datetime.fromisoformat(created_on_iso).replace(tzinfo=timezone.utc)

                if (subject_user['twitterFollowers'] > 100000 and subject_user['id'] not in yollanan_kisiler
                    and created_on >= five_minutes_ago and avax_price <= floorprice):
                    b = b + 1
                    print(Back.GREEN + f"{b} {subject_user['twitterHandle']} filtrelendi")

                    url_price = f"https://api.starsarena.com/trade/price?address={subject_user['address']}"
                    ahmet = requests.get(url_price,headers={"Host": "api.starsarena.com","Authorization": token,})
                    print(f"{subject_user['twitterHandle']} fiyat alındı {ahmet.json()}")
                    if ahmet.status_code == 200:
                        datapcheck = ahmet.json()
                        buy_amount = int(datapcheck['buyPrice']) / 10**18
                        while buy_amount < floorprice:
                            print(f"{buy_amount}")

                            buy_payload = {
                                "address": subject_user['address'],
                                "amount": datapcheck['buyPrice'],
                            }

                            buy_response = requests.post("https://api.starsarena.com/trade/buy", json=buy_payload, headers={"Host": "api.starsarena.com","Authorization": "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiZTU4ZWMyNTItYTY5NS00MDIzLWFiODktNjhjNWVlM2E3OWNlIiwidHdpdHRlcklkIjoiMTY5OTMzNzc5NDMyODM0MjUyOSIsInR3aXR0ZXJIYW5kbGUiOiIweE1hbXV0aCIsInR3aXR0ZXJOYW1lIjoiTUFNVVQuRVRIIiwidHdpdHRlclBpY3R1cmUiOiJodHRwczovL3Bicy50d2ltZy5jb20vcHJvZmlsZV9pbWFnZXMvMTcwNDI0NzcwNDI0NTY0NTMxMy9LM19XZjFUUF9ub3JtYWwuanBnIiwiYWRkcmVzcyI6IjB4OWZjOWRhNGU0YzMxNjViMTc4ZGExZDU3MjYyOWQwMWRmNmZlNDkwMiJ9LCJpYXQiOjE2OTY2MTEwOTEsImV4cCI6MTcwNTI1MTA5MX0.P6i2moi0_t4WazMD0jZBkrA4SvRtZubQE23h22S2ZzzOx_kSPOIPPS0-GjUQfZx6b4-i5fbP5jCbeldqPxOIUDk00_gwiiU-2TzBRtJc2Njq6QFNHztQ5WnGbh4uTJS7Mt702SBx0vubwIs_Ep7v32JjQCvXDEyRnbr3WyDjCbKRghQMa7TFsGbJOeV6BX7gA4_UWp2NBu2NTOkqYzJzOPKhIIbGsXP6gTShXQGYNkmI9xrx3guBjpF-HuI_YWOYdrcxkR7d64JTdq5ik2Bgsi8FVBlImualH4gOJfLal9WYISpj6GZj4LZ5CxhopgDwUMx5na1jpvIgESAZxga2KSl8k4l2S4vcCHoa2bCXFQjGoiaK-z4A5WsgCBwKrwH437wSsqKuzqCC_69sIwSoijBKvAKnmQNDF0ENOpTdqXtrPRQlouDfhiF7D3TluyANKbDlbyZ_BonxLSR75eou71eL9vt_XE2A8nS8QhMRAm5irZMIUbT7rxxCCIrL3Nur6t29NAfduNI_n9__CDRYKJmSWW6y6gZ9MffL5ow7AhLOXdxGS8flmXqBKiG1F0OV4LA6RF8LI3QYgQZ3h0tB0xU00_2fhplg1gBS9LIH5k3uc3ugC6yngfDMuGgXJRWkX8ykndzPzYlkbjzRpj2y21ZH-_u-o16dAnBSPvEtVvg"})

                            if buy_response.status_code == 201:
                                print(Back.GREEN + f"{subject_user['twitterHandle']} başarıyla {buy_amount} fiyatından satın alındı.")
                                yollanan_kisiler.add(subject_user['id'])
                                break

                            else:
                                time.sleep(0.3)
                                ahmet1 = requests.get(url_price,headers={"Host": "api.starsarena.com","Authorization": token,})
                                jahmet1 = ahmet1.json()
                                buy_amount = int(jahmet1['buyPrice']) / 10**18
                                datapcheck['buyPrice'] = jahmet1['buyPrice'] 
                    else:
                        print(Back.RED + f"{subject_user['twitterHandle']} için güncel fiyat bilgisi alınamadı")
                        yollanan_kisiler.add(subject_user['id'])

                else:
                    C = 31
        else:
            print("API'den veri alınamadı")


    except Exception as e:
        print("Bir hata oluştu:", e)
