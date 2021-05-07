import requests

SCRYFALL_API_URL = 'https://api.scryfall.com'
DEBUG = True

def search(query_string):
    cards = []
    url = query_url(query_string)
    has_more = True
    while has_more:
        if DEBUG:
            print(f'Making request to {url}')
        response = requests.get(url)
        if response.ok:
            cards.extend(response.json()['data'])
        has_more = response.json()['has_more']
        if has_more:
            url = response.json()['next_page']
    return cards

def query_url(query_string):
    return f'{SCRYFALL_API_URL}/cards/search?q={query_string}'
