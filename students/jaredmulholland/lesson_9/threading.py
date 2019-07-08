"""
Name: Jared Mulholland
Assignment: Threaded Downloader

In this lesson, we looked at an asyncio based web data scraper.

In that case, there were about 100 simultaneous requests. 
Async is very well suited to many requests, but for 100 or so, 
a multi-threaded approach could work well too. So your job is to 
make a multi-threaded version of the newsapi downloader:

"""

import threading
import time
import requests
import queue

WORD = "trump"

NEWS_API_KEY = "d5ecf0a8faea4a3197c2e533f5110705"

base_url = 'https://newsapi.org/v1/'

def get_sources():
    """get all english language sources of news"""
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params = params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    return sources

def get_articles(source):
    """
    returns articles from source list
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}

    print("requesting:",  source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()

    #the url to the article itself is in data['articles'][i]['url']
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles

def thread_worker(sources, titles):
    """
    Loop through the sources to retrieve titles
    """
    while sources:
        source = sources.pop()
        title = get_articles(source)
        titles.extend(title)
 
def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in str(title).lower():
            count += 1
    return count

start = time.time()
sources = get_sources()
#sources = sources[0:10]
threads = []
titles = []

for i in range(10):
    thread = threading.Thread(target = thread_worker, args = (sources, titles))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

word_count = count_word('trump',titles)

print(WORD, "found {} times in {} articles".format(word_count, len(titles)))
print("Process took {:.0f} seconds".format(time.time() - start))


################################################################

"""
Trump found 37 times in 531 articles

1 thread: Process took 31 seconds

5 threads: Process took 8 seconds

10 threads: Process took 5 seconds

20 threads: Process took 4 seconds




