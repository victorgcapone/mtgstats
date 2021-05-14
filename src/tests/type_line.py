from unittest import TestCase
from mtgstats.cards import extract_types, TYPE_LINE_SEPARATOR
import json

class TypeLineTest(TestCase):

    def test_single_supertype(self):
        type_line = "Artifact"
        St, st = extract_types(type_line)
        self.assertEqual(St, ["Artifact"])
        self.assertEqual(st, [])

    def test_supertype_subtype(self):
        type_line = f"Creature {TYPE_LINE_SEPARATOR} Shaman"
        St, st = extract_types(type_line)
        self.assertEqual(St, ["Creature"])
        self.assertEqual(st, ["Shaman"])

    def test_multiple_supertypes(self):
        type_line = "Legendary Artifact"
        St, st = extract_types(type_line)
        self.assertEqual(St, ["Legendary", "Artifact"])

    def test_multiple_subtype(self):
        type_line = f"Creature {TYPE_LINE_SEPARATOR} Snake Shaman"
        St, st = extract_types(type_line)
        self.assertEqual(St, ["Creature"])
        self.assertEqual(st, ["Snake", "Shaman"])

    def test_multiple_super_subtypes(self):
        type_line = f"Legendary Creature {TYPE_LINE_SEPARATOR} Elf Warrior"
        St, st = extract_types(type_line)
        self.assertEqual(St, ["Legendary", "Creature"])
        self.assertEqual(st, ["Elf", "Warrior"])