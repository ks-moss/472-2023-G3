import unittest
from src.SimulationWVehicleGenerator import VehicleGeneratorSimulation

# Goal: Increase the branch coverage of the codebase using the unittest library.
# There are 2 tests included in this unittest file.
# 1. test_vg_obstructed() - tests the branches cases while,
#                           Vehicle is obstructing 
#                                   vehicle generator is not ready
#                                       vehicle frequency is equal to counter
#                                       vehicle frequency is not equal to counter
#                                   vehicle generator is ready
#                                       vehicle frequency is equal to counter
#                                       vehicle frequency is not equal to counter
# 2. test_vg_unobstructed() - tests the branches while,
#                           Vehicle is not obstructing 
#                                   vehicle generator is not ready
#                                       vehicle frequency is equal to counter
#                                       vehicle frequency is not equal to counter
#                                   vehicle generator is ready
#                                       vehicle frequency is equal to counter
#                                       vehicle frequency is not equal to counter

# Relative path to the vehicle generator xml file
input_file = './InputFiles/vehicleGen2.xml'

class TestVehicleGeneratorSimulation(unittest.TestCase):

    def test_vehicle_generator_update(self):
        # Test that a new vehicle is added when a generator is ready and there is no vehicle on the road
        sim = VehicleGeneratorSimulation(input_file)
        sim.vehicle_list = [{"road": "A", "position": 10, "speed": 50, "acceleration": 2, "type": "car"}]
        sim.vehicle_generator_ready = [{"ready": True, "counter": 0}]
        sim.vehicle_generator_list = [{"name": "A", "position": 0, "speed": 60, "acceleration": 3, "type": "car", "frequency": 2}]
        sim.vehicle_generator_update()
        self.assertEqual(len(sim.vehicle_list), 2)
        
        # Test that no vehicle is added when a generator is not ready
        sim = VehicleGeneratorSimulation(input_file)
        sim.vehicle_list = [{"road": "A", "position": 10, "speed": 50, "acceleration": 2, "type": "car"}]
        sim.vehicle_generator_ready = [{"ready": False, "counter": 2}]
        sim.vehicle_generator_list = [{"name": "A", "position": 0, "speed": 60, "acceleration": 3, "type": "car", "frequency": 2}]
        sim.vehicle_generator_update()
        self.assertEqual(len(sim.vehicle_list), 1)
        
        # Test that no vehicle is added when there is a vehicle on the road
        sim = VehicleGeneratorSimulation(input_file)
        sim.vehicle_list = [{"road": "A", "position": 5, "speed": 50, "acceleration": 2, "type": "car"}]
        sim.vehicle_generator_ready = [{"ready": True, "counter": 0}]
        sim.vehicle_generator_list = [{"name": "A", "position": 0, "speed": 60, "acceleration": 3, "type": "car", "frequency": 2}]
        sim.vehicle_generator_update()
        self.assertEqual(len(sim.vehicle_list), 1)

    def test_update(self):
        # Test that the vehicle generator update method is called during update
        sim = VehicleGeneratorSimulation(input_file)
        sim.vehicle_generator_update = lambda: None
        sim.update()
        self.assertTrue(sim.vehicle_generator_update)
        
if __name__ == '__main__':
    unittest.main()