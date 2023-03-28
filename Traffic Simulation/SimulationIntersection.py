#3.7 Simulation of intersections
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
APPROACHING_DISTANCE = 5

class IntersectionSim:

    def __init__(self):

        self.autoSim = AutomaticSimulation()
        self.autoSim.update()
        self.vehicle_state = self.autoSim.vehicle_current_state
        self.trafficlight_state = self.autoSim.trafficlight_current_state

        print("\n==============================================")
        print(self.vehicle_state)
        print("==============================================")


    def is_approaching_N_selected_road(self):

        for i in range(len(self.vehicle_state)):
            for j in range(len(self.trafficlight_state)):

                # Is on the current road?
                if self.vehicle_state[i]["road"] == (self.trafficlight_state[j]["road"]):
                    print("\n---FOUND MATCH---")
                    print("Index:", i , "vehicle on the road :-", self.vehicle_state[i]["road"])
                    print("Index:", j , "trafficInter road name :-", self.trafficlight_state[j]["road"], "\n")

                    # print(i, "position",  self.vehicle_state[i]["position"])
                    # print(j , "position", self.trafficlight_state[j]["position"], "\n")

                    # (self.trafficlight_state[j]["position"])-APPROACHING_DISTANCE
                    # This will get the distance of the road and subtract it from the yield distance
                    # If the vehicle is in the yield distance, then start the process
                    if self.vehicle_state[i]["position"] >= (self.trafficlight_state[j]["position"])-APPROACHING_DISTANCE: 

                        # Choose a different road randomly
                        selected_road_loop = True
                        while(selected_road_loop):

                            # This will decide what road shoud bee taken next
                            num = random.randint(0, len(self.vehicle_state)-1)
                            
                            # Use the implementation of 1.5 here to get the road name
                            # Replace self.vehicle_state[i]["road"] with case 1.5
                            if(self.vehicle_state[i]["road"] != self.vehicle_state[num]["road"]):
                                print("---SWAP ROAD---")
                                print("Index:", i , self.vehicle_state[i]["road"], "SWAP WITH", "Index:", num , self.vehicle_state[num]["road"])
                                self.vehicle_state[i]["road"] = self.vehicle_state[num]["road"]

                                print("After Swap")
                                print("Index:", i , self.vehicle_state[i]["road"])
                                selected_road_loop = False

                                print("--------------------")
                                print(self.vehicle_state)
                                print("--------------------")


    def update(self):
        self.is_approaching_N_selected_road()
        
        
interSim = IntersectionSim()        
interSim.update()


    
            
            



            

    