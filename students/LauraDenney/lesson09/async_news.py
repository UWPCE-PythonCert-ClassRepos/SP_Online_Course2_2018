import time
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WORD = 'trump'

NEWS_API_KEY = '773951043e5045baa609b2fecca82fc2'

base_url = 'https://newsapi.org/v2/'

async def get_sources(sources):
    url = base_url + 'sources' + f'?apiKey={NEWS_API_KEY}'
    params = {'language': 'en'}
    logger.info(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl = False, params=params) as resp:
            data = await resp.json()
            logger.info(data)
            print('Got the sources')
    sources.extend([src['id'].strip() for src in data['sources']])

async def get_articles(source):
    url = base_url + 'top-headlines' + f'?apiKey={NEWS_API_KEY}'
    logger.info(url)
    params = {'source': source, 'apiKey': NEWS_API_KEY,
        'sortBy': 'top', 'language':'en',
        }
    print('requesting:', source)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, params=params) as resp:
            if resp.status != 200:
                logger.info(resp.status)
                print('something went wrong with {}'.format(source))
                #this next await is needed in order to hit the #following await
                await asyncio.sleep(0)
                return
            #this next line says 'release control back to the #main loop while I am waiting for this request to #come through'
            data = await resp.json()
            print('got the articles from {}'.format(source))
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
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
print('process took {:.0f} seconds'.format(time.time() - start))