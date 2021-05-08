import matplotlib.pyplot as plt
from mtgstats.analysis import cmc_analysis

def cmc_distribution(cards, ax=None):
    dist, cumsum = cmc_analysis(cards, normalize_cumsum=True)

    if ax == None:
        fig, ax = plt.subplots(figsize = (10,4));
    else:
        fig = ax.figure

    ax.set(
        title='CMC Distribution',
        xlabel = 'CMC',
        ylabel = 'Freq.',
        xticks = list(dist.keys())
    )

    cumsum_ax = ax.twinx()
    cumsum_ax.set(
        ylabel = '% cum sum'
    )

    ax.bar(dist.keys(), dist.values())
    cumsum_ax.plot(cumsum.keys(), cumsum.values(), c='salmon', label='Cum. Sum.')
    fig.legend(loc=(.1, .7))
    fig.tight_layout()
    plt.close()
    return fig

def color_distribution(cards, ax = None):
    colors = color_analysis(cards)
    colors_freq = pd.Series(colors)
    colors_freq = colors_freq.sort_values(ascending=False)
    
    if ax == None:
        fig, ax = plt.subplots( figsize=(10,4))
    else:
        fig = ax.figure
        
    ax.set(
        title='Amount of creatures for each color',
        xlabel='Color',
        ylabel='Amount of creatures'
    )

    # he cumulative sum will exceed the total number of cards if there are multicolored cards
    # as they count for all of their colors
    cumsum_ax = ax.twinx()
    cumsum_ax.plot(colors_freq.cumsum(), c='salmon')

    ax.bar(colors_freq.index, colors_freq)

    fig.tight_layout()
    plt.close()
    return fig

def not_in_color_distribution(cards, ax = None):
    colors = color_analysis(cards)
    colors_freq = pd.Series(colors)
    colors_freq = colors_freq.sort_values(ascending=False)
    
    if ax == None:
        fig, ax = plt.subplots(figsize = (10,4))
    else:
        fig = ax.figure

    # The number of cards not of each color is the total minus the amount of creatures in that color
    not_in_color = (len(data) - colors_freq).sort_values(ascending=False)

    ax.set(
        title = 'Amount of creatures NOT in each color',
        xlabel='Color',
        ylabel='Amount of creatures',
        ylim=(min(not_in_color) - len(data)/2,len(data))
    )

    ax.bar(not_in_color.index, not_in_color)
    cumsum_ax = ax.twinx()
    cumsum_ax.plot(colors_freq.cumsum(), c='salmon')
    
    fig.tight_layout()
    plt.close()
    return fig
