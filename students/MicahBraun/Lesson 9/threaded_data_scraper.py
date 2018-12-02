# --------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: threaded_data_scraper.py
# DATE CREATED: 12/01/2018
# PURPOSE: Lesson 09 Assignment
# DESCRIPTION:  Program runs utilizing the same idea behind the async and
#               sync versions of the newsapi downloader programs but using
#               multithreading in its place.
# NOTES: I had been trying to achieve the same results in displaying
#        the word searched and number of times it appeared in the articles
#        brought in, but could not figure out a way to make this work w/
#        threading... (and I burned through several API Keys while trying
#        to do so... is there a way that this is accomplished?)
# --------------------------------------------------------------------------
import requests
from threading import Thread
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


def get_articles(source):
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
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])
    return titles


if __name__ == '__main__':
    start = time.time()
    get_sources(sources)

    list_items = []

    for source in sources:
        thread = Thread(target=get_articles, args=(source,))
        thread.start()
        list_items.append(thread)

    for thread in list_items:
        thread.join()

    print('Process took {} seconds'.format(time.time() - start))
