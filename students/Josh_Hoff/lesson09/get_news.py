import time
import requests
import threading

lock = threading.Lock()

WORD = 'canada'

NEWS_API_KEY = "5e3dca56fa674afe9b01464c3bd308e8"

base_url = 'https://newsapi.org/v1/'


def get_sources():

    url = base_url + 'sources'
    params = {'language': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print('all the sources')
    print(sources)
    return sources


def get_articles(source, lock, titleslist):

    url = base_url + 'articles'
    params = {'source': source,
              'apiKey': NEWS_API_KEY,
              'sortBy': 'top',
              }
    print('requesting:', source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    lock.acquire()
    titleslist.extend([str(art['title']) + str(art['description'])
              for art in data['articles']])
    lock.release()
    return titleslist


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

start = time.time()
sources = get_sources()

art_count = 0
word_count = 0
titles = []
threads = []

for source in sources:
    thread = threading.Thread(target=get_articles, args = (source, lock, titles))
    thread.daemon = True
    thread.start()
    threads.append(thread)
    
for thread in threads:
    thread.join()

art_count = len(titles)
word_count += count_word(WORD, titles)
print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
print('Process took {:.0f} seconds'.format(time.time() - start))

