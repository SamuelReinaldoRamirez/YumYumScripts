import requests

def post_to_api():
    url = "https://api.ttsave.app/"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://ttsave.app",
        "Referer": "https://ttsave.app/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    }

    payload = {
        "id": "https://www.tiktok.com/@nafyknz/video/7363622871438036256?is_from_webapp=1&sender_device=pc",
        "hash": "1737761289a9dcb3e34002a38c45b469",
        "mode": "thumbnail",
        "locale": "en",
        "loading_indicator_url": "https://ttsave.app/images/slow-down.gif",
        "unlock_url": "https://ttsave.app/en/unlock"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Request successful!")
        print("Response:")
        print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")

def main():
    post_to_api()

if __name__ == "__main__":
    main()
