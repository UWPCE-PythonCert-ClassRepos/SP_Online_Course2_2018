# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 16:28:49 2018

@author: HP-Home
"""
import requests

from threading import Thread

WORD = 'trump'
NEWS_API_KEY = '4782c36a71c44196bcb04594c9816bcb'
base_url = 'https://newsapi.org/v1/'

    
sources = []


def get_sources(sources):
    url = base_url + 'sources'
    params = {'language': 'en'}
    r = requests.get(url, params=params)
    data = r.json()
    print('Got the sources')
    #print(r.url)
    sources.extend([src['id'].strip() for src in data['sources']])
    for i in sources:
        print(i)
    return sources
    
#get_sources(sources)


titles = []
    
def get_articles(source):
    print('Starting to get articles')
    url = base_url + 'articles'
    params = {'source': source,
              'apiKey': NEWS_API_KEY,
              'sortBy': 'top'}
    print('requesting:', source)
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print('Something went wrong with: {}', format(source))
        return
    data = r.json()
    print('got the articles from {}'.format(source))
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])
#    for i in titles:
#        print(i)
    return titles


        
if __name__ == '__main__':
    
    Thread(target=get_sources, args=(sources,)).start()
    l = []
    for i in sources:
        t = Thread(target=get_articles, args=(i))
        t.start()
        l.append(t)
    for x in l:
        x.join()