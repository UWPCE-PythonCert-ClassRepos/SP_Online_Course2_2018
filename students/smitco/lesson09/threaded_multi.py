# lesson 09 threaded downloader exercise
# !/usr/bin/env python3

# took 3 sec on my machine compared to 34 secs with sync and 4 secs with async

import time
import requests
import threading
import queue

WORD = 'trump'
NEWS_API_KEY = "36f7da631b8a4373a98bcae0f0516d7f"
base_url = 'https://newsapi.org/v1/'

sources = queue.Queue()
thread_lock = threading.Lock()

def get_sources(sources):
    """ Get the english language sources of news """
    
    url = base_url + 'sources'
    params = {'langauge': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    for src in data['sources']:
        sources.put(src['id'].strip())
    print('all the sources')
    return sources
    

def get_articles():
    while not sources.empty():
        source = sources.get()
        url = base_url + 'articles'
        params = {'source': source,
                   'apiKey': NEWS_API_KEY,
                   'sortBy': 'top'
                  }
        print('requesting:', params)
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            print('something went wrong with {}'.format(source))
            print(resp)
            print(resp.text)
            sources.task_done()
            return
        data = resp.json()
        print('got the articles from {}'.format(source))
        with thread_lock:
            titles.extend([str(art['title']) + str(art['description'])
                      for art in data['articles']])
        sources.task_done()
    return titles


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

start = time.time()
titles = []

get_sources(sources)

threads = []
for i in range(100):
    thread = threading.Thread(target=get_articles)
    threads.append(thread)
    thread.start()

sources.join()

art_count = len(titles)
word_count = count_word(WORD, titles)

print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
print('Process took {:.0f} seconds'.format(time.time() - start))