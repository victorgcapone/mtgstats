import re

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

MAIN_FACE_FIELDS = [
    'name', 'mana_cost', 'type_line'
]

MANA_SYMBOL_REGEX = "{([XUWBRGC0-9/]*)}"

LETTERS_MANA_SYMBOL = "XUWBRGC"

TYPE_LINE_SEPARATOR = '—'

def parse_cards(card_list, fields_to_keep = GAMEPLAY_FIELDS+EXTRA_FIELDS):
    if type(card_list) is not list:
        card_list = [card_list]
    return [parse_card(card, fields_to_keep) for card in card_list]

def parse_card(card, fields_to_keep = GAMEPLAY_FIELDS+EXTRA_FIELDS, parse_faces=True, main_face='front'):
    parsed = keep_card_fields(card, fields_to_keep)
    faces = card.get('card_faces', False)
    if parse_faces and faces:
        parsed_faces = __parse_faces(faces, card, fields_to_keep)
        parsed['faces'] = parsed_faces

        # Set the data of the card to the data of the main face (front or flip)
        main_face = 0 if main_face == 'front' else 1
        for field in MAIN_FACE_FIELDS:
            parsed[field] = parsed_faces[0][field]
    return parsed

def __parse_faces(faces, card, fields_to_keep):
    parsed_faces=[]
    for face in faces:
        parsed_face = keep_card_fields(face, fields_to_keep)
        # Each faces has the same color identity of the card as a whole
        parsed_face['color_identity'] = card['color_identity']
        parsed_face['cmc'] = calculate_mana_value(parsed_face['mana_cost'])
        parsed_faces.append(parsed_face)
    return parsed_faces

def keep_card_fields(card, fields_to_keep=GAMEPLAY_FIELDS+EXTRA_FIELDS):
    return {k: v for k,v in card.items() if k in fields_to_keep}

def calculate_mana_value(cost_string):
    cost_string = cost_string.upper().replace("\\", "/")
    symbols = re.findall(MANA_SYMBOL_REGEX, cost_string)
    cmc = .0
    for symbol in symbols:
        # X in the cost adds 0 to the CMC
        if symbol != 'X' and symbol in LETTERS_MANA_SYMBOL:
            cmc += 1
        # If it is not a hybrid mana pip and it isn't a letter, then it must be a number
        if '/' not in symbol and symbol not in LETTERS_MANA_SYMBOL:
            cmc += float(symbol)
        if '/' in symbol:
            cmc += __parse_hybrid_mana_symbol_value(symbol)
    return cmc

def __parse_hybrid_mana_symbol_value(symbol):
    s1, s2 = symbol.split("/")
    m = min(s1, s2)
    if m == 'X':
        return 0
    if m in LETTERS_MANA_SYMBOL:
        return 1
    return float(m)
     
def extract_types(type_line):
    if TYPE_LINE_SEPARATOR in type_line:
        supertypes, subtypes = type_line.split(TYPE_LINE_SEPARATOR)
        return supertypes.split(), subtypes.split()
    return type_line.split(), []