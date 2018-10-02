"""
Thomas Horn
Lesson 9
"""

import requests
import threading
import time
import queue

API_KEY = '439e5fb99a9b4098aa0ae52556559c1a'
URL = 'https://newsapi.org/v1/'
WORD = 'trump'
THREADS = 100 


def get_sources():
    # Build URL and basic parameters
    url = URL + 'sources'
    params = {
        'language': 'en',
        'apiKey:': API_KEY
    }

    # Use requests and check for proper response code (want 200)
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error retrieving sources.")
        return []
    
    # Get and return formatted JSON data
    data = response.json()
    sources = [src['id'].strip() for src in data['sources']]
    return sources


def get_articles(source):
    """ Gets info per source. """
    url = URL + 'articles'
    params = {
        'sources': source,
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error retrieving article from source: {source}")
        return []
    
    data = response.json()
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]

    return titles
    

if __name__ == "__main__":
    # Get sources first and print to confirm
    sources = get_sources()
    print(f'Sources Found: {sources}')

    # Prep threads
    print(f'Current Threads: {THREADS}')
    threads = []

    # Activate and join the threads
    for source in sources:
        thread = threading.Thread(target=get_articles, args=(source,))
        thread.start()
        threads.append(thread)

    for item in threads:
        item.join()

    


