# 3.3
from VehicleCalculations import *
from TrafficSimulation2 import *
from TrafficLightSimulation import *


class AutomaticSimulation:
    def __init__(self):
        # create a TrafficSystem object from the input file
        self.traffic_system = MovingVehicle()
        self.TrafficLight = TrafficLight()
        self.TrafficSystem = TrafficSystem()

        # Get Vehicle List
        self.vehicle_list = self.TrafficSystem.vehicleList
        # Get Traffic Light List
        self.traffic_light_list = self.TrafficSystem.trafficLightList

        self.generated_vehicles = []


    def vehicle_on_road(self):
        print('vehicle list')
        # 1. FOR any vehicle in the road network
        #for i in range(len(self.vehicle_list)):
            # 3.1 GOES HERE
            # Execute use-case 3.1 out on the vehicle
            

    def traffic_light_on_road(self):
        print('traffic_light list')
        # 2. FOR any traffic light in the road network
       # for i in range(len(self.traffic_light_list)):
            

    def update(self):
        self.vehicle_on_road()
        self.traffic_light_on_road()



simulation = AutomaticSimulation()
simulation.update()