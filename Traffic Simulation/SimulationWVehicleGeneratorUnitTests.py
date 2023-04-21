import unittest
import SimulationWVehicleGenerator

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

# Unit Testing
class TestVehicleGeneratorSim(unittest.TestCase):
    def test_vg_obstructed(self):
        self.sim = SimulationWVehicleGenerator.VehicleGeneratorSimulation()
        self.sim.vehicle_generator_list = [{"name": "Tropicana", "frequency": 10, "type": "auto"}]
        self.sim.vehicle_list = [{"road": "Tropicana", "position": 0, "speed": 10, "acceleration": 1.2, "type": "car"}]
        vehicleCount = len(self.sim.vehicle_list)
        updateCount = self.sim.vehicle_generator_list[0]["frequency"]
        for i in range(updateCount):
            self.sim.vehicle_generator_update()
        
        """Vehicle List has not grown"""
        self.assertTrue(vehicleCount == len(self.sim.vehicle_list))
        """VG is ready"""
        self.assertTrue(self.sim.vehicle_generator_ready[0]["ready"])
        """VG counter is 1 + the number of updates performed"""
        self.assertTrue(self.sim.vehicle_generator_ready[0]["counter"] == self.sim.vehicle_generator_list[0]["frequency"])

    def test_vg_unobstructed(self):
        self.sim = SimulationWVehicleGenerator.VehicleGeneratorSimulation()
        self.sim.vehicle_generator_list = [{"name": "Tropicana", "frequency": 10, "type": "auto"}]
        self.sim.vehicle_list = [{"road": "Tropicana", "position": 200, "speed": 10, "acceleration": 1.2, "type": "car"}]
        vehicleCount = len(self.sim.vehicle_list)
        updateCount = self.sim.vehicle_generator_list[0]["frequency"]
        for i in range(updateCount):
            self.sim.vehicle_generator_update()
        
        """Vehicle List has grown"""
        self.assertFalse(vehicleCount == len(self.sim.vehicle_list))
        """VG is no longer ready"""
        self.assertFalse(self.sim.vehicle_generator_ready[0]["ready"])
        """VG counter is reset to 1"""
        self.assertTrue(self.sim.vehicle_generator_ready[0]["counter"] == 0)
        
unittest.main()
