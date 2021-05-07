import requests

SCRYFALL_API_URL = 'https://api.scryfall.com'
DEBUG = True

def search(query_string, limit = None):
    cards = []
    url = query_url(query_string)
    has_more = True
    # While there are more cards to fetch and we haven't exceeded the limit
    # don't swap the order on the or clause as it should return limit if it is
    # not None or else infinity
    while has_more and len(cards) < (limit or float('inf')):
        if DEBUG:
            print(f'Making request to {url}')
        response = requests.get(url)
        if response.ok:
            cards.extend(response.json()['data'])
        has_more = response.json()['has_more']
        if has_more:
            url = response.json()['next_page']
    # Sometimes we may exceed limit because it is not a multiple of
    # scryfall's page length, in this case we slice the list
    return cards[:limit]

def query_url(query_string):
    return f'{SCRYFALL_API_URL}/cards/search?q={query_string}'
