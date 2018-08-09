#!/usr/bin/env python3
"""Multithreaded news scraper module"""
import logging
import threading
import time
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = 'https://newsapi.org/v1/'
HTTP_OK = 200
NEWS_API_KEY = "84d0483394c44f288965d7b366e54a74"
SEARCH_WORD = 'trump'
THREAD_COUNT = 20


def get_sources():
    """Returns a list of news sources provided at the base url

    Returns:
        list: News sources
    """
    url = f'{BASE_URL}sources'
    params = {'language': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    srcs = [src['id'].strip() for src in data['sources']]

    logger.info(f'Sources obtained: {srcs}')

    return srcs


def get_articles(source):
    """Parses and returns a list of articles titles from the specified news
       source

    Args:
        source (str): News source

    Returns:
        list: Article titles
    """
    url = f'{BASE_URL}articles'
    params = {'source': source,
              'apiKey': NEWS_API_KEY,
              'sortBy': 'top'}

    logger.info(f'Requesting: {source}')
    resp = requests.get(url, params=params)
    if resp.status_code != HTTP_OK:
        logger.info(f'Something failed with: {source}')
        logger.info(resp)
        logger.info(resp.text)
        return []

    d = resp.json()
    t = [str(art['title']) + str(art['description']) for art in d['articles']]
    return t


def word_count(word, titles):
    """Counts the occurrences of the specified word in the specified article

    Args:
        word (str): Search word.
        titles (str): Article title.

    Returns:
        int: Search word occurrence count.
    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def thread_worker(sources, titles):
    """Thread function that extracts all of the article titles from a news
       source. It acts upon one source at a time until all have been exhausted.

    Args:
        sources (list): Queue of news sources. Passed by ref, therefore this
                        function only operates on it using its own member
                        functions so all changes are global. This is
                        necessary since this data is shared between all
                        running threads.
        titles (list): List of titles. Passed by ref, therefor this function
                       only operates on it using its own member functions so
                       all changes are global. This is
                       necessary since this data is shared between all
                       running threads.
    """
    source = ''
    while True:
        try:
            source = sources.pop()
        except IndexError:
            break
        titles.extend(get_articles(source))


def main():
    """Main function"""
    logger.info('Gettings sources...')
    start = time.time()
    sources = get_sources()

    logger.info('Getting articles...')
    titles = []
    threads = []
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=thread_worker, args=[sources, titles])
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end = time.time()
    print(f'The requests process took approx: {end - start: .0f} seconds')

    count = word_count(SEARCH_WORD, titles)
    print(f'{SEARCH_WORD} appeared {count} times in {len(titles)} articles')


if __name__ == '__main__':
    main()
