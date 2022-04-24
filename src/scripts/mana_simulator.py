from random import shuffle

class Player():

    def __init__(self):
        pass

    def play_turn(self, hand, target, available_colors, remaining_turns):
        missing_colors = []
        for i, (available, t) in enumerate(zip(available_colors, target[:-1])):
            if available < t:
                missing_colors.append(i)

        if len(missing_colors) == 0:
            # No colors, missing, just find any land, preferably one that comes into play untapped
            candidates = list(filter(lambda l:not l['enters_tapped'] and not l.get('is_spell', False), hand))
        else:
            for color in missing_colors:
                candidates = list(filter(lambda l: l['colors'][color] > 0, hand))
                if len(candidates) > 0:
                    break
        if len(candidates) == 0:
            return False

        return candidates[0]

class Simulator():

    def __init__(self, deck, target):
        self.deck = deck
        self.target = target
        self.player = Player()

    def run_simulation(self, rounds):
        s = sum([self.simulate_round() for _ in range(rounds)])
        return s/rounds

    def simulate_round(self):
        available_colors = [0,0,0,0,0]
        lands_in_play = []
        turns = sum(self.target)
        # Copy and shuffle deck
        current_deck = self.deck[:]
        shuffle(current_deck)
        # Draw hand
        hand = [current_deck.pop() for _ in range(7)]
        while turns > 0:
            # Untap tapped lands
            for land in lands_in_play:
                land['is_tapped'] = False

            # Update Available Colors
            available_colors = self.compute_available_colors(lands_in_play)

            # Draw a card
            hand.append(current_deck.pop())

            # Let player choose a land to play
            land_to_play = self.player.play_turn(hand, self.target, available_colors, turns)

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
        for available, target in zip(available_colors, self.target[:-1]):
            if available < target:
                # Already missing a color
                return 0
        return 1. if sum(available_colors) >= sum(self.target) else 0

    def compute_available_colors(self, lands_in_play):
        colors = [0,0,0,0,0]
        for land in lands_in_play:
            if land.get('is_tapped', False):
                continue
            for i, c in enumerate(land.get('colors', [])):
                colors[i] += c
        return colors

def create_land(colors, enters_tapped):
    return {
        'colors': colors,
        'enters_tapped': enters_tapped
    }

# Color arrays is (red, green, blue, black, white)
def Mountain():
    return create_land((1,0,0,0,0), False)

def Forest():
    return create_land((0,1,0,0,0), False)

def Island():
    return create_land((0,0,1,0,0), False)

def Swamp():
    return create_land((0,0,0,1,0), False)

def Plains():
    return create_land((0,0,0,0,1), False)

def Spell():
    card = create_land((0,0,0,0,0), False)
    card['is_spell'] = True
    return card

def main():
    deck = [Mountain() for _ in range(18)]
    deck.extend([Forest() for _ in range(18)])
    deck.extend([Spell() for _ in range(63)])

    simulator = Simulator(deck, (1,1,0,0,0,1))
    #print(simulator.simulate_round())

    print(f"{simulator.run_simulation(1000):.2%}")

if __name__ == '__main__':
    main()