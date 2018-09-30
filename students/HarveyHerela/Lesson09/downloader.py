import configparser
import requests
import threading
import time

base_url = 'https://newsapi.org/v2/'

num_threads = 91

def get_api_key():
    try:
        config = configparser.ConfigParser()
        config.read('.config/config')
        key = config["newsapi"]["API_KEY"]
        return key
    except:
        print("Error getting API key!")
        return

def get_sources(api_key):
    url = base_url + "sources"
    params = {
        'language': 'en',
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error getting sources!")
        print(f"Tried: {url}?language=en&apiKey={api_key}")
        print("Got back: ", response.status_code)
        print(response.text)
        return []
    data = response.json()
    sources = [src['id'].strip() for src in data['sources']]
    return sources

def get_articles(source, api_key):
    url = base_url + "everything"
    params = {
        "sources": source,
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error getting articles from {source}!")
        print(response)
        print(response.text)
        return None
    data = response.json()
    titles = [str(art['title']) + str(art['description'])
        for art in data['articles']]
    return titles

if __name__ == '__main__':

    # First, get the sources, since they're common.
    # No sense in getting them multiple times!
    print("Reading config file")
    api_key = get_api_key()
    print("Gathering sources")
    sources = get_sources(api_key)
    print(f"Found {len(sources)} sources.")

    with open("results.txt", 'a') as results_file:
        print(f"Running with {num_threads} threads")
        start_time = time.time()
        threads = []
        threadcount = 0

        for s in sources:
            thread = threading.Thread(target=get_articles, args=(s, api_key))
            threads.append(thread)
            thread.start()
            threadcount += 1
            if threadcount == num_threads:
                for t in threads:
                    t.join()
                threadcount = 0
                threads = []
        end_time = time.time()
        duration = end_time - start_time
        results_file.write(f"{num_threads} threads took about {duration:.2f} seconds\n")

