import requests
import threading
import time
import queue

api_key = 'ae437e6f70b64c4d86997731951f92a0'
base_url = 'https://newsapi.org/v1/'

def get_sources():
    """
    Get all the english language sources of news
    
    https://newsapi.org/v1/sources?language=en
    """
    url = base_url + 'sources'
    params = {'language': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print('All the sources')
    print(sources)
    return sources


def get_articles(source):
    """
    Get all articles for a source
    """
    url = base_url + 'articles'
    params = {'source': source,
              'apiKey': api_key,
              'sortBy': 'top'}
    print('Requesting:', source)
    resp = requests.get(url, params=params)
    if resp.status_code != '200':
        print('Something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles


def count_word(word, titles):
    """
    Count all the occurances of word in title
    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def thread_func(sources, titles):
    """
    Loop through the sources for threading
    """
    while True:
        try:
            source = sources.pop()
        except:
            break
        titles.extend(get_articles(source))
        

start = time.time()
sources = get_sources()
titles = []
threads = []

for i in range(10):
    thread = threading.Thread(target=thread_func, args=[sources, titles])
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()

count = count_word('trump', titles)
print('trump found {} times in {} articles'.format(count, len(titles)))

end = time.time()
print('The requests process took approx: {: .0f} seconds'.format(end - start))

# 1 thread takes approx: 24 seconds, 10 threads takes approx: 3 seconds