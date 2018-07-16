#!/usr/bin/env python3

from configparser import ConfigParser
import requests
import logging
import threading


logging.basicConfig(level=logging.INFO)

CONF_FILE = 'config.ini'
configs = ConfigParser()
configs.read(CONF_FILE)
API_KEY = configs['DEFAULT']['key']
BASE_URL = 'https://newsapi.org/v1/'
WORD = 'trump'
THREADS = 10


def get_sources():
    logging.info('Getting sources')
    url = '{}sources'.format(BASE_URL)
    params = {'language': 'en'}
    response = requests.get(url, params=params)
    data = response.json()
    resources = [
        src['id'].strip() for src in data['sources']
    ]
    return resources


my_data = get_sources()
logging.info('Sources: {}'.format(my_data))


def get_articles(source):
    url = '{}articles'.format(BASE_URL)
    params = {
        'source': source,
        'apiKey': API_KEY,
        'sortBy': 'top',
    }
    logging.info('Requesting: {}'.format(source))
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logging.info('Something went wrong with {}'.format(source))
        logging.info(response)
        logging.info(response.text)
        return []
    data = response.json()
    titles = [
        str(art['title']) + str(art['description'])
        for art in data['articles']
    ]
    return titles


def worker():
    while True:
        try:
            source = my_data.pop()
        except IndexError:
            pass
        titles = get_articles(source)
        logging.info('Titles: '.format(titles))


if __name__ == '__main__':
    threads = []
    for _ in range(THREADS):  # number of threads
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
