# Lesson 09: threading
# Natalie Rodriguez

import threading
import queue
import requests

WORD = "kavanaugh"
NEWS_API_KEY = "36b1a4521bb5453bbbba61c0131b9121"

base_url = 'https://newsapi.org/v1/'


def get_sources():
    url = base_url + "sources"
    params = {"language": "en",
              "apiKey": NEWS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources

def get_articles(source):
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
    return titles


if __name__ == '__main__':
    news_queue = queue.Queue()


    def add_news_queue(*args):
        news_queue.put(get_articles(*args))


    sources = get_sources()
    threads = []

    for s in sources:
        thread = threading.Thread(target=add_news_queue, args=(s,))
        thread.start()
        print("Thread %s started" % thread.name)
        threads.append(thread)

    for t in threads:
        t.join()