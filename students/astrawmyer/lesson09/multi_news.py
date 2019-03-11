#Your API key is: 0c90527956054643acefdedb6587d07f

import time
import requests

WORD = "boeing"

NEWS_API_KEY = "0c90527956054643acefdedb6587d07f"

base_url = 'https://newsapi.org/v2/'


def get_sources():
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    response = requests.get(url, params=params).json()
    sources = [src['id'].strip() for src in response['sources']]
    print("all the sources")
    print(sources)
    return sources

def get_articles(source):
    
    url = base_url + "articles"
    params = {'source': source,
            'apiKey': NEWS_API_KEY,
            'sortBy': 'top',
            }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('something went wrong with {}'.format(source))
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in titles:
            count += 1
    return count

start = time.time()
sources = get_sources()

""" art_count = 0
word_count = 0
for source in sources:
    titles = get_articles(source)
    art_count += len(titles)
    word_count += count_word(WORD, titles)

print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
print('Process took {:.0f} seconds'.format(time.time()-start)) """