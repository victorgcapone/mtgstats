import matplotlib.pyplot as plt
from mtgstats.analysis import cmc_analysis, color_analysis
import pandas as pd

def cmc_distribution(cards, ax=None):
    dist, cumsum = cmc_analysis(cards, normalize_cumsum=True)

    if ax == None:
        fig, ax = plt.subplots(figsize = (10,4));

        ax.set(
            title='CMC Distribution',
            xlabel = 'CMC',
            ylabel = 'Freq.',
            xticks = list(dist.keys())
        )
    else:
        fig = ax.figure

    cumsum_ax = ax.twinx()
    cumsum_ax.set(
        ylabel = '% cum sum'
    )

    ax.bar(dist.keys(), dist.values())
    cumsum_ax.plot(cumsum.keys(), cumsum.values(), c='salmon', label='Cum. Sum.')
    fig.tight_layout()
    plt.close()
    return fig

def color_distribution(cards, ax = None):
    colors = color_analysis(cards)
    colors_freq = pd.Series(colors)
    colors_freq = colors_freq.sort_values(ascending=False)
    
    if ax == None:
        fig, ax = plt.subplots(figsize=(10,4))
      
        ax.set(
            title='Amount of cards for each color',
            xlabel='Color',
            ylabel='Amount of cards'
        )
    else:
        fig = ax.figure

    ax.bar(colors_freq.index, colors_freq)

    # he cumulative sum will exceed the total number of cards if there are multicolored cards
    # as they count for all of their colors
    cumsum_ax = ax.twinx()
    cumsum_ax.set(
        ylabel = 'Cum. Sum.'
    )
    cumsum_ax.plot(colors_freq.cumsum(), c='salmon')

    fig.tight_layout()
    plt.close()
    return fig

def not_in_color_distribution(cards, ax = None):
    colors = color_analysis(cards)
    colors_freq = pd.Series(colors)
    colors_freq = colors_freq.sort_values(ascending=False)
    
    # The number of cards not of each color is the total minus the amount of creatures in that color
    not_in_color = (len(cards) - colors_freq).sort_values(ascending=False)

    if ax == None:
        fig, ax = plt.subplots(figsize = (10,4))

        ax.set(
            title = 'Amount of cards NOT in each color',
            xlabel='Color',
            ylabel='Amount of cards',
            ylim=(min(not_in_color) - len(cards)/2,len(cards))
        )
    else:
        fig = ax.figure

    ax.bar(not_in_color.index, not_in_color)
    cumsum_ax = ax.twinx()
    cumsum_ax.set(
        ylabel = 'Cum. Sum.'
    )
    cumsum_ax.plot(colors_freq.cumsum(), c='salmon')
    
    fig.tight_layout()
    plt.close()
    return fig
