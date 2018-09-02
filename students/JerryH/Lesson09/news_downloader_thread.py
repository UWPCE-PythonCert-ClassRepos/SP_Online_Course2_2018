#!/usr/bin/env python3

import time
import requests
from threading import Thread

WORD = 'trump'

NEWS_API_KEY = 'b14f1fa2d6cd4deca673ed56ce5f2035'


base_url = 'https://newsapi.org/v1/'

sources, titles = [], []

def get_sources(sources):
	"""
	Get all the english language sources of news
	'https://newsapi.org/v1/sources?language=en'
	"""

	url = base_url + 'sources'
	params = {'language': 'en'}
	resp = requests.get(url, params=params)
	data = resp.json()
	# print(data)
	# sources = [src['id'].strip() for src in data['sources']]
	sources.extend([src['id'].strip() for src in data['sources']])
	# print('all the sources')
	# print(sources)
	return sources


def get_articles(source):
	"""
	https://newsapi.org/v1/articles?source=associated-press&.....
	"""

	url = base_url + "articles"
	params = {
				'source': source,
				'apiKey': NEWS_API_KEY,
				'sortBy': 'top'
			}
	print('requesting: ', source)
	resp = requests.get(url, params=params)
	if resp.status_code != 200:  # aiohttpp has "status"
		print("something went wrong with {}".format(source))
		print(resp)
		print(resp.text)
		return []
	data = resp.json()
	# the url to the article itself is in data['articles'][i]['url']
	# titles = [str(art['title']) + str(art['description']) for art in data['articles']]
	print('Got the articles from {}'.format(source))
	titles.extend([str(art['title']) + str(art['description']) for art in data['articles']])
	return titles


def count_word(word, titles):
	word = word.lower()
	count = 0 
	for title in titles:
		if word in title.lower():
			count += 1
	return count


start = time.time()
# sources = get_sources()

# art_count = 0
# word_count = 0
# for source in sources:
# 	titles = get_articles(source)
# 	art_count += len(titles)
# 	word_count += count_word('trump', titles)

if __name__ == '__main__':
	get_sources(sources)

	l = []

	for source in sources:
		t = Thread(target=get_articles, args=(source,))
		t.start()
		l.append(t)

	for t in l:
		t.join()

	# print(WORD, 'found {} times in {} articles'.format(word_count, art_count))
	print('Process took {} seconds'.format(time.time() - start))








