from pandas import Series
from mtgstats.cards import extract_types

"""
Takes a list of cards and compute frequency and cumulative sum arrays for it
"""
def cmc_analysis(cards, normalize_cumsum = False):
    cmcs = map(lambda x:x['cmc'], cards)
    series = Series(cmcs).value_counts().sort_index()
    cumsum = series.cumsum()
    if normalize_cumsum:
        cumsum /= len(cards)
    return series.to_dict(), cumsum.to_dict()


def color_analysis(cards, colors="WUBRGC"):
    counts = {
        c: 0 for c in colors
    }

    for card in cards:
        try:
            if len(card['colors']) == 0 and 'C' in colors:
                counts['C'] += 1
            for color in colors:
                if color in card['colors']:
                    counts[color] += 1
        except:
            print(card['name'])
    return counts

def subtype_analysis(cards):
    result = {}

    for card in cards:
        supertypes, subtypes = extract_types(card['type_line'])
        for subtype in subtypes:
            subtype_count = result.get(subtype, 0)
            result[subtype] = subtype_count + 1
    return result