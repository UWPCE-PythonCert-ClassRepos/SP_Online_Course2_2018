import requests

url = ('https://newsapi.org/v2/sources?' +
       'language=en&' +
       'apiKey=0c90527956054643acefdedb6587d07f')

response = requests.get(url).json()
sources = [src['id'].strip() for src in response['sources']]
print(sources)