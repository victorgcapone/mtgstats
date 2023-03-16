from distutils.log import INFO
from random import shuffle
from tqdm import tqdm
import numpy as np

import logging


class Player():

    def __init__(self):
        pass

    def play_turn(self, hand, target, available_colors, remaining_turns):
        missing_colors = []
        for i, (available, t) in enumerate(zip(available_colors, target[:-1])):
            if available < t:
                missing_colors.append(i)

        lands_in_hand = [l for l in hand if not l.get('is_spell', False)]

        logging.info(f"Lands in hand: {lands_in_hand}")

        if not lands_in_hand:
            # No lands in hand, just pass turn
            return False

        etb_untapped = [land for land in lands_in_hand if not land['enters_tapped']]
        etb_tapped   = [land for land in lands_in_hand if land['enters_tapped']]
        candidates = []
        if len(missing_colors) > 0:
            # Colors missing
            for color in missing_colors:
                logging.info(f"Color: {color}")
                # Try to find a land that generates a missing color
                colored = [land for land in lands_in_hand if land['colors'][color] > 0]

                if not colored:
                    # No Colored lands for that color, continue iteration
                    candidates = []
                    continue

                if remaining_turns == 1:
                    # If this is the last turn we have we would rather play an untapped land
                    # Note that if we have no untapped lands at the end of the last turn
                    # and we haven't met the target yet, we already failed, so it doesn't matter
                    candidates = [l for l in colored if not l['enters_tapped']]
                else:
                    # Otherwise, it is best to play a tapped land if we can
                    tapped = [l for l in colored if l['enters_tapped']]
                    if not tapped:
                        # If we don't have any tapped colored land, just play any colored land
                        candidates = colored
                if len(candidates) > 0:
                    break

        if len(missing_colors) == 0 or len(candidates) == 0:
            # No colors missing we or we couldn't find any land for the missing colors
            # We can play any land we like 
            logging.info("No colors missing")
            if remaining_turns == 1:
                # It is last turn just find any land that comes into play untapped
                candidates = etb_untapped
            else:
                # We have more turns, play an untapped land first
                candidates = etb_tapped
            
            if not candidates:
                # We couldn't find a suitable land, just play any
                candidates = lands_in_hand

        if len(candidates) == 0:
            return False

        return candidates[0]

class ManaCurveSimulator():

    def __init__(self, deck):
        self.deck = deck
        self.player = Player()

    def run_simulation(self, target, rounds):
        results = []
        for _ in tqdm(range(rounds)):
            results.append(self.simulate_round(target))
        s = sum(results)
        return s/rounds

    def simulate_round(self, target):
        logging.info('Starting Round')
        available_colors = [0,0,0,0,0]
        lands_in_play = []
        turns = sum(target)
        # Copy and shuffle deck
        current_deck = self.deck[:]
        shuffle(current_deck)
        # Draw hand
        hand = [current_deck.pop() for _ in range(7)]
        logging.info(f"Starting hand {hand}")
        while turns > 0:
            logging.info(f"Turns Remaining: {turns}, Lands in Play: {len(lands_in_play)}")
            # Untap tapped lands
            for land in lands_in_play:
                land['is_tapped'] = False

            # Update Available Colors
            available_colors = self.compute_available_colors(lands_in_play)

            # Draw a card
            hand.append(current_deck.pop())

            # Let player choose a land to play
            land_to_play = self.player.play_turn(hand, target, available_colors, turns)

            logging.info(f"Land to play: {land_to_play}")
            if land_to_play:
                hand.remove(land_to_play)
                if land_to_play.get('enters_tapped', False):
                    land_to_play['is_tapped'] = True
                lands_in_play.append(land_to_play)

            turns -= 1

        # Update Available Colors
        available_colors = self.compute_available_colors(lands_in_play)
        # Check if we have all the colors, discard last index of target as it represents
        # generic mana
        for available, target_color in zip(available_colors, target[:-1]):
            if available < target_color:
                # Already missing a color
                return 0
        if len(list(filter(lambda x:not x.get('is_tapped', False), lands_in_play))) >= sum(target):
            return 1
        else:
            return 0

    def compute_available_colors(self, lands_in_play):
        colors = [0,0,0,0,0]
        for land in lands_in_play:
            if land.get('is_tapped', False):
                continue
            for i, c in enumerate(land.get('colors', [])):
                colors[i] += c
        logging.info(f"Available colors: {colors}")
        return colors

def create_card(colors, enters_tapped):
    return {
        'colors': colors,
        'enters_tapped': enters_tapped
    }

def random_spell(colors, max_cmc):
    spell = create_card(colors, False)
    r = np.random.randint(1, 3, size=len(colors))
    spell['cost'] = colors * r
    cmc = sum(spell['cost'])
    for _ in range(cmc-max_cmc):
        idx = np.argmax(spell['cost'])
        spell['cost'][idx] -= 1
    spell['is_spell'] = True
    return spell
    

# Color arrays is (red, green, blue, black, white)
def Mountain():
    return create_card((1,0,0,0,0), False)

def Forest():
    return create_card((0,1,0,0,0), False)

def Island():
    return create_card((0,0,1,0,0), False)

def Swamp():
    return create_card((0,0,0,1,0), False)

def Plains():
    return create_card((0,0,0,0,1), False)

def Spell():
    card = create_card((0,0,0,0,0), False)
    card['is_spell'] = True
    return card


def main():
    deck = []
    deck.extend([Mountain() for _ in range(15)])
    deck.extend([Forest() for _ in range(15)])
    deck.extend([create_card((1,1,0,0,0), True) for _ in range(6)])
    deck.extend([Spell() for _ in range(63)])

    simulator = ManaCurveSimulator(deck)

    print(f"{simulator.run_simulation((1,1,0,0,0,0), 10000):.2%}")

if __name__ == '__main__':
    main()