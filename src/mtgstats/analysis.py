from collections import defaultdict
from email.policy import default
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

def partition(cards, field):
    partitions = defaultdict(list)

    for card in cards:
        p = card[field]
        partitions[p].append(card)

    return partitions

def poh_analysis(cards):
    partitions = partition(cards, 'cmc')
    maximum_edges = 0
    total_edges = 0
    graph = {}
    
    for cmc, p in partitions.items():
        next_cmc = cmc + 1
        next_partition = partitions.get(next_cmc, [])
        
        # The maximum number of edges is the sum of products of the partition sizes
        # ie: every creature in a partition can fetch every crature in the next
        maximum_edges += len(p) * len(next_partition)


        for card in p:
            graph[card['name']] = []
            edges = find_pyre_edges(card, next_partition)
            total_edges += len(edges)
            for s, _, t in edges:
                    graph[s].append(t)


    return graph, total_edges, maximum_edges

def find_pyre_edges(card, other_cards):
    edges = []
    _, subtypes = extract_types(card['type_line'])

    for other_card in other_cards:
        _, other_subtypes = extract_types(other_card['type_line'])
        common_types = set(subtypes).intersection(set(other_subtypes))
        if common_types:
            edges.append((card['name'], list(common_types), other_card['name']))
        else:
            if 'Changeling' in card['keywords']:
                edges.append((card['name'], other_subtypes, other_card['name']))
            elif 'Changeling' in other_card['keywords']:
                edges.append((card['name'], subtypes, other_card['name']))

    return edges

def poh_all_chains(graph):
    cache = {}
    result = {}
    for card in graph.keys():
        card_chains = poh_all_chains_from(graph, card, cache)
        result[card] = card_chains

    return result

def poh_all_chains_from(graph, start, cache = None):
    chains = []
    neighbors = graph[start]
    if cache is None:
        cache = {}
    for n in neighbors:
        if cache and n in cache:
            n_chains = cache[n]
        else:
            n_chains = poh_all_chains_from(graph, n, cache)
            cache[n] = n_chains
        if len(n_chains) == 0:
            chains.append([start, n])
        for c in n_chains:
            chains.append([start] + c)
    return chains

def poh_chain(graph, start, end):
    labels = list(graph.keys())
    start_idx = labels.index(start)
    stack = [start_idx]
    path = [-1] * len(labels)
    while len(stack) > 0:
        current = stack.pop()
        adj = graph.get(labels[current], [])
        for neighbor in adj:
            n_index = labels.index(neighbor)
            if neighbor not in stack and path[n_index] == -1:
                path[n_index] = current
                stack.append(n_index)
    
    current_idx = labels.index(end)
    start_idx = labels.index(start)
    result = []
    while path[current_idx] > -1:
        result.insert(0, labels[current_idx])
        current_idx = path[current_idx]
    
    if current_idx == start_idx:
        result.insert(0, labels[start_idx])
        return result
    return []

