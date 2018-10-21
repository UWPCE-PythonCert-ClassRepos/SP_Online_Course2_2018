"""
Thomas Horn
Lesson 9

Async Webrequests
"""

import requests
import time

API_KEY = '439e5fb99a9b4098aa0ae52556559c1a'
URL = 'https://newsapi.org/v1/'
WORD = 'trump'


def get_sources():
    """
    Get all the English language sources of news.
    """
    url = URL + 'sources'
    params = {
        'language': 'en'
    }

    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]

    print(f"Sources: {sources}")
    return sources


def get_articles(source):
    url = URL + 'articles'
    params = {
        'source': source,
        'apiKey': API_KEY,
        'sortBy': 'top'
    }
    print(f"Requestsing: {source}")

    resp = requests.get(url, params=params)
    if resp.status_code != 200:  # aiohttp has 'status'
        print("Something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []

    data = resp.json()
    # The url itself is in data['articles'][i]['url']
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles


def count_word(titles):
    word = WORD.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


if __name__ == "__main__":
    # Start timer
    start = time.time()
    sources = get_sources()

    # Setup article count and word count
    art_count = 0
    word_count = 0

    # Loop through sources and get num articles and count words
    for source in sources:
        titles = get_articles(source)
        art_count += len(titles)
        word_count += count_word(titles)
    
    print(f"{WORD}: Found {word_count} times in {art_count} articles.")
    print("Process took {:.0f} seconds.".format(time.time() - start))


