import requests
import time

ACCESS_TOKEN = "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwic3ViIjoiMTA3NzkxMzA4IiwiaWF0IjoxNzQ1ODQxNzcyLCJzaWQiOiI5ZjE4YTVlOS0xNzQ1Njk3NjE0Iiwic2NvcGUiOiJ1c2VyIiwiZXhwIjoxNzQ1ODQ4OTcyLCJwdXJwb3NlIjoiYWNjZXNzIiwiYWN0Ijp7InN1YiI6IjEwNzc5MTMwOCJ9LCJhY2NvdW50X2lkIjo3Njc2NDg0MX0.ow2S-JrWREsMXDW8izHYbUqiNIUtDr5GimZ4JyOOKYVL0Jb4kBjoESB9j9aKHDDiF5Sl3bLMvgZrEIKKZOTqGhayQ2hENCxuvOyAG8lQ536w1sSW3odCvA5xVKHFbJM5u8_Up4MYWiOKmqxZHfwkPJDkc0Mn8h1fPVKA2ogHZLiHFfK4k5TedIy9YCQBjvG8yRtXIJrK-dCMeF54TNbQSKgUe15_VD0nMD4YWDGiNgvYUzkhGamJRl7evyDZCUAOGp3E3bmKgOQTzi4OkSLgdgg-DYTOZzVQRbb6PVg8rZVptx3euPbDZ0UFQcNgC_L6tLBS-wAWv3dQTj0fJJBgtg"
REFRESH_TOKEN = "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhcHBfaWQiOjQsImNsaWVudF9pZCI6IndlYiIsImF1ZCI6ImZyLmNvcmUuYXBpIiwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwic3ViIjoiMTA3NzkxMzA4IiwiaWF0IjoxNzQ1ODQxNzcyLCJzaWQiOiI5ZjE4YTVlOS0xNzQ1Njk3NjE0Iiwic2NvcGUiOiJ1c2VyIiwiZXhwIjoxNzQ2NDQ2NTcyLCJwdXJwb3NlIjoicmVmcmVzaCIsImFjdCI6eyJzdWIiOiIxMDc3OTEzMDgifSwiYWNjb3VudF9pZCI6NzY3NjQ4NDF9.W4RZqwMuU0Xfv0srwgVlHjji6T9A1fayY6P0xzacis9fy3LJNfkdL7tdOemo_Lcpq7gvM9qNxS1aM05_PGmCH8ylh0W44F_uEfoMn5Mr-cooqGJnFlEYxJXeT5a387WA7xYZr664q75XGq05lN5Vz-yQRDkT1tgE59WWhkxeW1Gi1zPHWcwD9C2to3_VX0H2biG1j2WYbOpOMzrbWFHV01ImVoha7MdKDshTxgcWR_LWXBJyk42CDcI3y92L_6P5TMweKI_2u9ebJVRrOx1hMmqB1KhidU0mcHBj8PA6aXukRWQGAiATZbVkvvikFZC5utcHZLIqgghoERpQK_W2Aw"

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
    response = requests.get(SEARCH_URL, headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }, params=SEARCH_PARAMS)
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
