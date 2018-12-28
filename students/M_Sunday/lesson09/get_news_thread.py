import time
import requests
import threading
import logging
import time

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# uses data from the NewsAPI:
# https://newsapi.org

WORD = "TRUMP"

NEWS_API_KEY = "d203731e8eba4823892d2c6390bcd700"

base_url = "https://newsapi.org/v1/"


def get_sources():
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    # print("all the sources")
    # print(sources)
    return sources


def get_articles(source, title_list, sema):
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    sema.acquire()
    title_list.extend([str(art['title']) + str(art['description']) for art in
                    data['articles']])
    sema.release()
    time.sleep(0.0)
    return title_list


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
list_of_threads = []
title_list = []
sema = threading.Semaphore()

for source in sources:
    thread_id = threading.Thread(target=get_articles, args=(source,
                                                            title_list, sema))
    thread_id.start()
    logging.info(f'Thread_ID: {thread_id}')
    list_of_threads.append(thread_id)

for thread in list_of_threads:
    art_count += len(title_list)
    word_count += count_word(WORD, title_list)
    thread.join()

logging.info(f'Thread: {thread}')

print(WORD, "found {} times in {} articles".format(word_count, art_count))
print("Process took {:.0f} seconds".format(time.time() - start))
