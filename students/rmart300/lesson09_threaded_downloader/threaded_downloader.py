from queue import Queue
import requests
import threading
import time

API_KEY = '48db028227cb4ff8a3b2008ee3bcb75a'
BASE_URL = 'https://newsapi.org/v1/'
WORD = 'trump'

source_queue = Queue()
wc_queue = Queue()
ac_queue = Queue()

def get_sources():
    """ get list of sources from api """

    url = f"{BASE_URL}sources"
    params = {'language':'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [ src['id'].strip() for src in data['sources'] ]
    return sources

def get_articles(source):
    """ get list articles from source from api """

    print(f'getting articles for {source}')
    url = f"{BASE_URL}articles"
    params = { 'source': source, 'apiKey': API_KEY, 'sortBy': 'top' }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(resp.text)
        return []

    data = resp.json()
    titles = [ f"{art['title']} {art['description']}" for art in data['articles'] ]

    return titles

def count_word(word, titles):
    """ get count of word found in list of article titles """
    
    count = 0
    for title in titles:
        if word.lower() in title.lower():
            count += 1

    return count

def process_queue():
    """ gets source from queue and gets articles and count of word 
        adds word cound and article count to queues for summing up later 
    """

    while True:
        current_source = source_queue.get()
        titles = get_articles(current_source)
        words = count_word(WORD, titles)

        wc_queue.put(words)
        ac_queue.put(len(titles))

        source_queue.task_done()

if __name__ == '__main__':

    start_time = time.time()
    thread_count = 10
    source_list = get_sources()
    sources_processed = 0

    while sources_processed < len(source_list):

        max_thread = thread_count if len(source_list) - sources_processed > thread_count else len(source_list) - sources_processed
        print(f"max_thread {max_thread} and sources processed {sources_processed}/{len(source_list)}")

        for _ in range(max_thread):

            thread = threading.Thread(target=process_queue)
            print(f'starting thread {thread.getName()}')
            thread.daemon = True
            thread.start()

        for source in source_list[sources_processed: sources_processed + max_thread]:
            source_queue.put(source)
            sources_processed += 1

        #Blocks until all items in the queue have been gotten and processed
        source_queue.join()
        
    word_count = sum(wc_queue.get() for _ in range(len(source_list)))
    article_count = sum(ac_queue.get() for _ in range(len(source_list)))
    end_time = time.time()
    print(f"found {WORD} {word_count} times in {article_count} articles")
    print(f"finished in {end_time - start_time}")
