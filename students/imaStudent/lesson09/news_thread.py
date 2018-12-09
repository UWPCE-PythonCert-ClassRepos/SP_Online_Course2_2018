import time
import requests
import threading


WORD = "trump"
NEWS_API_KEY = "84d0483394c44f288965d7b366e54a74"
BASE_URL = 'https://newsapi.org/v1/'

lock = threading.Lock()
art_count = 0
word_count = 0

def get_sources():
    url = BASE_URL + "sources"
    params = {'language': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print(sources)
    return sources


def get_articles(source):
    url = BASE_URL + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": 'top',
             }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('Something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description'])
        for art in data['articles']
    ]
    return titles


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def thread_worker(source):
    global art_count, word_count
    titles = get_articles(source)
    with lock:
        art_count += len(titles)
        word_count += count_word(WORD, titles)


if __name__ == '__main__':
    threads = []

    start = time.time()
    sources = get_sources()

    for s in sources:
        t = threading.Thread(target=thread_worker, args=(s,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(WORD, " found {} times in {} articles".format(word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))
