import unittest
from unittest.mock import patch
from src import VehicleCalculations
from src import TrafficLightSimulation


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
    def test_green_light_changes_to_yellow(self):
        trafficLight = [{"road": "Main St", "position": 10, "cycle": 10}]
        cycleTimeCalc = trafficLight[0]["cycle"]/1.5
        lightStates = [{"color": "green", "counter": cycleTimeCalc}]
        vehicles = []
        expected_light = "yellow"
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, 0, lightStates)
        error_msg = "Error: Green light did not change to yellow!"
        self.assertEqual(expected_light, lightStates[0]["color"], error_msg)
    
    # Test that green light stays green if cycle time is less than timeSinceLastChange
    def test_green_light_stays_green(self):
        trafficLight = [{"road": "Main St", "position": 10, "cycle": 10}]
        cycleTimeCalc = (trafficLight[0]["cycle"]/1.5) - 1
        lightStates = [{"color": "green", "counter": cycleTimeCalc}]
        vehicles = []
        expected_light = "green"
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, 0, lightStates)
        error_msg = "Error: Green light did not stay on green!"
        self.assertEqual(expected_light, lightStates[0]["color"], error_msg)


    # Test that red light changes to green after cycle time
    def test_red_light_changes_to_green(self):
        trafficLight = [{"road": "Main St", "position": 10, "cycle": 10}]
        cycleTimeCalc = trafficLight[0]["cycle"]+1
        lightStates = [{"color": "red", "counter": cycleTimeCalc}]
        vehicles = []
        expected_light = "green"
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, 0, lightStates)
        error_msg = "Error: Red light did not change to green!"
        self.assertEqual(expected_light, lightStates[0]["color"], error_msg)

    # Test that red light stays red if cycle time is less than timeSinceLastChange
    def test_red_light_stays_red(self):
        trafficLight = [{"road": "Main St", "position": 10, "cycle": 10}]
        cycleTimeCalc = trafficLight[0]["cycle"]-1
        lightStates = [{"color": "red", "counter": cycleTimeCalc}]
        vehicles = []
        expected_light = "red"
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, 0, lightStates)
        error_msg = "Error: Red light did not change to green!"
        self.assertEqual(expected_light, lightStates[0]["color"], error_msg)


    # Test that acceleration is invoked for vehicles in front of the traffic light when it is green
    def test_acceleration_is_invoked_when_green(self):
        trafficLight = [{"road": "Main St", "position": 10, "cycle": 10}]
        vehicles = [{"road": "Main St", "position": 8, "speed": 0,"acceleration": 0},
                    {"road": "Main St", "position": 4, "speed": 0,"acceleration": 0}]
        cycleTimeCalc = trafficLight[0]["cycle"]+1
        lightStates = [{"color": "red", "counter": cycleTimeCalc}]
        expected_vehicles = [{"road": "Main St", "position": 8, "speed": 8, "acceleration": 2},
                             {"road": "Main St", "position": 4, "speed": 8, "acceleration": 2}]
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, 0, lightStates)
        error_msg = "Error: Acceleration was not adjusted for vehicles in front of the green light!"
        self.assertEqual(expected_vehicles, vehicles, error_msg)

    # Test that vehicles within deceleration distance slow down when light turns red
    def test_vehicles_within_deceleration_distance_slow_down_when_red(self):
        trafficLight = [{"road": "Main St", "position": 10, "cycle": 10}]
        vehicles = [{"road": "Main St", "position": 4, "speed": 8, "acceleration": 2, "type": "car"},
                    {"road": "Main St", "position": 1, "speed": 8, "acceleration": 2, "type": "car"}]
        cycleTimeCalc = trafficLight[0]["cycle"]+1
        lightStates = [{"color": "yellow", "counter": cycleTimeCalc}]
        expected_vehicles = [{"road": "Main St", "position": 4, "speed": 8, "acceleration": -0.4443373493975904, "type": "car"},
                             {"road": "Main St", "position": 1, "speed": 8, "acceleration": -0.4443373493975904, "type": "car"}]
        TrafficLightSimulation.trafficLightInteraction(trafficLight, vehicles, 0, lightStates)
        error_msg = "Error: Deceleration calculations was not adjusted!"
        self.assertEqual(expected_vehicles, vehicles, error_msg) 

# Call all functions within this file for a test
if __name__ == '__main__':
    unittest.main()
