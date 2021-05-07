from pandas import Series

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
