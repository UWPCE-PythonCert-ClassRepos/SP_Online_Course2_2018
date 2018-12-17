#!/usr/bin/env python
"""
Regular synchronous script to see how much a given word is mentioned in the news today
https://newsapi.org
NOTE : you need to register with the web site to get a key
"""
import time
import requests
import threading
import queue

__author__ = "Wieslaw Pucilowski"

WORD = "trump"

NEWS_API_KEY = "aaf5ea8408b845678ae5bd3c7f01ad18"

base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    Get all the english language sources of news
    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + 'sources'
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the {} sources:".format(len(sources)))
    print(sources)
    return sources

def get_articles(source):
    """
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              # "sortBy" "latest", # some sources don't support latest
              "sortBy": "top",
              # "sortBy": "popular",
        }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200: # aiohttpd has "status"
        print("something went wrong with {}".format(source))
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


def get_artickles_queue(source):
    titles = get_articles(source)
    q.put(titles)

if __name__ == "__main__":
   
   art_count = 0
   word_count = 0

   q = queue.Queue()
   threads = []
   
   start = time.time()
   sources = get_sources()
   start2 = time.time()

   # giving the free key limitation reducing polling to 10 sources
   print("\nGiving the free key limitation reducing polling to 10 sources.\n")
   for i in range(len(sources[:10])):
       t = threading.Thread(target=get_artickles_queue, args=(sources[i],))
       t.start()
       threads.append(t)
   
   for t in threads:
       t.join()
   print('All threads/requests finished, time to parse titles in the queue\n')
   while not q.empty():
      titles = q.get()
      art_count += len(titles)
      word_count += count_word('trump', titles)
   
   
   print(WORD, "found {} times in {} articles".format(word_count, art_count))
   print("Process took {:.0f} seconds, Articles scan took {:.0f} seconds".format(time.time() - start,
                                                                                 time.time() - start2)
                                             )

############# Statistics ###############
########################################
# sequential:
# 'trump' found 70 times in 563 articles
# Process took 29 seconds
########################################
# threads:
# 'trump' found 52 times in 563 articles
# Process took 7 seconds
########################################
# threads and queue
# 'trump' found 55 times in 563 articles
# Process took 2 seconds
