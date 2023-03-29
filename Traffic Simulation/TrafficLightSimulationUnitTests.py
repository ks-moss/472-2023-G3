import unittest
from unittest.mock import patch
import VehicleCalculations
import TrafficLightSimulation


# Goal: Test each condition within the trafficLightInteraction method
# There are six total tests within this class:
#   1. Green light changes to red when cycle > timeSinceLastChange
#   2. Green light stays green when cycle < timeSinceLastChange
#   3. Red light changes to green when cycle > timeSinceLastChange
#   4. Red light stays red when cycle < timeSinceLastChange
#   5. When light is switched to green, all vehicles in front of the traffic light accelerate back up
#   6. When light is switched to red, all vehicles in front of the traffic


class TestTrafficLightSimulation(unittest.TestCase):

    # Test that green light changes to red after cycle time
    def test_green_light_changes_to_red(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = []
        timeSinceLastChange = 11
        TrafficLightSimulation.green_light = True
        expected_light = False
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        error_msg = "Error: Green light did not change to red!"
        self.assertEqual(expected_light, TrafficLightSimulation.green_light, error_msg)
    
    # Test that green light stays green if cycle time is less than timeSinceLastChange
    def test_green_light_stays_green(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = []
        timeSinceLastChange = 5
        TrafficLightSimulation.green_light = True
        expected_light = True
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        error_msg = "Error: Green light did not stay green!"
        self.assertEqual(expected_light, TrafficLightSimulation.green_light, error_msg)


    # Test that red light changes to green after cycle time
    def test_red_light_changes_to_green(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = []
        timeSinceLastChange = 11
        TrafficLightSimulation.green_light = False
        expected_light = True
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        error_msg = "Error: Red light did not change to green!"
        self.assertEqual(expected_light, TrafficLightSimulation.green_light, error_msg)

    # Test that red light stays red if cycle time is less than timeSinceLastChange
    def test_red_light_stays_red(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = []
        timeSinceLastChange = 5
        TrafficLightSimulation.green_light = False
        expected_light = False
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        error_msg = "Error: Red light did not stay red!"
        self.assertEqual(expected_light, TrafficLightSimulation.green_light, error_msg)


    # Test that acceleration is invoked for vehicles in front of the traffic light when it is green
    def test_acceleration_is_invoked_when_green(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = [{"road": "Main St", "position": 8, "acceleration": 0},
                    {"road": "Main St", "position": 4, "acceleration": 0}]
        timeSinceLastChange = 5
        TrafficLightSimulation.green_light = True
        expected_vehicles = [{"road": "Main St", "position": 8, "acceleration": VehicleCalculations.maxAcceleration},
                             {"road": "Main St", "position": 4, "acceleration": VehicleCalculations.maxAcceleration}]
        actual_vehicles = TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        error_msg = "Error: Acceleration was not adjusted for vehicles in front of the green light!"
        self.assertEqual(expected_vehicles, actual_vehicles, error_msg)

    # Test that vehicles within deceleration distance slow down when light turns red
    def test_vehicles_within_deceleration_distance_slow_down_when_red(self):
        trafficLight = {"road": "Main St", "position": 10, "cycle": 10}
        vehicles = [{"road": "Main St", "position": 10, "acceleration": 0},
                    {"road": "Main St", "position": 7, "acceleration": 0},
                    {"road": "Main St", "position": 3, "acceleration": 0}]
        timeSinceLastChange = 11
        TrafficLightSimulation.green_light = True
        expected_vehicles = [{"road": "Main St", "position": 10, "acceleration": VehicleCalculations.maxAcceleration},
                             {"road": "Main St", "position": 7, "acceleration": VehicleCalculations.maxAcceleration/2},
                             {"road": "Main St", "position": 3, "acceleration": 0}]
        actual_vehicles = TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, timeSinceLastChange)
        error_msg = "Error: Deceleration calculations was not adjusted!"
        self.assertEqual(expected_vehicles, actual_vehicles, error_msg)

# Call all functions within this file for a test
if __name__ == '__main__':
    unittest.main()
