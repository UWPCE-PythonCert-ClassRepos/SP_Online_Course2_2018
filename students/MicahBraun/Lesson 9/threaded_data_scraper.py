# --------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: threaded_data_scraper.py
# DATE CREATED: 12/01/2018
# UPDATED: 12/02/2018
# DESCRIPTION:  Program runs utilizing the same idea behind the async and
#               sync versions of the newsapi downloader programs but using
#               multithreading in its place.
# NOTES ON UPDATE: Made edits based on instructor feedback:
#                  - included source limitations to avoid running out of
#                    free API requests
#                  - imported Semaphore from threading to implement
#                    internal counter for threaded processes
#                  - added count_word() function, along with print outs
# *Program runs on Pycharm 2018.3 (Windows 10, 64x) and Ubuntu 18.04.1 LTS
#  Both running Python 3.6.7
# --------------------------------------------------------------------------

import requests
from threading import Thread, Semaphore
import time

WORD = "russia"
NEWS_API_KEY = "f7b5ba7c04074455903bf52e04e3c54f"
base_url = 'https://newsapi.org/v1/'

sources = []
titles = []


def get_sources(sources):
    """
        Function connects with base_url to obtain sources
        with the outlined parameters (English language articles)
    """
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources.extend([src['id'].strip() for src in data['sources']])
    return sources


def get_articles(source, titles, sem):
    """

    """
    url = base_url + "articles"
    params = {
        "source": source,
        "apiKey": NEWS_API_KEY,
        "sortBy": "top",
    }
    print('Requesting: ', source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('An error occurred with {}'.format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    print('Retrieved: {}'.format(source))
    sem.acquire()
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])
    sem.release()
    return titles


def count_word(word, titles):
    """

    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


if __name__ == '__main__':
    start = time.time()
    w_count = 0
    a_count = 0
    get_sources(sources)

    sem = Semaphore()

    list_items = []

    for source in sources[:5]:
        thread = Thread(target=get_articles, args=(source, titles, sem))
        thread.start()
        list_items.append(thread)

    for thread in list_items:
        a_count += len(titles)
        w_count += count_word('russia', titles)
        thread.join()

    print('Process took {} seconds'.format(time.time() - start))
    # print(titles)
    print('The word \'{}\' was found {} times in {} articles.'.format(WORD, w_count, a_count))
