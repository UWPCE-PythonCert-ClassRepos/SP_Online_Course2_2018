#!/usr/bin/env python3

import logging
import requests
from threading import Thread

WORD = 'trump'
NEWS_API_KEY = "5794703b1f624142a329ce9a4fc84041"
BASE_URL = 'https://newsapi.org/v1/'

sources = []
titles = []


def get_sources(sources):
    """
    Ask newsapi.org for all news it has access to
    """
    url = BASE_URL + 'sources'
    params = {'language': 'en'}
    r = requests.get(url, params=params)
    data = r.json()
    sources.extend([src['id'].strip() for src in data['sources']])
    #  print sources
    return sources


def get_articles(source):
    print("Gathering Articles")
    url = BASE_URL + 'articles'
    params = {
        'source': source,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'top'
        }
    print('Requesting: ', source)
    r = requests.get(url, params=params)
    if r.status_code !=200:
        print('Error with {}'.format(source))
        return
    data = r.json()
    print('Got all articles from {}'.format(source))
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])
    return titles


if __name__ == '__main__':
    get_sources(sources)

    list = []
    for source in sources:
        t = Thread(target=get_articles, args=(source,))
        t.start()
        list.append(t)

    for t in list:
        t.join()
