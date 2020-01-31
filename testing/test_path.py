import unittest

from modules.Path import *
from modules.World import Farm


class PathTest(unittest.TestCase):
    def setUp(self):
        self.path_planner = Planner(Farm())
        self.path_a_north = deque(["FAR 18", "FAR 17", "FAR 16", "FAR 15", "FAR 14", "FAR 13",
                                   "FAR 12", "FAR 11", "FAR 10", "FAR 9", "FAR 8", "FAR 7", "FAR 6",
                                   "FAR 5", "FAR 4", "FAR 3", "FAR 2", "FAR 1", "FAR 0"])
        self.path_a_south = self.path_a_north.copy()
        self.path_a_south.reverse()
        self.path_a_south.popleft()
        self.path_a_south.append("FAR 19")
        self.path_b_north = deque(["FBR 18", "FBR 17", "FBR 16", "FBR 15", "FBR 14", "FBR 13",
                                   "FBR 12", "FBR 11", "FBR 10", "FBR 9", "FBR 8", "FBR 7", "FBR 6",
                                   "FBR 5", "FBR 4", "FBR 3", "FBR 2", "FBR 1", "FBR 0"])
        self.path_b_south = self.path_b_north.copy()
        self.path_b_south.reverse()
        self.path_b_south.popleft()
        self.path_b_south.append("FBR 19")
        self.path_a_south_to_charger = deque(["FAR 19", "PTH05 9", "PTH05 8", "PTH05 7", "PTH05 6",
                                              "PTH05 5", "PTH05 4", "PTH05 3", "PTH05 2", "PTH05 1",
                                              "PTH05 0", "PTH00 9", "PTH00 8", "PTH00 7", "PTH00 6",
                                              "PTH00 5", "PTH00 4", "PTH00 3", "PTH00 2", "PTH00 1",
                                              "PTH00 0"])
        self.path_charger_to_a_south = self.path_a_south_to_charger.copy()
        self.path_charger_to_a_south.reverse()
        self.path_charger_to_a_south.popleft()
        self.path_charger_to_a_south.append("FAR 18")
        self.path_a_north_to_charger = deque(["PTH03 9", "PTH03 8", "PTH03 7", "PTH03 6",
                                              "PTH03 5", "PTH03 4", "PTH03 3", "PTH03 2", "PTH03 1",
                                              "PTH03 0", "PTH00 9", "PTH00 8", "PTH00 7", "PTH00 6",
                                              "PTH00 5", "PTH00 4", "PTH00 3", "PTH00 2", "PTH00 1",
                                              "PTH00 0"])
        self.path_charger_to_a_north = self.path_a_north_to_charger.copy()
        self.path_charger_to_a_north.reverse()
        self.path_charger_to_a_north.popleft()
        self.path_charger_to_a_north.append("FAR 0")
        self.path_b_south_to_charger = deque(["FBR 19", "PTH04 9", "PTH04 8", "PTH04 7", "PTH04 6",
                                              "PTH04 5", "PTH04 4", "PTH04 3", "PTH04 2", "PTH04 1",
                                              "PTH04 0"])
        self.path_charger_to_b_south = self.path_b_south_to_charger.copy()
        self.path_charger_to_b_south.reverse()
        self.path_charger_to_b_south.popleft()
        self.path_charger_to_b_south.append("FBR 18")
        self.path_b_north_to_charger = deque(["FBR 0", "PTH01 9", "PTH01 8", "PTH01 7", "PTH01 6",
                                              "PTH01 5", "PTH01 4", "PTH01 3", "PTH01 2", "PTH01 1",
                                              "PTH01 0"])
        self.path_charger_to_b_north = self.path_b_north_to_charger.copy()
        self.path_charger_to_b_north.reverse()
        self.path_charger_to_b_north.popleft()
        self.path_charger_to_b_north.append("FBR 1")

    def test_path_within_field_a(self):
        path_north = self.path_planner.find_path(set_locations("FAR19", "FAR0"))
        self.assertEqual(len(path_north), len(self.path_a_north))
        for i in range(len(path_north)):
            self.assertEqual(path_north.popleft(), self.path_a_north.popleft())
        path_south = self.path_planner.find_path(set_locations("FAR0", "FAR19"))
        self.assertEqual(len(path_south), len(self.path_a_south))
        for i in range(len(path_south)):
            self.assertEqual(path_south.popleft(), self.path_a_south.popleft())

    def test_path_within_field_b(self):
        path_north = self.path_planner.find_path(set_locations("FBR19", "FBR0"))
        self.assertEqual(len(path_north), len(self.path_b_north))
        for i in range(len(path_north)):
            self.assertEqual(path_north.popleft(), self.path_b_north.popleft())
        path_south = self.path_planner.find_path(set_locations("FBR0", "FBR19"))
        self.assertEqual(len(path_south), len(self.path_b_south))
        for i in range(len(path_south)):
            self.assertEqual(path_south.popleft(), self.path_b_south.popleft())

    def test_field_a_to_charger(self):
        path_a_south_to_chgr = self.path_planner.find_path(set_locations("FAR18", "Charger"))
        self.assertEqual(len(path_a_south_to_chgr), len(self.path_a_south_to_charger))
        for i in range(len(path_a_south_to_chgr)):
            self.assertEqual(path_a_south_to_chgr.popleft(), self.path_a_south_to_charger.popleft(),
                             "They are not equal")

        path_a_north_to_chgr = self.path_planner.find_path(set_locations("FAR0", "Charger"))
        self.assertEqual(len(path_a_north_to_chgr), len(self.path_a_north_to_charger), "the sizes are not same")
        for i in range(len(path_a_north_to_chgr)):
            self.assertEqual(path_a_north_to_chgr.popleft(), self.path_a_north_to_charger.popleft())

        path_chgr_to_a_south = self.path_planner.find_path(set_locations("Charger", "FAR18"))
        self.assertEqual(len(path_chgr_to_a_south), len(self.path_charger_to_a_south))
        for i in range(len(path_chgr_to_a_south)):
            self.assertEqual(path_chgr_to_a_south.popleft(), self.path_charger_to_a_south.popleft())

        path_chgr_to_a_north = self.path_planner.find_path(set_locations("Charger", "FAR0"))
        self.assertEqual(len(path_chgr_to_a_north), len(self.path_charger_to_a_north))
        for i in range(len(path_chgr_to_a_north)):
            self.assertEqual(path_chgr_to_a_north.popleft(), self.path_charger_to_a_north.popleft())

    def test_field_b_to_charger(self):
        path_b_south_to_chgr = self.path_planner.find_path(set_locations("FBR18", "Charger"))
        self.assertEqual(len(path_b_south_to_chgr), len(self.path_b_south_to_charger), "FBR18 to Charger failed")
        for i in range(len(path_b_south_to_chgr)):
            self.assertEqual(path_b_south_to_chgr.popleft(), self.path_b_south_to_charger.popleft())
        path_b_north_to_chgr = self.path_planner.find_path(set_locations("FBR1", "Charger"))
        self.assertEqual(len(path_b_north_to_chgr), len(self.path_b_north_to_charger), "FBR1 to Charger failed")
        for i in range(len(path_b_north_to_chgr)):
            self.assertEqual(path_b_north_to_chgr.popleft(), self.path_b_north_to_charger.popleft())

        path_chgr_to_b_south = self.path_planner.find_path(set_locations("Charger", "FBR18"))
        self.assertEqual(len(path_chgr_to_b_south), len(self.path_charger_to_b_south), "Charger to FBR18 failed")
        for i in range(len(path_chgr_to_b_south)):
            self.assertEqual(path_chgr_to_b_south.popleft(), self.path_charger_to_b_south.popleft())
        path_chgr_to_b_north = self.path_planner.find_path(set_locations("Charger", "FBR1"))
        self.assertEqual(len(path_chgr_to_b_north), len(self.path_charger_to_b_north), "Charger to FBR1 failed")
        for i in range(len(path_chgr_to_b_north)):
            self.assertEqual(path_chgr_to_b_north.popleft(), self.path_charger_to_b_north.popleft())


if __name__ == '__main__':
    unittest.main()
