# lesson 09 threaded downloader exercise
# !/usr/bin/env python3

# sync version copied from course video
# took 34 seconds on my machine

import time
import requests

WORD = 'trump'
NEWS_API_KEY = "36f7da631b8a4373a98bcae0f0516d7f"

base_url = 'https://newsapi.org/v1/'

def get_sources():
    """ Get the english language sources of news """
    
    url = base_url + 'sources'
    params = {'langauge': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print('all the sources')
    print(sources)
    return sources

def get_articles(source):
    url = base_url + 'articles'
    params = {'source': source,
               'apiKey': NEWS_API_KEY,
               'sortBy': 'top'
              }
    print('requesting:', source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    return titles

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

start = time.time()
sources = get_sources()

art_count = 0
word_count = 0
for source in sources:
    titles = get_articles(source)
    art_count += len(titles)
    word_count += count_word(WORD, titles)

print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
print('Process took {:.0f} seconds'.format(time.time() - start))