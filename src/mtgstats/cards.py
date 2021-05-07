GAMEPLAY_FIELDS = [
    'name', 'mana_cost', 'cmc',
    'type_line',
    'oracle_text',
    'power','toughness',
    'colors', 'color_identity','keywords'
]

EXTRA_FIELDS = [
    'edhrec_rank', 'rarity'
]

def parse_cards(card_list, fields_to_keep = GAMEPLAY_FIELDS+EXTRA_FIELDS):
    if type(card_list) is not list:
        card_list = [card_list]
    return [parse_card(card, fields_to_keep) for card in card_list]

def parse_card(card, fields_to_keep = GAMEPLAY_FIELDS+EXTRA_FIELDS):
    parsed = { k:v for k,v in card.items() if k in fields_to_keep }
    return parsed
