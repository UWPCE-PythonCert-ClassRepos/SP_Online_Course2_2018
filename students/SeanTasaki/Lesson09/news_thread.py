'''
Sean Tasaki
12/13/2018
Lesson09
'''

import time
import requests
import threading
import queue

search_word = input("Enter the word you would like to search for:\n>> ")

NEWS_API_KEY = 'b14f1fa2d6cd4deca673ed56ce5f2035'


base_url = 'https://newsapi.org/v1/'

sources, titles = [], []

def get_sources():
    """
    Get all the english language sources of news
    'https://newsapi.org/v1/sources?language=en'
    """

    url = base_url + 'sources'
    params = {'language': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources.extend([src['id'].strip() for src in data['sources']])
    print(f'Gathering articles from the following sources: \n{sources}')
    return sources


def get_articles(source, titles, queueLock):
    """
     https://newsapi.org/v1/articles?source=associated-press
    &sortBy=top&apiKey=1fabc23bb9bc485ca59b3966cbd6ea26
    """

    url = base_url + "articles"
    params = {
                'source': source,
                'apiKey': NEWS_API_KEY,
                'sortBy': 'top'
            }
    print('requesting: ', source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:  # aiohttpp has "status"
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    # the url to the article itself is in data['articles'][i]['url']
    # titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    queueLock.acquire()
    print('Got the articles from {}'.format(source))
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])
    queueLock.release()
    return titles


def count_word(word, titles):
    word = word.lower()
    count = 0 
    for title in titles:
        if word in title.lower():
            count += 1
    return count




if __name__ == '__main__':

    start = time.time()
    sources = get_sources()
    titles = []
    thread_list = []
    queueLock = threading.Lock()

    for source in sources:
        thread = threading.Thread(target = get_articles,
            args = (source, titles, queueLock))
        print(f'This is the thread for source: {source}.')
        thread.daemon = True  # allow ctrl-c to end
        thread.start()
        thread_list.append(thread)

    for j in thread_list:
        print(f'Joining thread: {j}.')
        j.join()

    art_count = len(titles)
    word_count = 0   
    word_count += count_word(search_word, titles)
    print(search_word, 'found {} times in {} articles'.format(word_count, art_count))
    print('Process took {:.00f} seconds'.format(time.time() - start))