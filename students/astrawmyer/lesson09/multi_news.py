#Your API key is: 0c90527956054643acefdedb6587d07f

import time
import requests

WORD = "musk"

NEWS_API_KEY = "0c90527956054643acefdedb6587d07f"

base_url = 'https://newsapi.org/v1'


def get_sources():
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources