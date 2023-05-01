from src import TrafficSimulation2 as func
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

class TestElement(unittest.TestCase):
    
    # Test element equals
    def test_correct_element_type(self):
        elem = func.Element(elementType="TRAFFIC LIGHT")
        self.assertEqual(elem.elementType, "TRAFFIC LIGHT")
        
    # Test element mismatch
    def test_invalid_element_type(self):
        with self.assertRaises(AssertionError):
            elem = func.Element(elementType="INVALID")
        
    # Testing adding attributes to elements
    def test_append_attribute(self):
        elem = func.Element(attributeTypeList=["color"], attributeValueList=["red"])
        elem.Append("position", (0,0))
        self.assertEqual(elem["position"], (0,0))
        
    # Testing getter
    def test_get_existing_attribute(self):
        elem = func.Element(attributeTypeList=["color"], attributeValueList=["red"])
        self.assertEqual(elem["color"], "red")
        
    # Test getter (element that does not exist)
    def test_get_nonexisting_attribute(self):
        elem = func.Element(attributeTypeList=["color"], attributeValueList=["red"])
        with self.assertRaises(AssertionError):
            elem["position"]

    # Testing empty attributes        
    def test_empty_attribute_lists(self):
        elem = func.Element()
        self.assertEqual(len(elem.attributeListDictionary), 0)


class TestSimpleOutput(unittest.TestCase):
    
    def test_generateSimpleOutputString(self):
        
        ts = func.TrafficSystem()
        # create sample data
        ts.roadList = [
            {"name": "road1", "length": 5},
            {"name": "road2", "length": 3}
        ]
        ts.vehicleList = [
            {"type": "car", "road": "road1", "position": 2},
            {"type": "bus", "road": "road1", "position": 4},
            {"type": "fire truck", "road": "road2", "position": 1},
            {"type": "ambulance", "road": "road2", "position": 2},
        ]
        ts.trafficLightList = [
            {"road": "road1", "position": 1, "cycle": 20},
            {"road": "road1", "position": 3, "cycle": 10},
            {"road": "road2", "position": 0, "cycle": 20}
        ]
        ts.busStopList = [
            {"road": "road1", "position": 0},
            {"road": "road2", "position": 2}
        ]
        
        # call the method with a specific time
        output = ts.generateSimpleOutputString(10)
        
        # check the output string
        expected_output = (
            "\nroad1\n"
            " > road          |=C==B|\n"
            " > trafficLights |G R  |\n"
            " > bus stops     | B   |\n"
            "\nroad2\n"
            " > road          |= ==|\n"
            " > trafficLights |G   |\n"
            " > bus stops     |   B|\n"
        )
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()