#!/usr/bin/env python

"""
An Asynchronous version of the script to see how much a given word is
mentioned in the news today

Uses data from the NewsAPI:

https://newsapi.org
"""

import time
import threading
import requests

NEWS_API_KEY = "70c85127c4da4ded926f318f48b1e7ce"

WORD = "war"
base_url = 'https://newsapi.org/v1/'


# This has to run first, so doesn't really need async
# but why use two requests libraries ?
def get_sources(sources):
    """
    Get all the english language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    r = requests.get(url, params=params)
    if r.status_code != 200:  # aiohttpp has "status"
        print(f'something went wrong with: {r.status_code}')
        return
    data = r.json()
    print("Got the sources")
    sources.extend([src['id'].strip() for src in data['sources']])


def get_articles(source):
    """
    download the info for all the articles
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"
              }
    print("requesting:", source)
    r = requests.get(url, params=params)
    data = r.json()
    if r.status_code != 200:  # aiohttpp has "status"
        print(f'something went wrong with: {source}')
        return
            # awaits response rather than waiting on response in the requests version of this
    print("got the articles from {}".format(source))
    # the url to the article itself is in data['articles'][i]['url']
    titles.extend([(str(art['title']) + str(art['description']))
                   for art in data['articles']])


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


start = time.time()


# create the objects to hold the data
sources = []
titles = []

# get the sources -- this is essentially synchronous
get_sources(sources)

#thread list
threads =[]
for source in sources:
    thread = threading.Thread(target=get_articles, args=(source,))
    thread.start()
    threads.append(thread)

#join all threads
for thread in threads:
    thread.join()

art_count = len(titles)
word_count = count_word(WORD, titles)

print(f'found {WORD}, {word_count} times in {art_count} articles')
print(f'Process took {(time.time() - start):.0f} sec.')
