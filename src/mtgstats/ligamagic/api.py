import requests
from bs4 import BeautifulSoup
import pathlib

LIGAMAGIC_API_URL = 'https://www.ligamagic.com.br'
DEBUG = False

headers = {'User-Agent': 'Chrome'}

def get_card_pricings(card, set=''):
    url = query_url(card, set)
    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.content, 'html.parser')

    if set == '':
        sets = find_card_sets(bs)
    else:
        sets = [set]

    results = {}
    for s in sets:
        url = query_url(card, s)
        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.content, 'html.parser')
        pricings = bs.find('div', id='mobile-precomedio').find_all('div', class_='bloco-preco-superior')
        pricing_data = [parse_pricing_details(p) for p in pricings]
        results[s] = pricing_data
    
    return results


def find_card_sets(bs):
    sets = []
    edicoes = bs.find('ul', {'class' :'edicoes edicoes-fixo'}).find_all('img')
    for img_tag in edicoes:
        # The file name is <SET>_<RARITY>
        set_name, _ = pathlib.Path(img_tag['data-src']).stem.split('_')
        sets.append(set_name)
    return sets


def parse_pricing_details(details):
    extra = details.find('div', class_='col-ext').text
    lower = details.find('div', class_='col-prc-menor').text
    avg = details.find('div', class_= 'col-prc-medio').text
    upper = details.find('div', class_= 'col-prc-maior').text
    return (extra, lower, avg, upper)

def query_url(card_name, set=''):
    return f'{LIGAMAGIC_API_URL}/?view=cards/card&card={card_name}&ed={set}'
