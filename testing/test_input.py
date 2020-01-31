import unittest

from modules.Input import *


class CommandInputTest(unittest.TestCase):
    def setUp(self):
        self.field_a_locations = ["gOtOFieldAroW8",
                                  " go to  fieLDA RoW 18 ",
                                  "gOTOfield A rOW88"]
        self.field_b_locations = ["gOtOFieldBroW8",
                                  " go to  fieLDB RoW 18 ",
                                  "gOTOfield B rOW88"]
        self.charger_locations = ["gotocharGeR",
                                  "  goTo    cHaRgeR ",
                                  "    go toCHARGER  "]
        self.planting_locations = ["plantPotaToes inFieLDA rOW7",
                                   "  plANt caRRottsin fieldBRow 88"]

    def tearDown(self):
        self.field_a_locations = []
        self.field_b_locations = []
        self.charger_locations = []
        self.planting_locations = []

    def test_field_a_rows(self):
        self.assertEqual(user_input(self.field_a_locations[0])[0], "FAR8")
        self.assertEqual(user_input(self.field_a_locations[0])[1], "N/A")
        self.assertEqual(user_input(self.field_a_locations[1])[0], "FAR18")
        self.assertEqual(user_input(self.field_a_locations[1])[1], "N/A")
        self.assertEqual(user_input(self.field_a_locations[2])[0], "FAR88")
        self.assertEqual(user_input(self.field_a_locations[2])[1], "N/A")

    def test_field_b_rows(self):
        self.assertEqual(user_input(self.field_b_locations[0])[0], "FBR8")
        self.assertEqual(user_input(self.field_b_locations[0])[1], "N/A")
        self.assertEqual(user_input(self.field_b_locations[1])[0], "FBR18")
        self.assertEqual(user_input(self.field_b_locations[1])[1], "N/A")
        self.assertEqual(user_input(self.field_b_locations[2])[0], "FBR88")
        self.assertEqual(user_input(self.field_b_locations[2])[1], "N/A")

    def test_charger(self):
        self.assertEqual(user_input(self.charger_locations[0])[0], "Charger")
        self.assertEqual(user_input(self.charger_locations[0])[1], "N/A")
        self.assertEqual(user_input(self.charger_locations[1])[0], "Charger")
        self.assertEqual(user_input(self.charger_locations[1])[1], "N/A")
        self.assertEqual(user_input(self.charger_locations[2])[0], "Charger")
        self.assertEqual(user_input(self.charger_locations[2])[1], "N/A")

    def test_bad_input(self):
        self.assertEqual(user_input("")[0], "Invalid task")
        self.assertEqual(user_input("")[1], "N/A")
        self.assertEqual(user_input("fg73f37g")[0], "Invalid task")
        self.assertEqual(user_input("fg73f37g")[1], "N/A")

    def test_planting_instructions(self):
        self.assertEqual(user_input(self.planting_locations[0])[0], "FAR7")
        self.assertEqual(user_input(self.planting_locations[0])[1], "PotaToes")
        self.assertEqual(user_input(self.planting_locations[1])[0], "FBR88")
        self.assertEqual(user_input(self.planting_locations[1])[1], "caRRotts")


if __name__ == '__main__':
    unittest.main()
