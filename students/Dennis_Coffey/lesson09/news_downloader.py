# -*- coding: utf-8 -*-
"""
News downloader using threading

Created on Thu Apr 18 20:53:04 2019

@author: dennis coffey
"""

import sys
import threading
import queue
import time
import requests

WORD = "trump"

NEWS_API_KEY = "0c687b0ee9004be1afcf665704366932"

base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    Get all the english language sources of news
    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en",
              "apiKey": NEWS_API_KEY,
              "country": "us"
             }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("Something went wrong")
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("All the sources")
    print(sources)
    return sources

def get_articles(source):
    """ Get articles from sources"""
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}
    print("requesting: ", source)
    resp = requests.get(url, params = params)
    if resp.status_code != 200:
        print("Something went wrong with {source}".format(source))
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    # The url to the article itself is in the data['articles'][i]['url']
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    results.put(titles)
    return titles

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
        return count
    
if __name__ == '__main__':

    sources = get_sources()
    start = time.time()
    
    # limit sources to top N for testing
#    sources = sources[:10]
    
    results = queue.Queue()
   
    num_sources = len(sources)
    art_count = 0
    word_count = 0
    threads = []
    for source in sources:
        thread = threading.Thread(target=get_articles, args=(source,))
        thread.start()
        threads.append(thread)
        
    for i in range(num_sources):
        articles = results.get()
        art_count += len(articles)
        word_count += count_word(WORD, articles)

    print(WORD, "found {} times in {} articles.".format(word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))
