#Your API key is: 0c90527956054643acefdedb6587d07f

import time
import requests

WORD = "boeing"

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

def get_articles(source):
    
    url = base_url + "articles"
    params = {'source': source,
            'apiKey': NEWS_API_KEY,
            'sortBy': 'top',
            }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles

