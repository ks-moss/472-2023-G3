# 3.3
from TrafficSimulation2 import *
from VehicleCalculations import *
from TrafficLightSimulation  import *

# Goal: Run simulation automatically
# Precondition: The system contains a diagram of the virtual road network.
# Postcondition: The traffic in the road network is simulated.


# AutomaticSimulation contains all object lists and functions necessary for automatic simulation.
# First create AutomaticSimulation object, then call update on that object
# Atributes:
#   trafficSystem
#       - TrafficSystem object from TrafficSimulation2.py
#   vehicle_list
#       - vehicle list generated from trafficSystem
#   traffic_light_list
#       - traffic light list generated from trafficSystem
# Methods:
#   vehicle_on_road()
#       -prints all vehicles' position and road
#   traffic_light_on_road()
#       -prints all traffic lights' position and cycle
#   update()
#       -calls vehicle_on_road() and traffic_light_on_road()
class AutomaticSimulation:
    def __init__(self):
         # create a TrafficSystem object from the input file
        self.trafficSystem = TrafficSystem()
        self.trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim2.xml")        
        # Get Vehicle List
        self.vehicle_list = self.trafficSystem.vehicleList
        # Get Traffic Light List
        self.traffic_light_list = self.trafficSystem.trafficLightList
        # Store current state of vehicle
        self.vehicle_current_state = []
        for i in range(len(self.vehicle_list)):
            self.vehicle_current_state.append({"road": '', "position": 0})
        
        # Store current state of trafficlight
        self.trafficlight_current_state = []
        for i in range(len(self.traffic_light_list)):
            self.trafficlight_current_state.append({"road": '', "position": 0, "cycle" : 0})



    def vehicle_on_road(self):
        # 1. FOR any vehicle in the road network
        for i in range(len(self.vehicle_list)):
            # 3.1 GOES HERE
            # Execute use-case 3.1 out on the vehicle
            print("Vehicle:" , i)
            print("    -> road: ", self.vehicle_list[i]["road"])
            print("    -> position: ", self.vehicle_list[i]["position"])
            self.vehicle_current_state[i]["road"] = self.vehicle_list[i]["road"]
            self.vehicle_current_state[i]["position"] = self.vehicle_list[i]["position"]
            #VehicleCalculations.calculateVehicleSpeedAndPosition(i, 16.6, 100)
            #print(i)
        
    def traffic_light_on_road(self):
        
        # 2. FOR any traffic light in the road network
        for i in range(len(self.traffic_light_list)):
            print("Road: ", self.traffic_light_list[i]["road"])
            print("    -> position: ", self.traffic_light_list[i]["position"])
            print("    -> cycle: ", self.traffic_light_list[i]["cycle"])
            self.trafficlight_current_state[i]["road"] = self.traffic_light_list[i]["road"]
            self.trafficlight_current_state[i]["position"] = self.traffic_light_list[i]["position"]
            self.trafficlight_current_state[i]["cycle"] = self.traffic_light_list[i]["cycle"]
            # TrafficLightSimulation.trafficLightInteraction(self.trafficSystem, self.vehicle_list, self.traffic_light_list[i]["cycle"])

    def update(self):
        self.vehicle_on_road()
        self.traffic_light_on_road()
        


"""simulation = AutomaticSimulation()
simulation.update()
print(simulation.vehicle_current_state)
print(simulation.vehicle_current_state[0]["road"])
print(simulation.trafficlight_current_state)
print(simulation.trafficlight_current_state[0]["road"])

                # Is on the current road?
                if self.vehicle_state[i]["road"] == (self.trafficlight_state[j]["road"]
                    # Is approaching the intersection?
                    if self.vehicle_state[i]["position"] >= (self.trafficlight_state[j]["position"])-APPROACHING_DISTANCE: 
                        # Choose a different road randomly
                        selected_road_loop = True
                        while(selected_road_loop):
                            num = random.randint(0, len(self.trafficlight_state)-1)
                            
                                
                            if(self.vehicle_state[i]["road"] != self.trafficlight_state[num]["road"]):
                                    self.vehicle_state[num]["road"] = self.trafficlight_state[num]["road"]
                                    selected_road_loop = False

"""
# for i in range(len(simulation.vehicle_current_state)):
  # print( calculateVehicleSpeedAndPosition(simulation.vehicle_list, i)  )
  # print( calculateAcceleration(simulation.vehicle_list, i) )
  # print(adjustAccelerationToStop(16.6))