from unittest import TestCase
from mtgstats import cards

class ManaValueTest(TestCase):

    def test_no_mana_cost(self):
        self.assertEqual(cards.calculate_mana_value(''),0)

    def test_simple_cmc(self):
        self.assertEqual(cards.calculate_mana_value('{1}{r}'), 2)

    def test_hybrid_cmc_no_generic(self):
        self.assertEqual(cards.calculate_mana_value('{r/w}{r/w}'), 2)

    def test_hybrid_cmc_generic(self):
        self.assertEqual(cards.calculate_mana_value('{2/b}{2/w}'), 4)

    def test_x_cmc(self):
        self.assertEqual(cards.calculate_mana_value('{x}{2}{u}'), 3)

    def test_ballista_cmc(self):
        self.assertEqual(cards.calculate_mana_value('{x}{x}'), 0)

    def test_complex_cmc(self):
        self.assertEqual(cards.calculate_mana_value('{x}{2/r}{u/r}{r}'), 4)
