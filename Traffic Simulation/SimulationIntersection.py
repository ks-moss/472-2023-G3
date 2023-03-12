#3.7
from AutomaticSimulation import *
import random

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

                    if self.vehicle_state[i]["position"] >= (self.trafficlight_state[j]["position"])-APPROACHING_DISTANCE: 

                        # Choose a different road randomly
                        selected_road_loop = True
                        while(selected_road_loop):
                            num = random.randint(0, len(self.vehicle_state)-1)
                            
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


    
            
            



            

    