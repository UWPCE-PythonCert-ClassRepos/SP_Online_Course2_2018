
import threading
import queue
import requests
import time


WORD = "ethanol"
#NEWS_API_KEY = "1794fa683ec7489c8cbb7f422e2606a2"
NEWS_API_KEY = "f374b07257ea4d948d132cdafa937708"

base_url = 'https://newsapi.org/v1/'

results = queue.Queue()

def get_sources():
    """
    Get all the english sources of news
    """
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources

def get_articles(source):
    """

    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"
              }
    print("requesting: ", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    results.put(titles)
    return titles

def word_counter(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

def news_queue(*args):
    results.put(get_articles(*args))

if __name__ == '__main__':
    start = time.time()
    sources = get_sources()
    number = len(sources)
    art_count = 0
    word_count = 0
    threads = []
    for source in sources:
        thread = threading.Thread(target=get_articles, args=(source,))
        thread.start()
        threads.append(thread)
    for i in range(number):
        news = results.get()
        art_count += len(news)
        word_count += word_counter(WORD, news)
    print("Found \'{}\' {} times in {} articles".format(WORD, word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))
