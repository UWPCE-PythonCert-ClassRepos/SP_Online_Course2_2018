
from queue import Queue
import time
import threading
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORD = 'trump'

NEWS_API_KEY = '773951043e5045baa609b2fecca82fc2'

base_url = 'https://newsapi.org/v2/'

def get_sources():
    url = base_url + 'sources' + f'?apiKey={NEWS_API_KEY}'
    params = {'language': 'en'}
    # logger.info(url)
    resp = requests.get(url, params=params)
    data = resp.json()
    logger.info(data)
    print('Got the sources.')
    sources = [src['id'].strip() for src in data['sources']]
    return sources

def get_articles(source):
    url = base_url + 'top-headlines' + f'?apiKey={NEWS_API_KEY}'
    # logger.info(url)
    params = {'source': source, 'apiKey': NEWS_API_KEY,
        'sortBy': 'top', 'language':'en',
        }
    print('requesting:', source)
    resp = requests.get(url, params=params)
    if resp.status != 200:
        print('something went wrong with {}'.format(source))
        logger.info(resp, resp.text)
        return []
    data = resp.json()
    print('got the articles from {}'.format(source))
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles
    # titles.put([str(art['title']) + str(art['description']) for art in data['articles']])

def thread_the_articles(thread_count):
    for source in sources:
        thread = threading.Thread(target=get_articles, args=(source,))
        thread.start()
        titles.put(thread)

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

if __name__ == '__main__':
    thread_count = 1
    start = time.time()

    sources = get_sources()
    titles = Queue()
    thread_the_articles(thread_count)
    titles_list = list(titles.queue)

    logger.info(titles)
    logger.info(titles_list)

    art_count = 0
    word_count = 0
    for titles in titles_list:
        art_count += len(titles)
        word_count += count_word(WORD, titles)

    print('thread count = {}'.format(thread_count))
    print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
    print('process took {:.0f} seconds'.format(time.time() - start))