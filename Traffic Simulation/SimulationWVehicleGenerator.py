# 3.4
import VehicleCalculations
from TrafficSimulation2 import TrafficSystem
from AutomaticSimulation import AutomaticSimulation
import os

# Goal: Simulation with vehicle generator
# Precondition: The system contains a diagram of the virtual road network. There is a vehicle generator on a road.
# Postcondition: Vehicles are added automatically during the simulation.

# VehicleGeneratorSimulation inherits from AutomaticSimulation
# VehicleGeneratorSimulation contains all object lists and functions necessary for automatic simulation with
# vehicle generator functionality. First create VehicleGeneratorSimulation object, then call update.
# Atributes:
#   trafficSystem (inherited)
#       - TrafficSystem object from TrafficSimulation2.py
#   vehicle_list (inherited)
#       - vehicle list generated from trafficSystem
#   traffic_light_list (inherited)
#       - traffic light list generated from trafficSystem
#   vehicle_generator_list
#       - vehicle generator list generated from trafficSystem
#   vehicle_generator_ready
#       - list of dictionaries that holds when each VG is ready and how many updates until ready
# Methods:
#   vehicle_on_road()
#       -prints all vehicles' position and road
#   traffic_light_on_road()
#       -prints all traffic lights' position and cycle
#   vehicle_generator_update()
#       -loops through vg list and adds a new vehicle for each vg on frequency
#   update()
#       -calls vehicle_on_road(), traffic_light_on_road(), and vehicle_generator_update()
class VehicleGeneratorSimulation(AutomaticSimulation):

    def __init__(self, input_file):
        super().__init__(input_file)
        # Get Vehicle Generator List
        self.vehicle_generator_list = self.trafficSystem.vehicleGeneratorList
        # Declare and initalize list of Vehicle Generator dictionaries to keep track of VGs
        self.vehicle_generator_ready = []
        for vg in self.vehicle_generator_list:
            self.vehicle_generator_ready.append({"ready": False, "counter": 0})

    def vehicle_generator_update(self):

        # 3. FOR any vehicle generator
        for i in range(len(self.vehicle_generator_list)):
            # If the vehicle generator is not ready, increase count by 1
            if self.vehicle_generator_ready[i]["ready"] == False:
                self.vehicle_generator_ready[i]["counter"] += 1
            # 3.1 If time since last vehicle > frequency
            if self.vehicle_generator_ready[i]["counter"] == self.vehicle_generator_list[i]["frequency"]:
                self.vehicle_generator_ready[i]["ready"] = True
            # 3.1.1 If no vehicle on road between positions 0 and 2*(length of vehicle)
            noVehicle = True
            for v in self.vehicle_list:
                vType = VehicleCalculations.vehicleType[self.vehicle_generator_list[i]['type']]
                if (v["road"] == self.vehicle_generator_list[i]["name"]) and (v["position"] <= (VehicleCalculations.lengths[vType] * 2)):
                    noVehicle = False
            # 3.1.1.1 (If all of the above) THEN add vehicle to road at position 0
            if (noVehicle and self.vehicle_generator_ready[i]["ready"]):
                gen = self.vehicle_generator_list[i]
                self.create_vehicle_on_road(gen["name"], gen["position"], gen["speed"], gen["acceleration"], gen["type"])
                # Reset vehicle generator ready
                self.vehicle_generator_ready[i]["ready"] = False
                self.vehicle_generator_ready[i]["counter"] = 0
                return True
        return False

    # overrides AutomaticSimulation update()
    def update(self):
        self.vehicle_generator_update()
        super().update()
