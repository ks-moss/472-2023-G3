import src.SimulationIntersection as func
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

# test for Class IntersectionSim
class TestIntersectionSim(unittest.TestCase):

    def setUp(self):
        # Create sample data for testing
        self.intersections_data = [
            [{"road": "A", "position": 10}, {"road": "B", "position": 20}],  # Intersection 1
            [{"road": "C", "position": 30}, {"road": "D", "position": 40}]   # Intersection 2
        ]
        self.roads_data = ["A", "B", "C", "D"]
        self.trafficLight_data = [
            {"road": "A", "position": 15},  # Traffic light for intersection 1, road A
            {"road": "B", "position": 25},  # Traffic light for intersection 1, road B
            {"road": "C", "position": 35},  # Traffic light for intersection 2, road C
            {"road": "D", "position": 45}   # Traffic light for intersection 2, road D
        ]
        self.intersection_sim = func.IntersectionSim(self.intersections_data, self.roads_data, self.trafficLight_data)

    def test_is_approaching_N_selected_road(self):
        # Test case 1: Vehicle is not approaching the selected road
        vehicle_road = "A"
        vehicle_position = 5
        expected_output = (vehicle_road, vehicle_position)
        self.assertEqual(self.intersection_sim.is_approaching_N_selected_road(vehicle_road, vehicle_position), expected_output)

        # Test case 2: Vehicle is approaching the selected road, but doesn't make a turn
        vehicle_road = "A"
        vehicle_position = 16
        expected_output = (vehicle_road, vehicle_position)
        self.assertEqual(self.intersection_sim.is_approaching_N_selected_road(vehicle_road, vehicle_position), expected_output)

        # Test case 3: Vehicle is approaching the selected road and makes a turn
        vehicle_road = "A"
        vehicle_position = 26
        expected_output = ("B", 35)
        self.assertEqual(self.intersection_sim.is_approaching_N_selected_road(vehicle_road, vehicle_position), expected_output)

    def test_update(self):
        # Test case for update method
        self.assertIsNone(self.intersection_sim.update())

if __name__ == '__main__':
    unittest.main()