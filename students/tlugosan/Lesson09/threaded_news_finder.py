import threading
import time
import requests
import queue

WORD = 'trump'
NEWS_API_KEY = "84d0483394c44f288965d7b366e54a74"
base_url = 'http://newsapi.org/v1/'

my_queue = queue.Queue()


def get_sources():
    """
    'https://newsapi.org/v1/sources?language=en'
    :return:
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
    """https://newsapi.org/v1/articles?source=associated-press&sortBy=top
    &apiKey=1f"""
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              # "sortBy": "latest",
              # "sortBy": "popular",
              "sortBy": "top"
              }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description']) for art in data[
        'articles']]
    return titles


sources = get_sources()


def news_homework(*args):
    my_queue.put(get_articles(*args))


def threading_example():
    threads = []
    for i in sources:
        thread = threading.Thread(target=news_homework, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        print("joining thread {}", thread.name)
        thread.join()
    print("all threads finish")


if __name__ == '__main__':
    start = time.time()

    news_homework(sources)
    threading_example()
    art_count = 0
    word_count = 0
    while not my_queue.empty():
        articles_per_source = my_queue.get()
        art_count += len(articles_per_source)
        for i in articles_per_source:
            if WORD.lower() in i.lower():
                word_count += 1

    print(WORD, "found {} times in {} articles".format(word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))
