import unittest
from unittest.mock import patch
import VehicleCalculations
import datetime
import time
import TrafficLightSimulation

class TestTrafficLightSimulation(unittest.TestCase):

    # Test that green light changes to red after cycle time
    def test_green_light_changes_to_red(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = []
        timeSinceLastChange = 11
        TrafficLightSimulation.green_light = True
        expected = False
        actual = TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        self.assertEqual(expected, TrafficLightSimulation.green_light)

    # Test that red light changes to green after cycle time
    def test_red_light_changes_to_green(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = []
        timeSinceLastChange = 11
        TrafficLightSimulation.green_light = False
        expected = True
        actual = TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        self.assertEqual(expected, TrafficLightSimulation.green_light)

    # Test that acceleration is invoked for vehicles in front of the traffic light when it is green
    def test_acceleration_is_invoked_when_green(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = [{"road": "Main St", "position": 8, "acceleration": 0},
                    {"road": "Main St", "position": 12, "acceleration": 0}]
        timeSinceLastChange = 5
        TrafficLightSimulation.green_light = True
        expected_vehicles = [{"road": "Main St", "position": 8, "acceleration": VehicleCalculations.maxAcceleration},
                             {"road": "Main St", "position": 12, "acceleration": VehicleCalculations.maxAcceleration}]
        actual_vehicles = TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        self.assertEqual(expected_vehicles, actual_vehicles)

    # Test that vehicles within deceleration distance slow down when light turns red
    def test_vehicles_within_deceleration_distance_slow_down_when_red(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = [{"road": "Main St", "position": 6, "acceleration": 0},
                    {"road": "Main St", "position": 10, "acceleration": 0},
                    {"road": "Main St", "position": 14, "acceleration": 0}]
        timeSinceLastChange = 11
        TrafficLightSimulation.green_light = False
        expected_vehicles = [{"road": "Main St", "position": 6, "acceleration": VehicleCalculations.maxAcceleration},
                             {"road": "Main St", "position": 10, "acceleration": VehicleCalculations.maxAcceleration/2},
                             {"road": "Main St", "position": 14, "acceleration": 0}]
        actual_vehicles = TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        self.assertEqual(expected_vehicles, actual_vehicles)

if __name__ == '__main__':
    unittest.main()
