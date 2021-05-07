from pandas import Series

"""
Takes a list of cards and compute frequency and cumulative sum arrays for it
"""
def cmc_analysis(cards):
    cmcs = map(lambda x:x['cmc'], cards)
    series = Series(cmcs).value_counts().sort_index()
    return series.to_dict(), series.cumsum().to_dict()
