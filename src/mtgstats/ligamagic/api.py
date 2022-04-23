import requests
from bs4 import BeautifulSoup

LIGAMAGIC_API_URL = 'https://www.ligamagic.com.br'
DEBUG = False

def get_card_pricings(card, set=''):
    url = query_url(card, set)
    response = requests.get(url)
    bs = BeautifulSoup(response.content, 'html.parser')

    pricings = bs.find('div', id='mobile-precomedio').find_all('div', class_='bloco-preco-superior')
    pricing_data = [parse_pricing_details(p) for p in pricings]
    return pricing_data


def parse_pricing_details(details):
    extra = details.find('div', class_='col-ext').text
    lower = details.find('div', class_='col-prc-menor').text
    avg = details.find('div', class_= 'col-prc-medio').text
    upper = details.find('div', class_= 'col-prc-maior').text
    return (extra, lower, avg, upper)

def query_url(card_name, set=''):
    return f'{LIGAMAGIC_API_URL}/?view=cards/card&card={card_name}&ed={set}'
