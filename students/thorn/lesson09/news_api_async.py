"""
Thomas Horn
Lesson 9

Async Webrequests
"""

import aiohttp
import asyncio
import time

API_KEY = '439e5fb99a9b4098aa0ae52556559c1a'
URL = 'https://newsapi.org/v1/'
WORD = 'trump'

# Globals to hold results for async called data
titles = []
sources = []


async def get_sources(sources):
    """
    Gets all english language sources of news.

    Has to run first and doesn't need async.  The website returns a chunk of sources.  But, no point in 
    using 2 requests libraries.
    """
    url = URL + 'sources'
    params = {"language": 'en'}
    
    # AIOHTTP session start
    session = aiohttp.ClientSession()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, params=params) as resp:
            data = await resp.json()
            print("Sources found")
    sources.extend([src['id'].strip() for src in data['sources']])


async def get_articles(source):
    url = URL + 'articles'
    params = {
        'source': source,
        'apiKey': API_KEY,
        'sortBy': 'top'
    }
    print("Requesting:", source)

    # Async handling of HTTP.  Create client session with async 'with' context manager.
    async with aiohttp.ClientSession() as session:
        # Second context manager for easy cleanup, then pass in parameters
        async with session.get(url, ssl=False, params=params) as resp:
            # If status is bad -> pass 0 to async sleep to prevent any actual sleeping to release control back to
            # the main loop.
            if resp.status != 200:
                print("Something went wrong with {}".format(source))
                await asyncio.sleep(0)
                return

            # ASYNC KEY: This says that it is awaiting a response INSTEAD of waiting for the response as in sync
            # Await the response allows it release loop back to the loop, then it will have 
            # the response when asked again
            data = await resp.json()
            print(f"Got articles from {source}")

    # Extend the global titles.  Aync running on the same thread allows the extend to only be called on the titles
    # object once
    titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])


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

    # Async loop
    loop = asyncio.get_event_loop()

    # Get the sources - essentially synchronous
    loop.run_until_complete(get_sources(sources))

    # Run article loop
    jobs = asyncio.gather(*(get_articles(source) for source in sources))
    loop.run_until_complete(jobs)
    loop.close()

    art_count = len(titles)
    word_count = count_word(titles)
    
    print(f"{WORD}: Found {word_count} times in {art_count} articles.")
    print("Process took {:.0f} seconds.".format(time.time() - start))


