import requests
# Replace the URL below
API_BASE_URL = 'https://api.cryptowat.ch/'
API_KEY = 'replace_me'

headers = {
    "Accept": "application/json",
    "X-CW-API-Key": API_KEY,
}

cw_api = requests.Session()
