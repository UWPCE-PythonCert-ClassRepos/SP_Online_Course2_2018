# Multi-threading to extract news article from the web

import requests
import threading
import queue
import time

titles = []

# synchronous script
# Get new key from https://newsapi.org/ if fail

def get_sources(base_url):
    '''
    Same function from class example
    '''
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources
    
def get_articles(source):
    '''
    Same function from class example with minor edits
    '''
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top",
              }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    # Modified from existing program from class to extend to collect data via a global list variable
    titles.extend([str(art['title']) + str(art['description'])
              for art in data['articles']])
    return titles

def count_word(word, titles):
    '''
    Same function from class example
    '''
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count
    
def multi_threading_newsapi(WORD, base_url, NEWS_API_KEY):
    '''
    Function to process article extraction
    '''
    art_count = 0
    word_count = 0
    threads = []
    sources = get_sources(base_url)
    # Queue was not used to collect results due to difficulities in creating a mulit thread queue
 
    for source in sources:
        thread = threading.Thread(target=get_articles, args=(source,))
        thread.setDaemon(True)
        thread.start()
        print('Thread %s started' % thread.name)
        threads.append(thread)
    
    for thread in threads:
        thread.join()
        print('all threads finished')

    word_count = count_word(WORD, titles)
    art_count = len(titles)

    return (word_count, art_count)

if __name__ == '__main__':
    # clock in
    t0 = time.time()
    WORD = "Trump"
    NEWS_API_KEY = "2e05c437a9904c608b2f831272ffa374"
    base_url = 'https://newsapi.org/v1/'
    solution = multi_threading_newsapi(WORD, base_url, NEWS_API_KEY)
    print(WORD, "found {} times in {} articles". format(solution[0], solution[1]))
    # clock out
    t1 = time.time()
    print("This program ran for:", t1 - t0)
