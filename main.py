import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

SEARCH_URL = "https://www.vinted.de/api/v2/catalog/items"
TOKEN_URL = "https://www.vinted.de/oauth/token"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEARCH_PARAMS = {
    "search_text": "nintendo 3ds",
    "catalog_ids": [49],
    "price_to": 4,
    "currency": "EUR",
    "order": "newest_first",
    "country_ids": [16, 14, 1],
    "status_ids": [0],
    "is_for_sale": True
}

def refresh_access_token():
    global ACCESS_TOKEN
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        print("Token erfolgreich erneuert.")
    else:
        print("Fehler beim Erneuern des Tokens:", response.status_code)

def search_items():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(SEARCH_URL, headers=headers, params=SEARCH_PARAMS)
    if response.status_code == 401:
        refresh_access_token()
        return []
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        return items
    else:
        print("Fehler beim Abrufen:", response.status_code)
        return []

def main():
    while True:
        items = search_items()
        if items:
            print(f"Gefundene Artikel: {len(items)}")
            first_item = items[0]
            print("Artikel gefunden:", first_item["title"])
        else:
            print("Keine passenden Artikel gefunden.")
        time.sleep(60)

if __name__ == "__main__":
    main()
