#3.7 Simulation of intersections
from TrafficSimulation2 import *
from AutomaticSimulation import *
import random

# Goal:
# A road can contain intersections. Vehicles must choose which road to follow at an intersection.
# You also need to implement use case 1.5 for this.

# Precondition:
# The system contains a sceme of the virtual traffic network. This scheme contains at least 2 roads and 1 intersection.
# Postcondition:Vehicles choose a road at each intersection.

# Notes:
# If the position of an intersection on a road is equal to the length of the road, then the road ends at that intersection. 
# Vehicles will therefore not be able to choose this road at this intersection. 
# If the position of an intersection on a road is zero, then the road starts at that intersection.

# Atributes:
#   trafficSystem
#       - AutomaticSimulation
#   vehicle_state
#       - vehicle list (Vehicles choose a road at each intersection) 
#   trafficlight_state
#       - Store state of all intersections
# Methods:
#   is_approaching_N_selected_road
#       - First check if the vehicle is on thesame road as the intersection is located
#       - Secondly, check if the current position of hte vehicle is approaching the intersection
#           - If yes, then make a choice the swap the road
#           - If no, keep searching



# Set the yield distance of the traffic light
# When vehicle is close to the traffic light with assigned distance, starts choosing the road then turn
APPROACHING_DISTANCE = 3

class IntersectionSim:

    def __init__(self):

        # create a TrafficSystem object from the input file
        self.trafficSystem = TrafficSystem()
        self.trafficSystem.ReadElementsFromFile("./InputFiles/trafficSim1.xml")

        self.autoSim = AutomaticSimulation()
        self.autoSim.update()
        self.vehicle_state = self.autoSim.vehicle_current_state
        # Get Crossroads
        self.intersection_list = self.trafficSystem.intersectionList

        print("\n==============================================")
        print(self.vehicle_state)
        print("==============================================")


    def is_approaching_N_selected_road(self):

        for i in range(len(self.vehicle_state)):
            for j in range(len(self.intersection_list)):
                for k in range(len(self.intersection_list[j])):

                    # Is on the current road?
                    # This will check if the current vehicle is on the same road as the intersection

                    if (self.vehicle_state[i]["road"] == self.intersection_list[j][k]["road"]):
                        print("\n\n================================================================")
                        print("---> FOUND VEHICLE ON THE ROAD / INTERSECTION <---")
                        print("| Vehicle Type: ", self.vehicle_state[i]["type"])
                        print("| Vehicle is on the road: ", self.vehicle_state[i]["road"])
                        print("| Intersection on the road: ", self.intersection_list[j][k]["road"])

                        print("| Vehicle Position: ",  self.vehicle_state[i]["position"])
                        print("| Intersection Position: ", self.intersection_list[j][k]["position"])

                        # self.intersection_list[j][k]["position"]-APPROACHING_DISTANCE
                        # This will get the distance of the road and subtract it from the yield distance
                        # If the vehicle is in the yield distance, then start the process
                        trafficlight_position = (self.intersection_list[j][k]["position"])
                        vehicle_position = (self.vehicle_state[i]["position"]+APPROACHING_DISTANCE)
                        yield_distance = (self.intersection_list[j][k]["position"]-APPROACHING_DISTANCE)

                        print("--------------------------------------------------")
                        print("| Traffic Light Lists: ", self.intersection_list[j])
                        print("| Trafficlight Position:", trafficlight_position)
                        print("| Vehicle Position:", vehicle_position)
                        print("| Yield Distance:", yield_distance)
                        print("| Index j: ", j)
                        print("| Index k: ", k)
                        print("--------------------------------------------------")
                        
                        if (vehicle_position < trafficlight_position) and (vehicle_position >= yield_distance): 
                            print("\n==========> VEHICLE IS APPROACHING THE INTERSECTION <==========")

                            selected_road = ''

                            if(k == 0):   
                                print("| Selected Road: ", self.intersection_list[j][1]["road"])    
                                selected_road = self.intersection_list[j][1]["road"]
                            
                            if(k == 1):
                                print("| Selected Road: ", self.intersection_list[j][0]["road"])
                                selected_road = self.intersection_list[j][0]["road"]
                            

                            self.vehicle_state[i]["road"] = selected_road
                            print("| Vehicle Type: ", self.vehicle_state[i]["type"])
                            print("| Swap The current Road With Selected Road: ", self.vehicle_state[i]["road"])

                            print("================================================================")
                        else:
                            print("| ", self.vehicle_state[i]["type"], "Is Far Away From The Intersection")

                            print("================================================================")
                                           

    def update(self):
        self.is_approaching_N_selected_road()
        
        
interSim = IntersectionSim()        
interSim.update()


    
            
            



            

    