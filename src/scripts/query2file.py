from mtgstats.scryfall import api
from mtgstats.cards import parse_cards
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument(
    '--query',
    required=True,
    action = 'store',
    dest = 'query',
    type=str
)

parser.add_argument(
    '--output-file',
    required=False,
    default="query.json",
)

parser.add_argument(
    '--limit',
    required=False,
    default=None,
    type=int,
)

args = parser.parse_args()

query_result = api.search(args.query, limit=args.limit)

parsed_cards = parse_cards(query_result)

with open(args.output_file, 'w') as output:
    json.dump(parsed_cards, output)