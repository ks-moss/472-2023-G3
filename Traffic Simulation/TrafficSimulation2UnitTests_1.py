import TrafficSimulation2 as func
import unittest

class TestCheckLightState(unittest.TestCase):
    
    #Tests red light at at an even number
    def test_red_light_at_even_cycle_iteration(self):
        light = {
            "cycle": 10 # 10 seconds cycle
        }
        time = 20 # 2nd iteration of the cycle
        self.assertFalse(func.checkLightState(light, time))
        
    #Tests green light at at an odd number   
    def test_green_light_at_odd_cycle_iteration(self):
        light = {
            "cycle": 15 # 15 seconds cycle
        }
        time = 45 # 3rd iteration of the cycle
        self.assertTrue(func.checkLightState(light, time))
    
    #Tests light at at time 0
    def test_edge_case_zero_cycle_iteration(self):
        light = {
            "cycle": 5 # 5 seconds cycle
        }
        time = 0 # Starting time
        self.assertFalse(func.checkLightState(light, time))
        
    #Tests light at very long cycle
    def test_edge_case_infinite_cycle_iteration(self):
        light = {
            "cycle": 30 # 30 seconds cycle
        }
        time = 300 # 10 minutes, 20 iterations of the cycle
        self.assertFalse(func.checkLightState(light, time))

unittest.main()