# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import logging
import requests
from threading import Thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
WORD = 'earthquake'
NEWS_API_KEY = '550401f4c305476790e442b94b035101'
BASE_URL = 'https://newsapi.org/v1/'


sources = []
titles = []


def get_sources(sources):
    url = BASE_URL + 'sources'
    parameters = {'language': 'en'}
    r = requests.get(url, params=parameters)
    data = r.json()
    logger.info('Getting Sources')
    sources.extend([src['id'].strip() for src in data['sources']])
    return sources


def get_articles(source):
    logger.info('Getting Articles')
    url = BASE_URL + 'articles'
    parameters = {'source': source,
              'apiKey': NEWS_API_KEY,
              'sortBy': 'top'}
    logger.info('Requesting')
    r = requests.get(url, params=parameters)
    if r.status_code != 200:
        logger.info('Error!!!!!!!!!')
        return
    data = r.json()
    logger.info('Got All The Articles')
    titles.extend([str(art['title']) + str(art['description'])
                   for art in data['articles']])
    return titles


if __name__ == '__main__':

    get_sources(sources)
    list = []
    for item in sources:
        thread = Thread(target=get_articles, args=(item,))
        thread.start()
        list.append(thread)

    for thread in list:
        thread.join()
