import SimulationIntersection as func
import unittest
import random

class TestTurnVehiclesAtIntersection(unittest.TestCase):
    
    # Tests if a vehicle does not turn
    def test_vehicle_does_not_turn(self):
        intersection_list = [{"road": "A", "position": 0}, {"road": "B", "position": 5}]
        vehicles_list = [{"road": "A", "position": 2}, {"road": "B", "position": 7}]
        random.seed(42)
        func.turnVehiclesAtIntersection(intersection_list, 0, vehicles_list)
        self.assertListEqual(vehicles_list, [{"road": "A", "position": 2}, {"road": "B", "position": 7}])

    # Tests vehicle going from road A to B    
    def test_vehicle_turns_from_road_A_to_B(self):
        intersection_list = [{"road": "A", "position": 0}, {"road": "B", "position": 5}]
        vehicles_list = [{"road": "A", "position": 4}, {"road": "B", "position": 7}]
        random.seed(42)
        func.turnVehiclesAtIntersection(intersection_list, 0, vehicles_list)
        self.assertListEqual(vehicles_list, [{"road": "B", "position": 6}, {"road": "B", "position": 7}])

    # Tests vehicle going from road B to A 
    def test_vehicle_turns_from_road_B_to_A(self):
        intersection_list = [{"road": "A", "position": 0}, {"road": "B", "position": 5}]
        vehicles_list = [{"road": "A", "position": 7}, {"road": "B", "position": 2}]
        random.seed(42)
        func.turnVehiclesAtIntersection(intersection_list, 1, vehicles_list)
        self.assertListEqual(vehicles_list, [{"road": "A", "position": 1}, {"road": "A", "position": 1}])

unittest.main()