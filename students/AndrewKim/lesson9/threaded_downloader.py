import logging
import time
import requests
from threading import Thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
WORD = 'trump'
NEWS_API_KEY = 'b14f1fa2d6cd4deca673ed56ce5f2035'
BASE_URL = 'https://newsapi.org/v1/'


sources = []
titles = []


def get_sources(sources):
    """
        Returns a list of news sources provided at the base url
    """
    url = BASE_URL + 'sources'
    params = {'language': 'en'}
    resp  = requests.get(url, params=params )
    data = resp .json()
    sources.extend([src['id'].strip() for src in data['sources']])
    logger.info(f'Sources Obtained: {sources}')
    return sources


def get_articles(source):
    """
        Parses and returns a list of articles titles
    """
    
    url = BASE_URL + 'articles'
    params  = {'source': source,
              'apiKey': NEWS_API_KEY,
              'sortBy': 'top'}
    logger.info(f'Requesting: {source}')
    resp  = requests.get(url, params=params )
    if resp .status_code != 200:
        logger.info('error')
        return
    data = resp.json()
    logger.info('Got All The Articles')
    titles.extend([str(art['title']) + str(art['description'])
                   for art in data['articles']])
    return titles


if __name__ == '__main__':

    logger.info('Gettings sources...')
    get_sources(sources)
    lists = []
    for item in sources:
        thread = Thread(target=get_articles, args=(item,))
        thread.start()
        lists.append(thread)

    for thread in lists:
        thread.join()