from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Exchange Rates API")

# Allow requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_taptap_rates():
    url = "https://api.taptapsend.com/api/fxRates"
    headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,it;q=0.8",
    "appian-version": "web/2022-05-03.0",
    "origin": "https://www.taptapsend.com",
    "referer": "https://www.taptapsend.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Safari/537.36",
    "x-device-id": "web",
    "x-device-model": "web"
}

    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    return res.json()

@app.get("/rate")
def get_rate(sender: str, receiver: str):
    try:
        data = get_taptap_rates().get("availableCountries", [])
        for sender_country in data:
            if sender_country.get("isoCountryCode") == sender.upper():
                for corridor in sender_country.get("corridors", []):
                    if corridor.get("isoCountryCode") == receiver.upper():
                        return {"rate": corridor.get("fxRate")}
        return {"error": "Rate not found"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
