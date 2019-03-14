""" 
    Lesson 9 submision file. 
    Uses News API to get titles with multithreading.
"""
#orioginal API = "0c90527956054643acefdedb6587d07f"
#alt API 1 = "74c1d999b2bb43feaabb8c3c194fe5b3"

import time
import requests
import threading
import queue

WORD = "Boeing"

NEWS_API_KEY = "74c1d999b2bb43feaabb8c3c194fe5b3"

base_url = 'https://newsapi.org/v1/'




def get_sources():
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    response = requests.get(url, params=params).json()
    sources = [src['id'].strip() for src in response['sources']]
    print("all the sources")
    print(sources)
    return sources

def get_articles(source):
    
    url = base_url + "articles"
    params = {'source': source,
            'apiKey': NEWS_API_KEY,
            'sortBy': 'top',
            }
    print("requesting (get articles):", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    titles = [str(art['title']) + ' ' + str(art['description']) for art in data['articles']]
    #print(titles)
    return titles

def count_word(word, titles):
    word = word.lower()
    count = 0
    #print(word)
    for title in titles:
        #print(title)
        if word in title.lower():
            count += 1
    return count

def queue_handler(source):
    q.put(get_articles(source))


q = queue.Queue()
start = time.time()
sources = get_sources()
#test with partial sources because of API limits
#sources = ['the-new-york-times','associated-press', 'bbc-news','google-news','reuters']

art_count = 0
word_count = 0
threads = []

for source in sources:
    thread = threading.Thread(target=queue_handler, args=(source,))
    thread.start()
    threads.append(thread)
    #added to see threads
    print(thread.name)

for thread in threads:
    print("join", thread.name)
    thread.join()

while not q.empty():
    queue_titles = q.get()
    for title in queue_titles:
        art_count += 1
        #print(title)
        if WORD.lower() in title.lower():
            word_count += 1
    #print(count)


print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
print('Process took {:.0f} seconds'.format(time.time()-start))