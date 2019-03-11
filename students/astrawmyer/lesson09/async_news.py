import time
import asyncio
import aiohttp
import requests

WORD = "Boeing"

NEWS_API_KEY = "0c90527956054643acefdedb6587d07f"

base_url = 'https://newsapi.org/v1/'

async def get_sources(sources):
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    session = aiohttp.ClientSession()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, params=params) as resp:
            data = await resp.json()
            print("got the sources")
    sources.extend([src['id'].strip() for src in data['sources']])

async def get_articles(source):
    url = base_url + "articles"
    params = {'source': source,
            'apiKey': NEWS_API_KEY,
            'sortBy': 'top',
            }
    print("requesting:", source)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, params=params) as resp:
            if resp.status !=200:
                print("somthing went wrong with {}".format(source))
                await asyncio.sleep(0)
                return
            data = await resp.json()
            print("got the articles from {}".format(source))
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        #print(title)
        if word in titles:
            count += 1
    return count

start = time.time()

loop = asyncio.get_event_loop()

sources = []
titles = []

loop.run_until_complete(get_sources(sources))

jobs = asyncio.gather(*(get_articles(source) for source in sources))
loop.run_until_complete(jobs)
loop.close()

art_count = len(titles)
word_count = count_word(WORD, titles)

print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
print('Process took {:.0f} seconds'.format(time.time()-start))