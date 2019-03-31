import queue
import requests
import time
import threading

#84697d4e8b104a608e3fba47b8dac45c

WORD = "military"
NEWS_API_KEY = "db0200d972284abc99e39877ad49cee5"
base_url = "https://newsapi.org/v1/"
THREADS = 20

def get_sources():
    """
    Get all the english language sources of news

    """

    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("The sources have been obtained.")
    return sources


def get_articles(source):
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:  # aiohttpp has "status"
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    return titles


def word_count(word, titles):
    """count word"""

    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

def treading_work():
    try:
        source = sources.pop()
    except IndexError:
        pass
    titles.extend(get_articles(source))

if __name__ == '__main__':
    start = time.time()
    sources = get_sources()
    threads = []
    titles = []

    for s in range(len(sources)):
        tread = threading.Thread(target = treading_work,args = ())
        tread.start()
        threads.append(tread)

    for t in threads:
        t.join()

    wordcount = 0
    wordcount += word_count('military', titles)
    articlecount = len(titles)

    print(WORD, " found {} times in {} articles.".format(wordcount, articlecount))
    print("Process took {:.0f} seconds.".format(time.time() - start))
