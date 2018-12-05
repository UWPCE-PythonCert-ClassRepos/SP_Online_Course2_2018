"""
Shin Tran
Python 220
Assignment 9

Threading script to see how much a given word is mentioned in the news today

Uses data from the NewsAPI:
https://newsapi.org

#!/usr/bin/env python
"""

import queue
import requests
import threading
import time


WORD = "trump"
NEWS_API_KEY = "7d180fa4b3bc4a2999e1a064833f9ede"
base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    Get all the english language sources of news
    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("The sources have been obtained.")
    #print(sources)
    return sources


def get_articles(source, title_list, queueLock):
    """
    https://newsapi.org/v1/articles?source=associated-press
    &sortBy=top&apiKey=1fabc23bb9bc485ca59b3966cbd6ea26
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:  # aiohttpp has "status"
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    # the url to the article itself is in data['articles'][i]['url']
    queueLock.acquire()
    title_list.extend([str(art['title']) + str(art['description'])
        for art in data['articles']])
    queueLock.release()
    return title_list


def count_word(word, titles):
    """
    Looks for a given word in a list of article title and descriptions
    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


if __name__ == "__main__":
    start = time.time()
    sources = get_sources()
    titles = []
    thread_list = []
    queueLock = threading.Lock()

    for source in sources:
        thread = threading.Thread(target = get_articles,
            args = (source, titles, queueLock))
        thread.daemon = True  # allow ctrl-c to end
        thread.start()
        thread_list.append(thread)

    for j in thread_list:
        j.join()

    word_count = 0
    art_count = len(titles)
    word_count += count_word('trump', titles)
    print(WORD, " found {} times in {} articles.".format(word_count, art_count))
    print("Process took {:.0f} seconds.".format(time.time() - start))
